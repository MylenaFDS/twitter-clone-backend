from django.http import JsonResponse

def like_list(request):
    return JsonResponse({"message": "Likes endpoint funcionando"})


