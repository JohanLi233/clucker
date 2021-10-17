from django import forms
from .models import User
from django.core.validators import RegexValidator

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets = {'bio': forms.Textarea() }

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase character and a number.'
        )]
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password!= confirm_password:
            self.add_error('confirm_password', 'Confirmation does match password.')

    def save(self):
         super().save(commit=False)
         user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            password=self.cleaned_data.get('new_password'),
         )
         return user
