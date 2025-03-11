import random

from django.http import JsonResponse, HttpResponse

from countdown.leetcode import getQuestions
from countdown.models import Countdown, User, Session, SessionUserQuestions, Question  # Import Session model
import json
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

# View to get the current target_time
@csrf_exempt
@csrf_exempt
def get_countdown(request):
    try:
        data = json.loads(request.body)
        session_name = data.get('session_name')

        if not session_name:
            return JsonResponse({'target_time': 0})
        
        if session_name == 0:
            return JsonResponse({'target_time': 0})


        session = Session.objects.get(session_name=session_name)

        if not session.target_time:
            # If no target_time exists, set it to the current UNIX timestamp
            session.target_time = int(now().timestamp())
            session.save()

        return JsonResponse({'target_time': session.target_time})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View to set a new target_time
@csrf_exempt
def set_countdown(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

        data = json.loads(request.body)
        session_name = data.get('session_name')
        target_time = data.get('target_time')

        if not session_name:
            return JsonResponse({'success': True, 'target_time': 0, 'no session_name given': 1})
        
        if session_name == 0:
            return JsonResponse({'success': True, 'target_time': 0, 'no session_name given': 1})

        if not isinstance(target_time, int):
            return JsonResponse({'error': 'Invalid target_time, must be an integer'}, status=400)

        session = Session.objects.get(session_name=session_name)
        session.target_time = target_time
        session.save()

        return JsonResponse({'success': True, 'target_time': session.target_time})

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
                return JsonResponse({'message': 'Session created successfully', 'session_name': session.session_name}, status=200)
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
            session_name = data.get('session_name')
            if session_name:
                session = Session.objects.get(session_name=session_name)
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
            session = Session.objects.get(session_name=session_name)
            player_amount = SessionUserQuestions.objects.filter(current_session=session.id).count()
            if session_name:
                session = Session.objects.get(session_name=session_name)
                session.round = session.round + 1
                session.save()
                users_in_session = list(session.users.values_list('username', flat=True))
                questions = Question.objects.filter(session=session)

                if session.round == 1:
                    questions = getQuestions(int(player_amount))

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
                            latest_question=q,
                            new_question=q
                        )

                        i+=1

                    session.busy = True
                    session.save()

                    return JsonResponse({'message': 'Session started successfully'}, status=200)

                else:
                    # scramble the questions

                    questions = Question.objects.filter(session=session)
                    questions_data = [
                        {
                            'question_text': question.question_text,
                            'code': question.code,
                            'question_id': question.id
                        }
                        for question in questions
                    ]
                    original_questions_data = questions_data.copy()

                    derangement = False
                    while not derangement:
                        derangement = True
                        random.shuffle(questions_data)
                        for i in range(len(questions_data)):
                            if questions_data[i]['question_id'] == original_questions_data[i]['question_id']:
                                derangement = False
                                break

                    i = 0
                    while i < len(users_in_session):
                        for j in range(len(questions_data)):
                            if i >= len(users_in_session):
                                break
                            q = Question.objects.get(id=questions_data[j]['question_id'])
                            session_user_question = SessionUserQuestions.objects.get(
                                current_session=session,
                                user=User.objects.get(username=users_in_session[i])
                            )
                            session_user_question.latest_question = session_user_question.new_question
                            session_user_question.new_question = q
                            session_user_question.save()
                            i += 1

                    return JsonResponse({'message': 'Session started successfully'}, status=200)

            else:
                return JsonResponse({'error': 'Session Name is required'}, status=400)
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
                        'question_id': latest_question.id,
                        'round': session.round
                    }, status=200)
                else:
                    return JsonResponse({
                        'code': latest_question.code,
                        'question_id': latest_question.id,
                        'round': session.round
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
            session_name = data.get('session_name')
            user_name = data.get('user_name')
            code = data.get('code')

            session = Session.objects.get(session_name=session_name)
            user = User.objects.get(username=user_name)

            question_id = SessionUserQuestions.objects.filter(current_session=session, user=user).first().new_question.id

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


@csrf_exempt
def get_current_questions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')

            if session_id:
                session = Session.objects.get(id=session_id)
                questions = Question.objects.filter(session=session)
                questions_data = [
                    {
                        'code': question.code,
                        'question_id': question.id
                    }
                    for question in questions
                ]
                return JsonResponse({'questions': questions_data}, status=200)
            else:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def remove_questions_from_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            question_ids = data.get('question_ids', [])

            if session_id and question_ids:
                session = Session.objects.get(id=session_id)
                questions = Question.objects.filter(id__in=question_ids, session=session)
                questions.delete()
                return JsonResponse({'message': 'Questions removed successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Session ID and question IDs are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)