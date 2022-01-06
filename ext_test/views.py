from django.shortcuts import render
from django.views.generic import View

from .psychic import Psychic, Player


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
            psychics = [Psychic(f'Name{number}') for number in range(5)]
            session['psychics'] = psychics
        else:
            psychics = session['psychics']
        answers = [{'name': psychic.name, 'answer': psychic.get_answer()} for psychic in psychics]
        session.modified = True
        context = {'answers': answers}
        return render(request, template_name, context=context)


class TotalView(View):

    @staticmethod
    def get(request):
        template_name = 'total.html'
        session = request.session
        if not session.get('player'):
            player = Player()
            session['player'] = player
        else:
            player = session['player']
        answer = request.GET.get('answer', None)
        try:
            answer_int = int(answer)
            if not (9 < answer_int < 100):
                raise ValueError('The number must be greater then 9 and less then 100')
        except ValueError as e:
            player.numbers.append(answer)
            session.modified = True
            return render(request, 'error.html', context={'error': e})
        player.numbers.append(answer_int)
        psychics = session['psychics']
        for psychic in psychics:
            if psychic.answers[-1] == answer_int:
                psychic.change_level(True)
            else:
                psychic.change_level(False)
        session.modified = True
        context = {'answer': answer_int, 'numbers': player.numbers, 'psychics': psychics}
        return render(request, template_name, context=context)
