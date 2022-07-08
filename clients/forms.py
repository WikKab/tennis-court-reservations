from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm
from django.forms import ModelForm
from clients.models import Profile
from django import forms


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name
    class Meta:

#     username = forms.CharField(max_length=150,  )
    # email = forms.EmailField()
    #
    # < label
    # for ="id_username" > Nazwa użytkownika:< / label >
    # < input
    # type = "text"
    # name = "username"
    # value = "qwerty"
    # maxlength = "150"
    # autocapitalize = "none"
    # autocomplete = "username"
    # required
    # id = "id_username" >
    #
    # < span
    #
    # class ="helptext" > Wymagana.150
    # lub mniej znaków.Jedynie litery, cyfry i @ /./ + / - / _.< / span >