from django import forms
from .models import Employee, User

class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'password', widget = forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'comfirm password', widget = forms.PasswordInput
    )

    # since inheritance from modelform
    # i can use the model to declare the fields

    class Meta:
        model=User
        fields = ('username','first_name','email','password')

        # overiding a inbuilt method to check the
        # password = confirm password
        # clean_<fieldname>

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password']!=cd['password']:
                raise forms.ValidationError('password does not match')
            
            return cd['password2']