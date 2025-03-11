from django.db import models

class Countdown(models.Model):
    target_time = models.BigIntegerField()  # Store Unix timestamp as a big integer

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)

class Session(models.Model):
    session_name = models.CharField(max_length=150, unique=True)
    users = models.ManyToManyField(User)
    target_time = models.BigIntegerField(default=0)
    session_User_Questions = models.ManyToManyField('SessionUserQuestions')
    round = models.IntegerField(default=1)

class Question(models.Model):
    question_text = models.TextField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    code = models.TextField()
    session_user_questions = models.ManyToManyField('SessionUserQuestions')

class SessionUserQuestions(models.Model):
    current_session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latest_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='latest_question')
    new_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='new_question', null=True)
