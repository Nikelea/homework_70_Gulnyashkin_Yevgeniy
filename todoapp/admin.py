from django.contrib import admin
from django.db.models import fields
from todoapp.models import *

# Register your models here.
class TodoTask_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status']
    fields = ['title','description', 'status', 'updated_at', 'created_at']
    readonly_fields = ['updated_at', 'created_at']

# admin.site.register(TodoTask, TodoTask_Admin)
admin.site.register(TodoTask)
admin.site.register(TodoProject)

class TaskType_Admin(admin.ModelAdmin):
    list_display = ['id', 'title']
    fields = ['title']

admin.site.register(TaskType, TaskType_Admin)

class TaskStatus_Admin(admin.ModelAdmin):
    list_display = ['id', 'title']
    fields = ['title']

admin.site.register(TaskStatus, TaskStatus_Admin)

