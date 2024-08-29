import ee
import os
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Extractor:
    def __init__(self, client_secrets_path='client_secrets.json'):
        """
        Initializes the GEEImageExtractor with Google Drive authentication.
        
        Args:
        - client_secrets_path (str): Path to the Google API client secrets file.
        """
        self.gauth = GoogleAuth()
        self.gauth.LoadClientConfigFile(client_secrets_path)
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

    def extract_images(self, path, geometry_object, date_range, bands=None, file_name="temp_file"):
        """
        Extracts and downloads images from an ImageCollection in GEE based on the provided parameters.

        Args:
        - path (str): The dataset or image collection path.
        - geometry_object (ee.Geometry): The region for which the data is required.
        - date_range (tuple): The date range in the format (start_date, end_date).
        - bands (list, optional): The bands of interest. Defaults to None.
        - file_name (str): The base name for the downloaded files.

        Returns:
        - List of download URLs for each image that matches the filters.
        """
        try:
            collection = ee.ImageCollection(path)
            collection_size = collection.size().getInfo()

            if collection_size <= 0:
                print("No collection found at the given path.")
                return []

            # Filter by date range and geometry
            filtered_collection = collection.filterDate(date_range[0], date_range[1]).filterBounds(geometry_object)
            if bands:
                filtered_collection = filtered_collection.select(bands)

            download_urls = []
            for index, image_info in enumerate(filtered_collection.toList(filtered_collection.size()).getInfo()):
                print(f"Processing image {index}")
                folder_name = f"{file_name}_folder_{index}"

                try:
                    self.extract_and_download_image(image_info, geometry_object, file_name, folder_name)
                    download_urls.append(f"Folder: {folder_name}, Image: {file_name}.tif")
                except Exception as e:
                    print(f"An error occurred while processing image {index}: {e}")

            return download_urls

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def extract_and_download_image(self, image_info, geometry, output_image_name='extraction_temp_file', folder_name='extraction_temp_folder', scale=30, number_of_pixels=1e13):
        """
        Extracts an image from GEE and downloads it to Google Drive.

        Args:
        - image_info (dict): The image information from GEE.
        - geometry (ee.Geometry): The region for which the data is required.
        - output_image_name (str): The base name of the downloaded image file.
        - folder_name (str): The folder name for saving the image.
        - scale (int): The scale for the GEE export.
        - number_of_pixels (float): The maximum number of pixels for the GEE export.
        """
        file_name = f"{output_image_name}.tif"
        if image_info is None:
            print("Image not found.")
            return

        image = ee.Image(image_info['id']).toFloat()
        try:
            export_task = ee.batch.Export.image.toDrive(
                image=image,
                description=output_image_name,
                folder=folder_name,
                region=geometry,
                scale=scale,
                maxPixels=number_of_pixels,
            )
            export_task.start()

            while export_task.status()['state'] in ['READY', 'RUNNING']:
                print(f"Task status: {export_task.status()['state']}")
                time.sleep(5)

            if export_task.status()['state'] == 'COMPLETED':
                print("Export to GDrive completed successfully!")
            else:
                print(f"Export {export_task.id} to GDrive failed with state: {export_task.status()['state']}")
                return

            self.download_from_drive(folder_name, file_name)

        except Exception as e:
            print(f"An error occurred while exporting the image: {e}")

    def download_from_drive(self, folder_name, file_name):
        """
        Downloads a file from Google Drive by searching for it in a specific folder.

        Args:
        - folder_name (str): The name of the folder in Google Drive where the file is stored.
        - file_name (str): The name of the file to be downloaded.
        """
        try:
            folder_list = self.drive.ListFile({'q': f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed=false"}).GetList()

            if not folder_list:
                print(f"Folder '{folder_name}' not found. Please check the folder name.")
                return
            else:
                folder_id = folder_list[0]['id']
                print(f"Folder '{folder_name}' found with ID: {folder_id}")

                file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

                for file1 in file_list:
                    local_folder_path = folder_name
                    local_file_path = os.path.join(local_folder_path, file1['title'])

                    if not os.path.exists(local_folder_path):
                        os.makedirs(local_folder_path)
                        print(f"Folder '{local_folder_path}' created.")

                    file1.GetContentFile(local_file_path)
                    print(f"File '{local_file_path}' downloaded successfully.")
                else:
                    print(f"File not found in the folder '{folder_name}'.")

        except Exception as e:
            print(f"An error occurred while accessing Google Drive: {e}")


# Example usage:
# if __name__ == "__main__":
#     ee.Initialize()
    
#     path = 'LANDSAT/LC08/C02/T1_L2'
#     geometry = ee.Geometry.Point([77.2, 28.6])
#     date_range = ('2022-01-01', '2022-01-31')

#     extractor = Extractor('../secrets/client_secrets.json')
#     extractor.extract_images(path, geometry, date_range)
