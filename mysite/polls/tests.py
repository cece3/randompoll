import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    def setUp(self):
        q1 = Question.objects.create(question_text='Who is the best dog?', pub_date=timezone.now())
        q1.choice_set.create(choice_text='Baylee', votes=0)
        q1.choice_set.create(choice_text='Lulu', votes=0)
        q1.choice_set.create(choice_text='Bubba', votes=0)
        q1.choice_set.create(choice_text='Sissy', votes=0)

        q2 = Question.objects.create(question_text="What's up?", pub_date=timezone.now())
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

