from django.shortcuts import  reverse, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from todoapp.forms import ProjectForm, ProjectUsersForm
from todoapp.models import TodoTask, TodoProject
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

# Create your views here.
class IndexListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/main_template.html'
    model = TodoProject
    context_object_name = 'projects'
    ordering = ('begin_at')
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'tasks': TodoTask.objects.filter(project__users__username=self.request.user)
        })
        return context


class ProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'projects/main_template.html'
    model = TodoProject
    context_object_name = 'projects'
    ordering = ('begin_at')
    paginate_by = 4
    

class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'projects/detail_template.html'
    model = TodoProject
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        tasks = TodoTask.objects.filter(project__users__username=self.request.user)
        context = super().get_context_data(**kwargs)
        context.update({ 'tasks': tasks.filter(project__pk=self.object.pk)
        })
        return context


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = TodoProject
    template_name = 'projects/create_template.html'
    form_class = ProjectForm
    permission_required = 'todoapp.add_todoproject'

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return redirect('project_detail', pk=project.pk)
    
    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectEditView(PermissionRequiredMixin, UpdateView):
    model = TodoProject
    template_name = 'projects/edit_template.html'
    form_class = ProjectForm
    permission_required = 'todoapp.change_todoproject'
    

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = TodoProject
    permission_required = 'todoapp.delete_todoproject'

    def get_success_url(self):
        return reverse('projects_list')


class ProjectUsersEdit(PermissionRequiredMixin, UpdateView):
    model = TodoProject
    template_name = 'projects/users_edit_template.html'
    form_class = ProjectUsersForm
    permission_required = 'todoapp.can_edit_users'

    def has_permission(self):
        return (
        self.get_object().users.filter(username=self.request.user) and
        super().has_permission() or
        self.request.user.is_superuser
        )


    def form_valid(self, form):       
        project = form.save(commit=False)
        if project.users.all():
            for user in project.users.all():
                if user == self.request.user:
                    if not form.cleaned_data['users'].filter(username=self.request.user):
                        messages.error(self.request, 'Нельзя удалить самого себя из проекта!')
                        return redirect('project_users_edit', pk=project.pk)
        project.save()
        super().form_valid(form)
        return redirect('project_detail', pk=project.pk)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})
