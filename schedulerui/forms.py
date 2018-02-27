from django import forms

SITE_NAME = (
    ( 'https://www.indeed.com/jobs?', 'indeed'),
    ( 'www.simplyhired.com', 'simplydired'),

)
RECURRENCE_LIST = (
    ( '1' , 'DAILY'),
    ( '1', 'WEEKLY'),
)

class SiteForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.Select(choices=SITE_NAME))
    job_title = forms.CharField(max_length=50)
    location = forms.CharField(max_length=30)
    company_name = forms.CharField(max_length=50)
    recurrence = forms.CharField(max_length=5,widget=forms.Select(choices=RECURRENCE_LIST))
    search_start_time  = forms.TimeField()
    until_stop = forms.BooleanField()