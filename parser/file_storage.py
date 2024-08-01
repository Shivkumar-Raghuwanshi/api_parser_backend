from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FileStorage:
    @staticmethod
    def save_file(filename, content):
        path = default_storage.save(filename, ContentFile(content))
        return path

    @staticmethod
    def read_file(filename):
        with default_storage.open(filename, 'r') as file:
            return file.read()