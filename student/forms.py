from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['student', 'category','description','upload','urgency','date','time']