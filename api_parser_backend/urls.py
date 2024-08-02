"""
URL configuration for api_parser_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from parser import views 

urlpatterns = [
    # Django admin URL
    path('admin/', admin.site.urls),
    
    # API Document URLs
    path('api-documents/', views.APIDocumentList.as_view(), name='api-document-list'),
    path('api-documents/<int:pk>/', views.APIDocumentDetail.as_view(), name='api-document-detail'),
    
    # Generated Code URLs
    path('generated-code/', views.GeneratedCodeList.as_view(), name='generated-code-list'),
    path('generated-code/<int:pk>/', views.GeneratedCodeDetail.as_view(), name='generated-code-detail'),
    
    # API Data URLs
    path('api-data/', views.APIDataList.as_view(), name='api-data-list'),
    path('api-data/<int:pk>/', views.APIDataDetail.as_view(), name='api-data-detail'),
    
    # Interpretation URL
    path('interpret/', views.InterpretAPIDocumentation.as_view(), name='interpret'),
    
    # Code Execution URL (Note: This is disabled for security reasons)
    path('execute/', views.ExecuteGeneratedCode.as_view(), name='execute'),
    
    # Latest Generated Code and API Data URLs
    path('generated-code/latest/', views.LatestGeneratedCodeView.as_view(), name='latest-generated-code'),
    path('api-data/latest/', views.LatestAPIDataView.as_view(), name='latest-api-data'),
    
    # Download Generated Code URLs
    path('download-generated-code/<int:pk>/', views.DownloadGeneratedCode.as_view(), name='download-generated-code'),
    path('download-latest-generated-code/', views.DownloadGeneratedCode.as_view(), name='download-latest-generated-code'),
    
    # Download CSV URLs
    path('download-csv/<int:pk>/', views.DownloadCSVFile.as_view(), name='download-csv'),
    path('download-latest-csv/', views.DownloadCSVFile.as_view(), name='download-latest-csv'),
    
    # List CSV Files URL
    path('list-csv-files/', views.ListCSVFiles.as_view(), name='list-csv-files'),
]