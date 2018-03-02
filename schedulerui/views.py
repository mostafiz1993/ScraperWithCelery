# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response, render, redirect
import urllib
from bs4 import BeautifulSoup
import csv
import json
from .forms import *
from .models import *


def index(request):
    return render(request,'index.html')

def addParserJob(request):
    if request.method == "POST":
        form = JobParserFrom(request.POST)
        if form.is_valid():
            siteName = form.cleaned_data['siteName']
            siteURL = form.cleaned_data['siteURL']
            searchSyntax = form.cleaned_data['searchSyntax']
            jobTitle = form.cleaned_data['jobTitle']
            jobCategory= form.cleaned_data['jobCategory']
            location = form.cleaned_data['location']
            jobParser = JobParser.objects.create(siteName=siteName,siteURL=siteURL,searchSyntax=searchSyntax,
                                                 jobTitle=jobTitle,jobCategory=jobCategory,location=location)
            jobParser.save()
            # print(siteName)
            # print(siteURL)
            # print(searchSyntax)
            form = JobParserFrom()
            jobParserListJson = getAllJobParser()
            return render(request, 'newJobParser.html', {"form": form, "jobParserListJson": json.loads(jobParserListJson)})

    else:
        form = JobParserFrom()

    jobParserListJson = getAllJobParser()
    return render(request, 'newJobParser.html', {"form":form, "jobParserListJson": json.loads(jobParserListJson)})

def getAllJobParser():
    jobParserList = JobParser.objects.all()
    results = []
    for jobParser in jobParserList:
        jobParserJson = {}
        jobParserJson['siteName'] = jobParser.siteName
        jobParserJson['siteURL'] = jobParser.siteURL
        jobParserJson['jobTitle'] = jobParser.jobTitle
        jobParserJson['jobId'] = jobParser.id
        jobParserJson['updated'] = jobParser.updated.strftime("%d-%m-%Y")
        results.append(jobParserJson)
    jobParserListJson = json.dumps(results)
    return jobParserListJson

def addJobInScheduler(request):
    return render(request,'jobScheduler.html')

def deleteJobParser(request,jobparserid):
    print(jobparserid)
    jobParser = JobParser.objects.get(pk=jobparserid)
    jobParser.delete()
    return redirect("/home/addparserjob")
    # form = JobParserFrom()
    # jobParserListJson = getAllJobParser()
    # return render(request, 'newJobParser.html', {"form": form, "jobParserListJson": json.loads(jobParserListJson)})


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            site_name = form.cleaned_data['name']
            job_title = form.cleaned_data['job_title']
            location = form.cleaned_data['location']
            company_name = form.cleaned_data['company_name']
            recurrence = form.cleaned_data['recurrence']
            search_start_time = form.cleaned_data['search_start_time']
            create_site_object(site_name,job_title,location,company_name,recurrence,search_start_time)
            f = {'q': job_title, 'I': location}
            print(urllib.urlencode(f))
            url_to_parse =  site_name + urllib.urlencode(f)
            #parser(url_to_parse)
            form = SiteForm()
            return render(request, 'scheduler.html', {'jobs' : SITE.objects.all(),'form': form})
            #pass  # does nothing, just trigger the validation
    else:
        form = SiteForm()
    return render(request, 'scheduler.html', {'form': form})

# Create your views here.


def create_site_object(site_name,job_title,location,company_name,recurrence,search_start_time):
    site_data = SITE(name = site_name,job_title = job_title,location = location, company_name = company_name,recurrence = recurrence, search_start_time = search_start_time)
    site_data.save()



def parser(url):
    prefix = 'https://www.indeed.com'
    first_page = urllib.urlopen(url).read()
    soup = BeautifulSoup(first_page, "html.parser")
    outputFile = open('example2.csv', 'w')

    def parse_each_page(soup):
        job = soup.find_all("div", class_="row")

        for eachJob in job:
            eachJobUrl = eachJob.find_all('a', class_='turnstileLink')
            eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
            eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
            company = eachJobPage.find_all("div", class_="cmp_title")

            jobTitle = eachJobPage.find_all("b", class_="jobtitle")

            row = []
            try:
                companyName = company[0].a.text
                job = jobTitle[0].font.text
                row.append(companyName)
                row.append(job)
                #with outputFile:
                writer = csv.writer(outputFile)
                print(row)
                writer.writerow(row)
                print(job)
                print(companyName)
                break
            except IndexError:
                pass

    def go_to_next_page(url):
        urlopen = urllib.urlopen(prefix + url)
        print(prefix + url)
        soup = BeautifulSoup(urlopen, "html.parser")
        parse_each_page(soup)
        pagination = soup.find_all("div", class_="pagination")
        next = pagination[0].find_all("a");
        for nextHref in next:
            if "Next" in nextHref.find_all("span")[0].text:
                go_to_next_page(nextHref['href'])

    parse_each_page(soup)

    pagination = soup.find_all("div", class_="pagination")
    next = pagination[0].find_all("a");
    for nextHref in next:
        if "Next" in nextHref.find_all("span")[0].text:
            go_to_next_page(nextHref['href'])
