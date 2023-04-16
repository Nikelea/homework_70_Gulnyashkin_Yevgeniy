from django.urls import path
from todoapp.views.task_views import *
from todoapp.views.project_views import *

urlpatterns = []
tasks_urls = [
    path('', IndexListView.as_view(), name='index_list'),
    path('tasks', TaskListView.as_view(), name='tasks_list'),
    path('create', TaskCreateView.as_view(), name='task_create'),
    path('projects/<int:pk>/task_create', ProjectTaskCreateView.as_view(), name='project_task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit', TaskEditView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('<str:filter>/', FilterListView.as_view(), name='task_filter_list'),
    path('search', SearchView.as_view(), name='search_task')
]
project_urls = [
    path('projects', ProjectsListView.as_view(), name='projects_list'),
    path('project/create', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project<int:pk>/edit', ProjectEditView.as_view(), name='project_edit'),
    path('project<int:pk>/delete', ProjectDeleteView.as_view(), name='project_delete'),
     path('project<int:pk>/users_edit', ProjectUsersEdit.as_view(), name='project_users_edit'),
]
urlpatterns += tasks_urls 
urlpatterns += project_urls