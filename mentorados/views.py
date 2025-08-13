from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Mentorados,Navigators
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def mentorados(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'GET':
        navigators = Navigators.objects.filter(users=request.user)
        return render(request, 'mentorados.html', {
            'estagios': Mentorados.estagio_choices,
            'navigators': navigators
        })

    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        estagio = request.POST.get('estagio')
        navigator = request.POST.get('navigator')

        # Verifica se os campos obrigatórios foram preenchidos
        if not nome or not estagio or not navigator:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios.')
            return redirect('mentorados')

        mentorado = Mentorados(
            nome=nome,
            foto=foto,
            estagio=estagio,
            navigator_id=navigator,
            user=request.user
        )
        mentorado.save()

        messages.add_message(request, constants.SUCCESS, 'Mentorado cadastrado com sucesso!')
        return redirect('mentorados')