from django.shortcuts import reverse, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from todoapp.forms import TaskForm, SearchForm
from todoapp.models import TodoTask, TodoProject
from todoapp.service import SearchEngine
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class TaskListView(PermissionRequiredMixin, ListView):
    template_name = 'tasks/main_only_tasks_template.html'
    model = TodoTask
    context_object_name = 'tasks'
    ordering = ('updated_at')
    paginate_by = 6
    permission_required = 'todoapp.view_todotask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'tasks': TodoTask.objects.filter(project__users__username=self.request.user)
        })
        return context


class SearchView(LoginRequiredMixin, SearchEngine):
    template_name = 'tasks/main_template.html'
    model = TodoTask
    context_object_name = 'tasks'
    ordering = ('updated_at')
    paginate_by = 6
    search_form = SearchForm
    search_fields = {
        'title': 'icontains',
        'description': 'icontains',
        'status__title': 'iexact'
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'projects': TodoProject.objects.filter(self.get_query())
        })
        return context


class FilterListView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/main_template.html'

    def filter_list(self, filter):
        if TodoTask.objects.filter(types__title__iexact=filter):
            return TodoTask.objects.filter(types__title__iexact=filter)
        else:
            return TodoTask.objects.filter(status__title__iexact=filter)

    def get_context_data(self, **kwargs):
        kwargs['tasks'] = self.filter_list(self.kwargs.get('filter'))
        context = super().get_context_data(**kwargs)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/detail_template.html'
    model = TodoTask
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'project': get_object_or_404(TodoProject.objects.filter(pk=self.get_object().project.pk))
        })
        return context


class TaskCreateView(PermissionRequiredMixin,CreateView):
    model = TodoTask
    template_name = 'tasks/create_template.html'
    form_class = TaskForm
    permission_required = 'todoapp.add_todotask'
    
    def has_permission(self):
        return (
        self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class ProjectTaskCreateView(PermissionRequiredMixin, CreateView):
    model = TodoTask
    template_name = 'tasks/create_template.html'
    form_class = TaskForm
    permission_required = 'todoapp.add_todotask'

    def has_permission(self):
        project = get_object_or_404(TodoProject, pk=self.kwargs.get('pk'))
        return (
        project.users.filter(username=self.request.user) and
        super().has_permission() or
        self.request.user.is_superuser
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})


class TaskEditView(PermissionRequiredMixin, UpdateView):
    model = TodoTask
    template_name = 'tasks/edit_template.html'
    form_class = TaskForm
    permission_required = 'todoapp.change_todotask'

    def has_permission(self):
        project = get_object_or_404(TodoProject, pk=self.get_object().project.pk)
        return (
        project.users.filter(username=self.request.user) and
        super().has_permission() or
        self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = TodoTask
    permission_required = 'todoapp.delete_todotask'

    def get_success_url(self):
        return reverse('tasks_list')

    def has_permission(self):
        project = get_object_or_404(TodoProject, pk=self.get_object().project.pk)
        return (
        project.users.filter(username=self.request.user) and
        super().has_permission() or
        self.request.user.is_superuser
        )
