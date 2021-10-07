"""Handles TAPIS functionality related to files."""

import os

from core.TapisController import TapisController
from tapipy.errors import InvalidInputError


class Files(TapisController):
    """Contains all of the CRUD functions associated with files."""
    def __init__(self):
        TapisController.__init__(self)
        
    def delete(self, system_id, path) -> None:
        """Deletes the specified file from the target system."""
        try:
            self.client.files.delete(systemId=system_id, path=path)
            self.logger.info(f"Deleted file '{path}' in system '{system_id}'\n")
            return
        except InvalidInputError:
            self.logger.error(f"File '{path}' not found in system '{system_id}'\n")
            return

    def get_contents(self, system_id, path) -> None:
        """Retrieves the contents of the specified file in the target system."""
        try:
            contents = self.client.files.getContents(systemId=system_id, path=path)
            self.logger.newline(1)
            self.logger.complete(f"Fetched contents of file '{path}':\n")
            print(contents, "\n")
            return
        except InvalidInputError:
            self.logger.error(f"File '{path}' not found in system '{system_id}'\n")
            return
        
    def list(self, system_id, path) -> None:
        """List every file on the target system."""
        # BUG Seems to be breaking a LOT... very rarely works.
        files = self.client.files.listFiles(systemId=system_id, path=path)
        for file in files:
            print(file.name)

        return

    def upload(self, system_id, path_to_file, destination_folder) -> None:
        """
        Uploads the specified file to the provided file path on the target system.
        The destination must inlcude all sub directories and a filename.
        (Directories that don't exist in destination will be created.)
        EX: '/home/folder1/folder2/filename.txt'

        NOTE: The Tapipy client hasn't yet implemented the insert method in the
        files module. The upload method on the Tapis class handles this instead.
        """    
        try:
            self.client.upload(
                system_id = system_id,
                source_file_path = path_to_file,
                dest_file_path = destination_folder
            )
            self.logger.newline(1)
            self.logger.complete(f"Uploaded file '{path_to_file}' to {destination_folder}\n")
            return
        except Exception as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    def upload_folder(self, system_id, path_to_folder, destination_folder) -> None:
        """ 
        Uploads the every file in the specified folder file the provided destination
        folder file path on the target system. Unlike upload(), this will automatically
        provide the filenames on the target system.
        EX: '/home/folder1/folder2/ /user/foldername
        """
        print("\nUploading files...\n")
        for file in os.listdir(path_to_folder):
            if os.path.isdir(os.path.join(path_to_folder, file)):
                self.logger.warn(f"'{file}' is a folder, so its contents will not be uploaded.")
                continue
            try:
                self.client.upload(
                    system_id = system_id,
                    source_file_path = os.path.join(path_to_folder, file),
                    dest_file_path = os.path.join(destination_folder, file)
                )
                self.logger.complete(f"Successfully uploaded {file} to {os.path.join(destination_folder, file)}")
            except Exception as e:
                self.logger.error(f"{e.message}\n")
                self.exit(1)

        self.logger.success(f"Successfully uploaded files to {destination_folder}\n")
        return