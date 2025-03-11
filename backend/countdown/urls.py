from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/', views.get_countdown, name='get_countdown'),
    path('set/', views.set_countdown, name='set_countdown'),
    path('saveUsername/', views.save_username, name='save_username'),
    path('getAllUsernames/', views.get_usernames, name='get_usernames'),
    path('listSessions/', views.list_sessions, name='list_sessions'),
    path('joinSession/', views.join_session, name='join_session'),
    path('removeSession/', views.remove_session, name='remove_session'),
    path('leaveSession/', views.leave_session, name='leave_session'),
    path('createSession/', views.create_session, name='create_session'),

    path('startSession/', views.start_session, name='start_session'),

    path('getQuestion/', views.get_question, name='get_question'),
]
