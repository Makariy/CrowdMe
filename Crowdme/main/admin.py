from django.contrib import admin
from .models import Project

# Register your models here.


class ProjectAdminModel(admin.ModelAdmin):
    list_display = ('title', 'cost', 'funded', 'days_left', 'is_new', 'published_date')
    list_display_links = ('title', 'cost', 'funded', 'days_left', 'is_new', 'published_date')
    ordering = ['-published_date', 'title']


admin.site.register(Project, ProjectAdminModel)

