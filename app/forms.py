from django import forms

from app.models import User, Comment


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError('password error')
        except User.DoesNotExist:
            raise forms.ValidationError('email not found')
        return password


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=55)
    email = forms.EmailField()
    password = forms.CharField(max_length=55)
    confirm_password = forms.CharField(max_length=55)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password error')
        return password


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


