from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, RegisterForm
from .models import Profile
from django.shortcuts import redirect, reverse

from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['contraseña']
            user = Profile.objects.get(username=username)
            print("Contraseña ingresada: " + user.contraseña)
            print("Contraseña db: " + password)
            if(user.contraseña == password):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse('home-view'))
        else:
            print("Formulario login invalido")
    else:
        form = UserForm()
    return render(request, 'profile/login.html', {'form': form})
    

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['nombre']
            surname = form.cleaned_data['apellido']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['contraseña']
                                    # email de la db = this.email
            print("Nombre: " + name)
            print("Apellido: " + surname)
            print("Usuario: " + username)
            print("Email: " + email)
            print("Contraseña: " + password)

            user = Profile.objects.filter(username = username).exists()
            if user is False or user is None:
                print("NO EXISTE")
                user = Profile(username = username, correo = email, contraseña = password)
                user.set_password(password)
                user.save()
                # user = form.save(commit=False)
                # form.save()                
                print("USUARIO NUEVO REGISTRADO")
                login(request, user)
                return redirect(reverse('home-view'))
        else:
            print("No es valido")

    else:
        form = RegisterForm()
    # context = {'form': form}
    return render(request, 'profile/register.html', {'form': form})

@login_required
def home_view(request):
    if request.method == 'GET':
        return render(request, 'page/home.html')    

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login-view'))

import json
from django.http import HttpResponse
def username_validate_view(request):
    print("RECIBI PETICION")
    if request.method == 'POST':
        print("TIPO POST: " +  request.POST['username'])

        user = Profile.objects.filter(username = request.POST['username']).exists()
        if user is False or user is None:   
            return HttpResponse(json.dumps({'valido': True}), content_type='application/javascript')
        else:
            return HttpResponse(json.dumps({'valido': False}), content_type='application/javascript')     
            # try:
            #     Profile.objects.filter(username = request.POST['username'])
            #     # Profile.objects.get(id=request.POST['username']) # el mismo string que pusiste en la data del AJAX
            #     return HttpResponse(json.dumps({'valido': False}), content_type='application/javascript')
            # except Profile.DoesNotExist:
            #     return HttpResponse(json.dumps({'valido': True}), content_type='application/javascript')