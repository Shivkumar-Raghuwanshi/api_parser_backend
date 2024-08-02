from django.db import models

class APIDocument(models.Model):
    # Store the title of the API document
    title = models.CharField(max_length=255)
    # Store the content of the API document
    content = models.TextField()
    # Automatically set the creation time when a new instance is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the model instance
        return self.title

class GeneratedCode(models.Model):
    # Foreign key relationship to APIDocument
    # If the related APIDocument is deleted, also delete this GeneratedCode instance
    api_document = models.ForeignKey(APIDocument, on_delete=models.CASCADE)
    # Store the generated code
    code = models.TextField()
    # Automatically set the creation time when a new instance is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the model instance
        return f"Generated code for {self.api_document.title}"

class APIData(models.Model):
    # Foreign key relationship to GeneratedCode
    # If the related GeneratedCode is deleted, also delete this APIData instance
    generated_code = models.ForeignKey(GeneratedCode, on_delete=models.CASCADE)
    # Store JSON data
    data = models.JSONField()
    # Store the file path where the data is saved
    file_path = models.CharField(max_length=255)
    # Automatically set the creation time when a new instance is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the model instance
        return f"API data for {self.generated_code}"