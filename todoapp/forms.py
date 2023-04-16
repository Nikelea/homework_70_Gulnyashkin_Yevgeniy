from dataclasses import field
from django import forms
from .models import TaskStatus, TaskType,TodoProject, TodoTask 


class ProjectForm(forms.ModelForm):

    class Meta:
        model = TodoProject
        exclude =['is_deleted', 'users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'users': forms.CheckboxSelectMultiple(attrs={'type': 'hidden'}),
            'begin_at':forms.DateInput(format=('%d-%m-%Y'),attrs={'type': 'date', 'class': 'form-control'}),
            'end_at':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
            }


class TaskForm(forms.ModelForm):

    class Meta:
        model = TodoTask
        exclude =['is_deleted']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'types': forms.CheckboxSelectMultiple(),
            'status': forms.RadioSelect(),
            'project': forms.RadioSelect()
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")
    
class ProjectUsersForm(forms.ModelForm):

    class Meta:
        model = TodoProject
        fields =['users']
        widgets = {
            'users': forms.CheckboxSelectMultiple(),
            }
