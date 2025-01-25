from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    age=forms.IntegerField()
    gender_choices = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    password=forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput,required=True)

    class Meta:
        model=User
        fields=['username','email','first_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different username.")
        return username

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password!=confirm_password:
            raise forms.ValidationError('passwords does not match')
        return cleaned_data
