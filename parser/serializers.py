from rest_framework import serializers
from .models import APIDocument, GeneratedCode, APIData

class APIDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIDocument
        # Define which fields to include in the serialized output
        fields = ['id', 'title', 'content', 'created_at']

class APIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIData
        # Define which fields to include in the serialized output
        fields = ['id', 'generated_code', 'data', 'file_path', 'created_at']

class GeneratedCodeSerializer(serializers.ModelSerializer):
    # Nest the APIDocumentSerializer for the related api_document
    api_document = APIDocumentSerializer(read_only=True)
    # Prepare for nesting APIDataSerializer (will be populated in to_representation)
    api_data = APIDataSerializer(read_only=True)

    class Meta:
        model = GeneratedCode
        # Define which fields to include in the serialized output
        fields = ['id', 'api_document', 'code', 'created_at', 'api_data']

    def to_representation(self, instance):
        # Customize the output representation
        representation = super().to_representation(instance)
        # Fetch the related APIData instance
        api_data = APIData.objects.filter(generated_code=instance).first()
        if api_data:
            # If APIData exists, include its serialized data
            representation['api_data'] = APIDataSerializer(api_data).data
        return representation

class DetailedAPIDataSerializer(serializers.ModelSerializer):
    # Nest the GeneratedCodeSerializer for the related generated_code
    generated_code = GeneratedCodeSerializer(read_only=True)

    class Meta:
        model = APIData
        # Define which fields to include in the serialized output
        fields = ['id', 'generated_code', 'data', 'file_path', 'created_at']