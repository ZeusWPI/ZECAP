from django.http import JsonResponse, HttpResponse

from countdown.leetcode import getQuestions
from countdown.models import Countdown, User, Session, Question  # Import Session model
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

@csrf_exempt
def save_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            if username:
                User.objects.create(username=username)
                return JsonResponse({'message': 'Username saved successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Username is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_usernames(request):
    if request.method == 'GET':
        try:
            usernames = User.objects.values_list('username', flat=True)
            return JsonResponse({'usernames': list(usernames)}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def create_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_name = data.get('session_name')
            if session_name:
                session = Session.objects.create(session_name=session_name)
                return JsonResponse({'message': 'Session created successfully', 'session_id': session.id}, status=200)
            else:
                return JsonResponse({'error': 'Session name is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def list_sessions(request):
    if request.method == 'GET':
        try:
            sessions = Session.objects.values_list('session_name', flat=True)
            return JsonResponse({'sessions': list(sessions)}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def join_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            username = data.get('username')
            if session_id and username:
                session = Session.objects.get(id=session_id)
                user = User.objects.get(username=username)
                session.users.add(user)
                return JsonResponse({'message': 'User joined session successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID and username are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def leave_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            username = data.get('username')
            if session_id and username:
                session = Session.objects.get(id=session_id)
                user = User.objects.get(username=username)
                session.users.remove(user)
                return JsonResponse({'message': 'User left session successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID and username are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def remove_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            if session_id:
                session = Session.objects.get(id=session_id)
                session.delete()
                return JsonResponse({'message': 'Session removed successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def index(request):
    return HttpResponse("Countdown app is working!")

def countdown(request):
    # Your logic for the countdown view
    return render(request, 'countdown.html')


@csrf_exempt
def start_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            player_amount = data.get('player_amount', 1)

            if session_id:
                session = Session.objects.get(id=session_id)
                questions = getQuestions(player_amount)

                for question_text, code in questions:
                    Question.objects.create(
                        question_text=question_text,
                        session=session,
                        code=code
                    )

                session.busy = True
                session.save()



                return JsonResponse({'message': 'Session started successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
