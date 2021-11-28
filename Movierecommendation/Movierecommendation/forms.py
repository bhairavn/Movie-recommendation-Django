from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     """
#     A form that creates a user, with no privileges, from the given email and
#     password.
#     """
#     def __init__(self, *args, **kargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kargs)
#         del self.fields['email']

#     class Meta:
#         model = CustomUser
#         # fields = ("email",)
#         fields=['firstname','lastname','phone','gender','genre','email','password1']


# # class CustomUserChangeForm(UserChangeForm):
# #     """A form for updating users. Includes all the fields on
# #     the user, but replaces the password field with admin's
# #     password hash display field.
# #     """

# #     def __init__(self, *args, **kargs):
# #         super(CustomUserChangeForm, self).__init__(*args, **kargs)
# #         del self.fields['email']
# #     class Meta:
# #         model = CustomUser
# # 		fields = ''

class UserRegisterForm(forms.ModelForm):
    # first_name = forms.CharField(label='firstname', max_length=10)
    # last_name = forms.CharField(label='lastname', max_length=10)
    # phone = forms.CharField(label='phone', max_length=15)
    # gender = forms.CharField(label='gender', max_length=8)
    # gendre = forms.CharField(label='genre', max_length=100)
    # email = forms.EmailField()
    # password = forms.CharField(
    #     label='password', max_length=100, widget=forms.PasswordInput)
    class Meta:
        model=UserProfile
        # fields = "__all__"
        fields=['firstname','lastname','phone','gender','genre','email','password']
