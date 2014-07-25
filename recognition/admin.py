from django.contrib import admin
from .models import Classifier
# Register your models here.

"""
#TODO: make it work with mongoengine
class ClassifierAdmin(admin.ModelAdmin):
    model = Classifier

admin.site.register(Classifier, ClassifierAdmin)
"""