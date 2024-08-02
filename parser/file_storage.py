from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FileStorage:
    @staticmethod
    def save_file(filename, content):
        """
        Saves a file to the default storage system.
        
        Args:
            filename (str): The name of the file to save.
            content (str): The content to be saved in the file.
        
        Returns:
            str: The path where the file was saved.
        """
        # Use Django's default storage to save the file
        # ContentFile is used to create a file-like object from the content string
        path = default_storage.save(filename, ContentFile(content))
        return path

    @staticmethod
    def read_file(filename):
        """
        Reads the content of a file from the default storage system.
        
        Args:
            filename (str): The name of the file to read.
        
        Returns:
            str: The content of the file.
        """
        # Open the file using Django's default storage
        with default_storage.open(filename, 'r') as file:
            # Read and return the file's content
            return file.read()