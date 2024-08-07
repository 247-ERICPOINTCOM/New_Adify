from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django_countries import countries
from django.forms import TypedChoiceField
from django_countries.fields import CountryField


# In this method it load the PasswordResetForm that will ask for an email address and if it's not in the system show error
# class EmailValidationOnForgotPassword(PasswordResetForm):

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if not User.objects.filter(email__iexact=email, is_active=True).exists():
#             raise ValidationError((f" There is no user registered with this {email} address.."))


def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError((f"{value} is taken."),params = {'value':value})

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(validators = [validate_email])

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

def save(self, commit=True):
         user=super(UserRegisterForm,self)

         if commit:
             user.save()
             return user

# class UserUpdateForm(forms.ModelForm):
# 	email = forms.EmailField(validators = [validate_email])

# 	class Meta:
# 		model = User
# 		fields = ['username', 'first_name', 'last_name',  'email']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise ValidationError((f"{email} is taken."),params = {'value':email})
        return email

# class ProfileUpdateForm(forms.ModelForm):
# 	class Meta:
# 			model = Profile
# 			fields = ['image', 'bio', 'location', 'business']


SELECTED_COUNTRIES = [(country, country_name) for country, country_name in list(countries)]

class ProfileUpdateForm(forms.ModelForm):
    country = TypedChoiceField(choices=SELECTED_COUNTRIES)

    # country = CountryField(blank_label='(select country)').formfield()
    state = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'location', 'country', 'state', 'city', 'business']