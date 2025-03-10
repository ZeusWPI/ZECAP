from django.http import JsonResponse, HttpResponse
from countdown.models import Countdown
import json
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

# View to get the current target_time
def get_countdown(request):
    try:
        countdown = Countdown.objects.first()  # Get the first countdown object
        if not countdown:
            # If no countdown exists, create one with the current UNIX timestamp
            countdown = Countdown.objects.create(target_time=int(now().timestamp()))

        return JsonResponse({'target_time': countdown.target_time})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View to set a new target_time
@csrf_exempt
def set_countdown(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

        data = json.loads(request.body)
        target_time = data.get('target_time')

        if not isinstance(target_time, int):
            return JsonResponse({'error': 'Invalid target_time, must be an integer'}, status=400)

        countdown = Countdown.objects.first()

        if countdown:
            countdown.target_time = target_time
        else:
            countdown = Countdown.objects.create(target_time=target_time)

        countdown.save()
        return JsonResponse({'success': True, 'target_time': countdown.target_time})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def index(request):
    return HttpResponse("Countdown app is working!")

def countdown(request):
    # Your logic for the countdown view
    return render(request, 'countdown.html')
