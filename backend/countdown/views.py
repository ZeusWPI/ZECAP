from django.http import JsonResponse, HttpResponse

from countdown.leetcode import getQuestions
from countdown.models import Countdown, User, Session, Question, SessionUserQuestions  # Import Session model
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
            sessions = Session.objects.all()
            session_map = {}
            for session in sessions:
                usernames = session.users.values_list('username', flat=True)
                session_map[session.session_name] = list(usernames)
            return JsonResponse({'sessions': list(session_map.keys()), 'sessionUsers': session_map}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def join_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_name = data.get('session_name')
            username = data.get('username')
            if session_name and username:
                session = Session.objects.get(session_name=session_name)
                user = User.objects.get(username=username)
                session.users.add(user)
                return JsonResponse({'message': 'User joined session successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session name and username are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def leave_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_name = data.get('session_name')
            username = data.get('username')
            if session_name and username:
                session = Session.objects.get(session_name=session_name)
                user = User.objects.get(username=username)
                session.users.remove(user)
                return JsonResponse({'message': 'User left session successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session name and username are required'}, status=400)
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
            session_name = data.get('session_name')
            player_amount = data.get('player_amount', 1)

            if session_name:
                session = Session.objects.get(session_name=session_name)
                questions = getQuestions(int(player_amount))

                users_in_session = list(session.users.values_list('username', flat=True))

                i = 0

                for question_text, code in questions:
                    q = Question.objects.create(
                        question_text=question_text,
                        session=session,
                        code=code
                    )

                    SessionUserQuestions.objects.create(
                        current_session=session,
                        user=User.objects.get(username=users_in_session[i]),
                        latest_question=q
                    )

                    i+=1

                session.busy = True
                session.save()



                return JsonResponse({'message': 'Session started successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def get_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_name = data.get('session_name')
            username = data.get('username')

            if session_name and username:
                session = Session.objects.get(session_name=session_name)
                user = User.objects.get(username=username)
                session_user_question = SessionUserQuestions.objects.get(current_session=session, user=user)
                latest_question = session_user_question.latest_question

                if session.round == 1:
                    return JsonResponse({
                        'question_text': latest_question.question_text,
                        'code': latest_question.code,
                        'question_id': latest_question.id
                    }, status=200)
                else:
                    return JsonResponse({
                        'code': latest_question.code,
                        'question_id': latest_question.id
                    }, status=200)
            else:
                return JsonResponse({'error': 'Session name and username are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def submit_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            code = data.get('code')

            if question_id and code:
                question = Question.objects.get(id=question_id)
                question.code = code
                question.save()
                return JsonResponse({'message': 'Code updated successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Question ID and code are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)