from django.http import JsonResponse
from .models import Follow

def follow_list(request):
    return JsonResponse({"message": "Follow endpoint funcionando"})
