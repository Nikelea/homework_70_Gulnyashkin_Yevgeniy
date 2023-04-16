from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from api_v1.serializers import ProjectSerializer, TaskSerializer
from todoapp.models import TodoProject, TodoTask
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse



# Create your views here.
class ProjectListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = TodoProject.objects.all()
        serializer = ProjectSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class ProjectDetailView(APIView):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(TodoProject, pk=kwargs.get('pk'))
        serializer = ProjectSerializer(object)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        object = get_object_or_404(TodoProject, pk=kwargs.get('pk'))
        serializer = ProjectSerializer(object, data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(TodoProject, pk=kwargs.get('pk'))
        object.delete()
        return Response({'deleted': kwargs.get('pk') })



class TaskListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = TodoTask.objects.all()
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class TaskDetailView(APIView):
    def get(self, request, *args, **kwargs):
        objects = TodoTask.objects.filter(id=kwargs.get('pk'))
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        object = get_object_or_404(TodoTask, pk=kwargs.get('pk'))
        serializer = TaskSerializer(object, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(TodoTask, pk=kwargs.get('pk'))
        object.delete()
        return Response({'deleted': kwargs.get('pk') })
