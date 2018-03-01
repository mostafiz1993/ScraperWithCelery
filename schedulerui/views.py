# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response,render
import datetime
import urllib
from bs4 import BeautifulSoup
import csv

from .forms import SiteForm
from .models import *





# Create your views here.
def home (request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            site_name = form.cleaned_data['name']
            job_title = form.cleaned_data['job_title']
            location = form.cleaned_data['location']
            company_name = form.cleaned_data['company_name']
            recurrence = form.cleaned_data['recurrence']
            search_start_time = form.cleaned_data['search_start_time']
            #create_site_object(site_name,job_title,location,company_name,recurrence,search_start_time)
            f = {'q': job_title, 'I': location}
            print urllib.urlencode(f)
            url_to_parse =  site_name + urllib.urlencode(f)
            #parser(url_to_parse)
            form = SiteForm()
            return render(request, 'scheduler.html', {'form': form})
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
                print row
                writer.writerow(row)
                print job
                print companyName
                break
            except IndexError:
                pass

    def go_to_next_page(url):
        urlopen = urllib.urlopen(prefix + url)
        print prefix + url
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
