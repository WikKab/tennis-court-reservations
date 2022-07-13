from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm
from django.forms import ModelForm
from clients.models import Profile
from django import forms


class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': ' form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': ' form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': ' form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': ' form-control'}))
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': ' form-control'}))
    # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': ' form-control'}))

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )