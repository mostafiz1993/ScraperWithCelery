from django import forms

from .models import JobInfo
from .models import Calcu

class UserForm(forms.ModelForm):
    class Meta:
        model = Calcu
        fields = [
            "n",
        ]


class JobForm(forms.ModelForm):
    class Meta:
        model = JobInfo
        fields = [
            "jobName"
        ]