# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response,render
import datetime
import urllib
from bs4 import BeautifulSoup

from .forms import SiteForm


# Create your views here.
def home (request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            site_name = form.cleaned_data['name']
            job_title = form.cleaned_data['job_title']
            location = form.cleaned_data['location']
            f = {'q': job_title, 'I': location}
            print urllib.urlencode(f)
            url_to_parse =  site_name + urllib.urlencode(f)
            parser(url_to_parse)
            form = SiteForm()
            return render(request, 'scheduler.html', {'form': form})
            #pass  # does nothing, just trigger the validation
    else:
        form = SiteForm()
    return render(request, 'scheduler.html', {'form': form})

# Create your views here.


def parser(url):
    prefix = 'https://www.indeed.com'
    first_page = urllib.urlopen(url).read()
    soup = BeautifulSoup(first_page, "html.parser")

    def parse_each_page(soup):
        job = soup.find_all("div", class_="row")
        for eachJob in job:
            eachJobUrl = eachJob.find_all('a', class_='turnstileLink')
            eachJobUrl = urllib.urlopen(prefix + eachJobUrl[0]["href"])
            eachJobPage = BeautifulSoup(eachJobUrl, "html.parser")
            company = eachJobPage.find_all("div", class_="cmp_title")
            jobTitle = eachJobPage.find_all("b", class_="jobtitle")
            try:
                companyName = company[0].a.text
                job = jobTitle[0].font.text
                print job
                print companyName
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
