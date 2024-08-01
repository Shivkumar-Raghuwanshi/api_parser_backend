
from django.db import models

class APIDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GeneratedCode(models.Model):
    api_document = models.ForeignKey(APIDocument, on_delete=models.CASCADE)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generated code for {self.api_document.title}"

class APIData(models.Model):
    generated_code = models.ForeignKey(GeneratedCode, on_delete=models.CASCADE)
    data = models.JSONField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API data for {self.generated_code}"

