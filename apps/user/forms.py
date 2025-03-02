from django import forms
from .models import UserModel

# 新規ユーザー登録フォーム
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

# ログインフォーム
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス", max_length=255)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)