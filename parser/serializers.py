from rest_framework import serializers
from .models import APIDocument, GeneratedCode, APIData

class APIDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIDocument
        fields = ['id', 'title', 'content', 'created_at']

class APIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIData
        fields = ['id', 'generated_code', 'data', 'file_path', 'created_at']

class GeneratedCodeSerializer(serializers.ModelSerializer):
    api_document = APIDocumentSerializer(read_only=True)
    api_data = APIDataSerializer(read_only=True)

    class Meta:
        model = GeneratedCode
        fields = ['id', 'api_document', 'code', 'created_at', 'api_data']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        api_data = APIData.objects.filter(generated_code=instance).first()
        if api_data:
            representation['api_data'] = APIDataSerializer(api_data).data
        return representation

class DetailedAPIDataSerializer(serializers.ModelSerializer):
    generated_code = GeneratedCodeSerializer(read_only=True)

    class Meta:
        model = APIData
        fields = ['id', 'generated_code', 'data', 'file_path', 'created_at']

