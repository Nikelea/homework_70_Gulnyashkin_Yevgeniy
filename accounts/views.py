from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from accounts.forms import*
from django.contrib import messages
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index_list')
            else:
                context['has_error'] = True
        return render(request, 'accounts/login.html', context=context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index_list')

class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, avatar='default.png')
            login(request, user)
            return redirect('index_list')
        else:
            form = UserCreationForm(data=request.POST)
        return render(request, self.template_name, context={'form': form})



class UserDetailView(PermissionRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'
    permission_required = 'auth.view_user'
    paginate_related_by = 2
    paginate_related_orphans = 0

    def has_permission(self):
        return (
        self.get_object().pk == self.request.user.pk or
        super().has_permission() or
        self.request.user.is_superuser
        )

    def get_context_data(self, **kwargs):
        projects = self.object.projects.order_by('begin_at')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UsersListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'user_objs'
    ordering = ('username')
    paginate_by = 6
    permission_required = 'auth.view_user'


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'accounts/user_edit.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.pk})


class ChangePasswordView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.get_success_url())


    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.pk})
