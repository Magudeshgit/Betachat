from .models import BetaUser
from django.contrib.auth.forms import UserCreationForm

class MakeUser(UserCreationForm):
    class Meta:
        model = BetaUser
        fields = ['username','email','password1','password2']

class LogUser(UserCreationForm):
    class Meta:
        model = BetaUser
        fields = ['username','password']