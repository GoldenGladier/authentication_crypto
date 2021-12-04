from django import forms
from .models import Profile
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.Form):
    usuario = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}))
                                    # , widget=forms.PasswordInput()
    # contraseña = forms.CharField(min_length=8, max_length=16)
    contraseña_aux = forms.CharField(min_length=8, max_length=8, label='Contraseña', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)    
    contraseña = forms.CharField(min_length=8, max_length=16, label='', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control aux', 'autocomplete':'off', 'style':'display:none;', 'maxlength':'8'}), required=False )    

    def clean(self):
        username = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('contraseña')
        user_username = Profile.objects.filter(username=username).exists()
        user = authenticate(username=username, password=password)
        if not user:
            if not user_username:
                raise forms.ValidationError('El usuario no existe!!!')
                print('El usuario no existe!!!')
            else:
                raise forms.ValidationError('¡La contraseña es incorrecta!')
                print('El usuario no existe!!!')
        
        return self.cleaned_data

class RegisterForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    email = forms.EmailField(error_messages={'Correo invalido': 'Verifique que haya ingresado su correo correctamente.'}, widget=forms.TextInput(attrs={'class':'form-control', 'type':'email', 'autocomplete':'off'}), required=True)
    contraseña = forms.CharField(min_length=8, max_length=16, error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
    confirmarContra = forms.CharField(min_length=8, max_length=16, label='Confirmar contraseña', error_messages={'Contraseña invalida': 'La contraseña debe tener mínimo 8 caracteres.'}, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'off'}), required=True)
        