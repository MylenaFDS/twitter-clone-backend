from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def user_list(request):
    return JsonResponse({"message": "Users endpoint funcionando"})
