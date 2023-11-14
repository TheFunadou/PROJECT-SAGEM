from django.contrib import admin

# Register your models here.
from django.contrib import admin

from report.models import *

admin.site.register(ReportRequest)
admin.site.register(ReportDefinition)