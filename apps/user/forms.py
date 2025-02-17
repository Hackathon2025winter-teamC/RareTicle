from django import forms
from .models import UserModel

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("パスワードが違います")
        return cleaned_data