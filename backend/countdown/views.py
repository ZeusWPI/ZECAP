from django.http import JsonResponse, HttpResponse
from countdown.models import Countdown
import json
from django.shortcuts import render

# View to get the current target_time
def get_countdown(request):
    try:
        countdown = Countdown.objects.first()  # Get the first countdown object
        if countdown:
            return JsonResponse({'target_time': countdown.target_time})
        else:
            return JsonResponse({'error': 'Countdown not set'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View to set a new target_time
def set_countdown(request):
    try:
        data = json.loads(request.body)
        target_time = data.get('target_time')
        if target_time is None:
            return JsonResponse({'error': 'No target_time provided'}, status=400)
        
        countdown, created = Countdown.objects.get_or_create(id=1)  # Assuming a single countdown record
        countdown.target_time = target_time
        countdown.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def index(request):
    return HttpResponse("Countdown app is working!")

def countdown(request):
    # Your logic for the countdown view
    return render(request, 'countdown.html')
