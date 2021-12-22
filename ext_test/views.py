import random

from django.shortcuts import render

from django.views.generic import View
from .psychic import new_psychic


# Create your views here.
class StartView(View):

    @staticmethod
    def get(request):
        template_name = 'start.html'
        context = {}
        return render(request, template_name, context=context)


class PsychicsResultView(View):

    @staticmethod
    def get(request):
        template_name = 'ps_result.html'
        session = request.session
        if not session.get('psychics'):
            session['psychics'] = [new_psychic(f'Name{number}') for number in range(5)]
        answers = []
        for psychic in session['psychics']:
            psychic['last_answer'] = random.randrange(10, 100)
            psychic['answers'].append(psychic['last_answer'])
            answers.append({'name': psychic['name'], 'answer': psychic['last_answer']})
        session.modified = True
        context = {'answers': answers}
        return render(request, template_name, context=context)


class TotalView(View):

    @staticmethod
    def get(request):
        template_name = 'total.html'
        session = request.session
        answer = request.GET.get('answer', None)
        try:
            answer_int = int(answer)
        except ValueError as e:
            return render(request, 'error.html', context={'error': e})
        if not session.get('numbers'):
            session['numbers'] = []
        session['numbers'].append(answer_int)
        for psychic in session['psychics']:
            if psychic['last_answer'] == answer_int:
                psychic['level'] += 1
            else:
                psychic['level'] -= 1
        session.modified = True
        context = {'answer': answer_int, 'numbers': session['numbers'], 'psychics': session['psychics']}
        return render(request, template_name, context=context)
