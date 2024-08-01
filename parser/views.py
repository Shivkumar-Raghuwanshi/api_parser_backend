from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse
from .models import APIDocument, GeneratedCode, APIData
from .serializers import APIDocumentSerializer, GeneratedCodeSerializer, APIDataSerializer, DetailedAPIDataSerializer
from .api_parser import APIDocParser
from .code_generator import CodeGenerator
from .data_processor import DataProcessor
from .file_storage import FileStorage
import json
import logging
import os
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

class APIDocumentList(generics.ListCreateAPIView):
    queryset = APIDocument.objects.all()
    serializer_class = APIDocumentSerializer

class APIDocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = APIDocument.objects.all()
    serializer_class = APIDocumentSerializer

class GeneratedCodeList(generics.ListAPIView):
    queryset = GeneratedCode.objects.all()
    serializer_class = GeneratedCodeSerializer

class GeneratedCodeDetail(generics.RetrieveAPIView):
    queryset = GeneratedCode.objects.all()
    serializer_class = GeneratedCodeSerializer

class APIDataList(generics.ListAPIView):
    queryset = APIData.objects.all()
    serializer_class = APIDataSerializer

class APIDataDetail(generics.RetrieveAPIView):
    queryset = APIData.objects.all()
    serializer_class = APIDataSerializer

class InterpretAPIDocumentation(APIView):
    def post(self, request):
        serializer = APIDocumentSerializer(data=request.data)
        if serializer.is_valid():
            api_doc = serializer.save()
            
            parser = APIDocParser()
            try:
                api_info = parser.parse_documentation(api_doc.content)
            except ValueError as e:
                logger.error(f"Error parsing API documentation: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            generator = CodeGenerator()
            try:
                code_response = generator.generate_code(api_info)
                if code_response.status_code != status.HTTP_200_OK:
                    return code_response
                code = code_response.data['generated_code']
            except Exception as e:
                logger.error(f"Error generating code: {str(e)}")
                return Response({'error': 'Failed to generate code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            generated_code = GeneratedCode.objects.create(
                api_document=api_doc,
                code=code,
            )

            data_processor = DataProcessor()
            try:
                processed_data = data_processor.process_json(json.dumps(api_info))
                
                # Generate CSV
                filename = f'api_data_{generated_code.id}.csv'
                csv_content = DataProcessor.save_to_csv_flattened(processed_data)
                
                # Save CSV file using FileStorage
                file_path = FileStorage.save_file(filename, csv_content)
                
                api_data = APIData.objects.create(
                    generated_code=generated_code,
                    data=processed_data,
                    file_path=file_path
                )
            except Exception as e:
                logger.error(f"Error processing API data: {str(e)}")
                return Response({'error': 'Failed to process API data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'api_doc': APIDocumentSerializer(api_doc).data,
                'generated_code': GeneratedCodeSerializer(generated_code).data,
                'api_data': APIDataSerializer(api_data).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExecuteGeneratedCode(APIView):
    def post(self, request):
        generated_code_id = request.data.get('generated_code_id')
        try:
            generated_code = GeneratedCode.objects.get(id=generated_code_id)
        except GeneratedCode.DoesNotExist:
            return Response({'error': 'Generated code not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'Code execution is disabled for security reasons',
            'code': generated_code.code
        })

class LatestGeneratedCodeView(APIView):
    def get(self, request):
        latest_code = GeneratedCode.objects.order_by('-created_at').first()
        if latest_code:
            serializer = GeneratedCodeSerializer(latest_code)
            return Response(serializer.data)
        return Response(None)

class LatestAPIDataView(APIView):
    def get(self, request):
        latest_data = APIData.objects.order_by('-created_at').first()
        if latest_data:
            serializer = DetailedAPIDataSerializer(latest_data)
            return Response(serializer.data)
        return Response(None)

class DownloadGeneratedCode(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                generated_code = GeneratedCode.objects.get(pk=pk)
            except GeneratedCode.DoesNotExist:
                return Response({'error': 'Generated code not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            generated_code = GeneratedCode.objects.order_by('-created_at').first()
            if not generated_code:
                return Response({'error': 'No generated code found'}, status=status.HTTP_404_NOT_FOUND)

        filename = f'generated_code_{generated_code.id}.py'
        try:
            file_path = FileStorage.save_file(filename, generated_code.code.encode())
            return FileResponse(default_storage.open(file_path, 'rb'), as_attachment=True, filename=filename)
        except IOError:
            logger.error(f"Error saving or opening file: {filename}")
            return Response({'error': 'Failed to generate file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadCSVFile(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                api_data = APIData.objects.get(pk=pk)
            except APIData.DoesNotExist:
                return Response({'error': 'API data not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            api_data = APIData.objects.order_by('-created_at').first()
            if not api_data:
                return Response({'error': 'No API data found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = api_data.file_path
        if not file_path:
            return Response({'error': 'File path not found'}, status=status.HTTP_404_NOT_FOUND)

        if not default_storage.exists(file_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            file_content = FileStorage.read_file(file_path)
            response = HttpResponse(file_content, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except IOError:
            logger.error(f"Error opening file: {file_path}")
            return Response({'error': 'Failed to open file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListCSVFiles(APIView):
    def get(self, request):
        api_data = APIData.objects.all().order_by('-created_at')
        csv_files = [
            {
                'id': data.id,
                'filename': os.path.basename(data.file_path),
                'created_at': data.created_at
            }
            for data in api_data if data.file_path and default_storage.exists(data.file_path)
        ]
        return Response(csv_files)