from django import forms
from .models import Profile
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm)

class UserForm(forms.Form):
    usuario = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}))
                                    # , widget=forms.PasswordInput()
    # contraseña = forms.CharField(min_length=8, max_length=16)
    contraseña_aux = forms.CharField(min_length=8, max_length=8, label='Contraseña', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)    
    contraseña = forms.CharField(min_length=8, max_length=16, label='', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control aux', 'autocomplete':'off', 'style':'display:none;'}), required=False )    

    def clean(self):
        username = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('contraseña')
        user_username = Profile.objects.filter(username=username).exists()
        if user_username:
            user_aux =  Profile.objects.get(username=username)
            print(str(user_username) +' - ' + str(password) + ' - ' + str(user_aux.contraseña))

        print(str(user_username) +' - ' + str(password))
        if not username:
            print('El usuario no existe!!!')
        user = authenticate(username=username, password=password)
        if not user:
            print('Usuario (django) no autenticado!!!')
            if not user_username:
                raise forms.ValidationError('El usuario no existe!!!')
            else:
                raise forms.ValidationError('¡La contraseña es incorrecta!')
                print('El usuario no existe!!!')
        print('largo: ' + str(len(password)))
        print(str(self.cleaned_data))
        return self.cleaned_data

class RegisterForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    email = forms.EmailField(error_messages={'Correo invalido': 'Verifique que haya ingresado su correo correctamente.'}, widget=forms.TextInput(attrs={'class':'form-control', 'type':'email', 'autocomplete':'off'}), required=True)
    contraseña = forms.CharField(min_length=8, max_length=16, error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    confirmarContra = forms.CharField(min_length=8, max_length=16, label='Confirmar contraseña', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
        

# Formulario para volver a guardar contraseña
class CustomSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'password_notvalid': ("Password must of 8 Character which contain alphanumeric with atleast 1 special charater and 1 uppercase."),
    }
    new_password1 = forms.CharField(
        label=("Nueva Contraseña"),
        widget=forms.PasswordInput,
        # strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Confirmar nueva contraseña"),
        # strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    # def clean_new_password2(self):
    #     password1 = self.cleaned_data.get('new_password1')
    #     password2 = self.cleaned_data.get('new_password2')
    #     if password1 and password2:
    #         if password1 != password2:
    #             raise forms.ValidationError(
    #                 self.error_messages['password_mismatch'],
    #                 code='password_mismatch',
    #             )
    #         # Regix to check the password must contains sepcial char, numbers, char with upeercase and lowercase.
    #         regex = re.compile('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,30})')
    #         if(regex.search(password1) == None):
    #                 raise forms.ValidationError(
    #                 self.error_messages['password_notvalid'],
    #                 code='password_mismatch',
    #             )

        # password_validation.validate_password(password2, self.user)
        # return password2

    def save(self, commit=True):
        print("Iniciando save")
        password = self.cleaned_data["new_password1"]
        # password = self["new_password1"]
        print("Iniciando setPass")
        print('Password: ' + str(password))
        print('Password: ' + password)
        self.user.set_password(password)
        self.user.contraseña = password
        # print("Usuario: " + self.user)
        print("Termine setPass")

        # instance = Profile.objects.get(username=self.user.username)
        # instance = self.user.objects.get(username=self.user.username)
        # print("Instance: " + instance.correo)
        # instance.contraseña = password
        # instance.save()

        if commit:
            self.user.save()
            print("Hice user.save()")
        # email = self.user.email
        # instance = Profile.objects.get(username=self.user.username)
        # if not instance.first_login:
        #     instance.first_login = True
        #     instance.save()
        return self.user        
