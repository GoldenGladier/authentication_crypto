from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, RegisterForm
from .models import Profile
from django.shortcuts import redirect, reverse

from django.contrib.auth.decorators import login_required

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

# PASSWORD RESET
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from users.models import Profile
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def password_reset_request(request):
    if request.method == "POST": 
        password_reset_form = PasswordResetForm(request.POST) 
        if password_reset_form.is_valid(): 
            data = password_reset_form.cleaned_data['email'] 
            associated_users = Profile.objects.filter(Q(correo=data)) 
            if associated_users.exists(): 
                for user in associated_users: 
 					    # subject = "Password Reset Requested" 
                        email_template_name = "password/password_reset_email.txt"
                        c = { 
                        "email":user.correo, 
                        'domain':'omaraguirre.pythonanywhere.com', 
                        'site_name': 'Website', 
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)), 
                        "user": user, 
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        } 
                        email = render_to_string(email_template_name, c)
                    
                    # ----------------
                        from_address = 'doncelomar@gmail.com'

                        to_address = user.correo

                        message = MIMEMultipart('Foobar')

                        # epos_liggaam['Subject'] = 'Foobar'
                        message['Subject'] = "Solicitud de restablecimiento de contraseña."

                        message['From'] = from_address

                        message['To'] = to_address

                        content = MIMEText(email, 'plain')
                        # content = MIMEText('Some message content', 'plain')

                        message.attach(content)

                        mail = smtplib.SMTP('smtp.gmail.com', 587)

                        mail.ehlo()

                        mail.starttls()
                        try: 
                            mail.login(from_address, 'H0MER0poter')
                            mail.sendmail(from_address,to_address, message.as_string())
                            mail.close()  
                        except BadHeaderError: 
                            return HttpResponse('Invalid header found.') 
                        return redirect ("/password_reset/done/")                          

                                          
                    # ----------------
                    # subject = "Password Reset Requested"    
                    
    password_reset_form = PasswordResetForm() 
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})                                  

# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = Profile.objects.filter(Q(correo=data)) # ===========================================
# 			if associated_users.exists():
# 				for user in associated_users:
#                     # ----------------
#                     # from_address = "johndoe@gmail.com"
#                     # subject = "Password Reset Requested"
#                     # ----------------
# 					subject = "Password Reset Requested"
# 					email_template_name = "password/password_reset_email.txt"
# 					c = {
# 					"email":user.correo,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.correo], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})                    

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['contraseña']
            user = Profile.objects.get(username=username)
            print("Contraseña ingresada: " + password)
            print("Contraseña db: " + user.contraseña)
            if(user.contraseña == password):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse('home-view'))
        else:
            print("Formulario (form) login invalido")
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


from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from .forms import CustomSetPasswordForm

def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='password/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=CustomSetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    # UserModel = get_user_model()
    UserModel = Profile
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        print('UID: ' + uid)
        user = UserModel._default_manager.get(pk=uid)        
        # print('user: ' + user)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
        print(str(ValueError) + ' tTType: ' + str(TypeError))

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = ('Enter new password')
        if request.method == 'POST':
            print("Recibi el POST")
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                print("Termine el save")
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        print('user: ' + str(user))
        print("Link de reset invalido :c")
        validlink = False
        form = None
        title = ('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)            