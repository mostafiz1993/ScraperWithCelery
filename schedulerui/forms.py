from django import forms

from schedulerui.models import JobParser

SITE_NAME = (
    ( 'https://www.indeed.com/jobs?', 'indeed'),
    ( 'www.simplyhired.com', 'simplydired'),

)
RECURRENCE_LIST = (
    ( '1', 'Daily'),
    ( '2', 'Every Two Day'),
    ( '3', 'Weekly'),
    ( '4', 'Monthly'),
)

class SiteForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.Select(choices=SITE_NAME))
    job_title = forms.CharField(max_length=50)
    location = forms.CharField(max_length=30, required=False)
    company_name = forms.CharField(max_length=50, required=False)
    recurrence = forms.CharField(max_length=5,widget=forms.Select(choices=RECURRENCE_LIST))
    search_start_time  = forms.TimeField( required=False)
    until_stop = forms.BooleanField( required=False)


class JobParserFrom(forms.Form):
    siteName = forms.CharField(max_length=200, required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    siteURL = forms.CharField(max_length=200, required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    searchSyntax = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    jobTitle = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    jobCategory = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    # city = forms.CharField(max_length=200)
    # state = forms.CharField(max_length=200)
    # country = forms.CharField(max_length=200)
    # zipcode = forms.CharField(max_length=200)
    # salaryInfo = forms.CharField(max_length=200)
    # yearsOfExp = forms.CharField(max_length=200)
    # jobPostedDate = forms.CharField(max_length=200)
    # companyName = forms.CharField(max_length=200)
    # companyDomainAddress = forms.CharField(max_length=200)
    # jobURL = forms.CharField(max_length=200)
    # jobDesc = forms.CharField(max_length=200)
    # aboutCompany = forms.CharField(max_length=200)
    # numOfJob = forms.CharField(max_length=200)

class LoginForm(forms.Form):
    userName = forms.EmailField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Password'
        }
    ))

def getJobParserURL():
    #parserURLList = (('hello','hello'),('hi','hi'),('ami','ami'))

    jobParserList = JobParser.objects.all()
    results = []
    for jobParser in jobParserList:
        tempTuple = (jobParser.siteURL,jobParser.siteURL)
        results.append(tempTuple)
    return results

class JobSchedulerForm(forms.Form):
    siteURL = forms.CharField(max_length=200, required=True,widget=forms.Select(choices=getJobParserURL(),attrs={'class': 'form-control'}))
    jobTitle = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    dailyStartTime = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    recurrence = forms.CharField(max_length=5, required=True,widget=forms.Select(choices=RECURRENCE_LIST,attrs={'class':'form-control'}))
    oneTimeProcess = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'checkbox'}))
