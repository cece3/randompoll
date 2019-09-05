from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic

from .models import Choice,Question

def index(request):
    try:
        if 'answered_questions' not in request.session: 
            print('It is None')
            question = Question.objects.order_by('?').first()
        else:
            print ("It is defined and has a value: ")
            answered_questions = request.session['answered_questions']
            print (answered_questions)
            question = Question.objects.exclude(id__in=answered_questions).order_by('?').first()
            if not question:
                #if there are not any other questions remaining, delete the session and start over
                del request.session['answered_questions']
                #question = Question.objects.order_by('?').first()
                return HttpResponseRedirect('finished')
        return render(request,'polls/detail.html', { 'question': question })
    except(NameError):
        print ("other error")

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def finished(Request):
    return HttpResponse('Congratulations, you have answered all of the questions in this poll!<br/><br/><a href="/polls"HttpResponse>Start over</a>')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        if not 'answered_questions' in request.session or not request.session['answered_questions']:
            request.session['answered_questions'] = [question_id]
        else:
            answered_questions = request.session['answered_questions']
            if not int(question_id) in answered_questions:
                answered_questions.append(question_id)
                request.session['answered_questions'] = answered_questions
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
