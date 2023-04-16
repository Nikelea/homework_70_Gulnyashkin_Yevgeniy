from django.urls import path

from api_v1.views import *

urlpatterns = []
accounts_urls = [
    path('api_v1/projects', ProjectListView.as_view(), name='list_projects_api'),
    path('api_v1/projects/<int:pk>', ProjectDetailView.as_view(), name='detail_project_api'),
    path('api_v1/tasks', TaskListView.as_view(), name='list_of_tasks_api'),
    path('api_v1/tasks/<int:pk>', TaskDetailView.as_view(), name='detail_task_api'),
]

urlpatterns += accounts_urls 
