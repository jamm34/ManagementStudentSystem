from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd



def ShowLoginPage(request):
    return render(request, 'login_page.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Metodo no permitido</h2>')

    user = EmailBackEnd.authenticate(
        request,
        username=request.POST.get('email'),
        password=request.POST.get('password'),
    )
    if user is not None:
        login(request, user)
        if user.user_type == '1':
            return HttpResponseRedirect('admin_home')
        if user.user_type == '2':
            return HttpResponseRedirect(reverse('staff_home'))
        if user.user_type == '3':
            return HttpResponseRedirect(reverse('student_home'))

    messages.error(request, 'Credenciales de inicio de sesion invalidas')
    return HttpResponseRedirect('/')


def GetUserDetails(request):
    if request.user is not None:
        return HttpResponse(
            'Usuario: ' + request.user.email + ' | tipo de usuario: ' + request.user.user_type
        )

    return HttpResponse('Por favor, inicia sesion primero')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')



