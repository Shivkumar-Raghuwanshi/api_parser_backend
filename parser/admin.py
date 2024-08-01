from django.contrib import admin

# Register your models here.


from . models import  APIDocument, APIData, GeneratedCode
# Register your models here.
admin.site.register( APIDocument)
admin.site.register( APIData)
admin.site.register(GeneratedCode)