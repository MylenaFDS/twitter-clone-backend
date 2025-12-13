from django.http import JsonResponse

def comment_list(request):
    return JsonResponse({"message": "Comments endpoint funcionando"})
