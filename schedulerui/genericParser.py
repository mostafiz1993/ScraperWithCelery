import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import time
from celery import shared_task,current_task
from .TaskState import *



property = {}
identifierofEachJobAttr = {}
identifierofEachJobUrl = {}
jobTitileAttr = {}
jobCompanyAttr = {}
jobLocationAttr = {}
paginationAttr = {}
csvFileName = ''

def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')




def generate_csv(jobTitle,jobLocation,jobCompany,writer):
    try:
        writer.writerow({'JobTitle': jobTitle, 'JobLocation': jobLocation, 'Company': jobCompany})
        #csvF.write(jobTitle + ',' + jobLocation + ',' + jobCompany + '\n')
    except:
        pass




def initParameter(csvFile):
    with open(csvFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            property[row[0]] = row[1]
            #if row[0].split(',')[0] == 'valueOfIdentifierofEachJobAttr':
            #print row
        identifierofEachJobAttr[property['identifierofEachJobAttr']] = property['valueOfIdentifierofEachJobAttr']
        identifierofEachJobUrl[property['identifierofEachJobUrl']] = property['valueOfIdentifierofEachJobUrl']
        jobTitileAttr[property['jobTitileAttr']] = property['valueOfjJobTitileAttr']
        jobCompanyAttr[property['jobCompanyAttr']] = property['valueOfJobCompanyAttr']
        jobLocationAttr[property['jobLocationAttr']] = property['valueOfjJobLocationAttr']
        paginationAttr[property['paginationAttr']] = property['valueOfPaginationAttr']

def parse_each_page(soup,writer):
    job = soup.find_all(property['eachJobIn'], attrs = identifierofEachJobAttr)
    for eachJob in job:
        if int(property['directEachjobUrl']) == 1:
            eachJobUrl = eachJob.find_all(property['EachJobUrlIn'])
            #print eachJobUrl
        else:
            eachJobUrl = eachJob.find_all(property['EachJobUrlIn'], attrs = identifierofEachJobUrl)
        if int(property['prefixFlag']) == 1:
            eachJobUrl = property['prefix'] + eachJobUrl[0]["href"]
        else:
            eachJobUrl = eachJobUrl[0]["href"]

        eachJobPage = getSoap(eachJobUrl)
        if int(property['jobCompanyBranch']) == 1:
            companyt = eachJobPage.find_all(property['jobCompanyIn'], attrs = jobCompanyAttr)
            try:
                companyt1 = companyt[0].find_all(property['jobCompanyBranchAttr'])
                company = companyt1[0].text

            except:
                company=''
                pass
        else:
            companyt = eachJobPage.find_all(property['jobCompanyIn'], attrs=jobCompanyAttr)
            try:
                company = companyt[0].text
            except:
                company = ''
                pass
        if int(property['jobTitileBranch']) == 1:
            jobt = eachJobPage.find_all(property['jobTitileIn'], attrs=jobTitileAttr)
            try:
                jobt1 = jobt[0].find_all(property['jobTitileBranchAttr'])
                jobTitle = jobt1[0].text
            except:
                jobTitle = ''
                pass
        else:
            jobt = eachJobPage.find_all(property['jobTitileIn'], attrs=jobTitileAttr)
            try:
                jobTitle = jobt[0].text
            except:
                jobTitle = ''
                pass

            #companyName = company[0].a.text
            #job = jobTitle[0].font.text
        jobL = eachJobPage.find_all(property['jobLocationIn'], attrs=jobLocationAttr)
        if property['jobLocationIn'] == 'input':
            try:
                jobLocation = jobL[0]['value']
            except:
                jobLocation = ''
                pass
        else:
            try:
                jobLocation = jobL[0].text
            except:
                jobLocation = ''
                pass
        generate_csv(jobTitle,jobLocation,company,writer)


def go_to_next_page(url,writer):
    if int(property['prefixPaginationFlag']) == 1:
        try:
            urlopen = property['prefix'] + url
        except:
            return
    else:
        try:
            urlopen = url
        except:
            return
    print(url)

    soup = getSoap(urlopen)
    parse_each_page(soup,writer)
    if int(property['directPagination']) != 1:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
        try:
            go_to_next_page(next['href'],writer)
        except:
            return

    else:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        #print(pagination[0]['href'])
        try:
            go_to_next_page(pagination[0]['href'],writer)
        except:
            return

@shared_task
def runParser(searchSyntax,location,jobTtile,csvName):
    #url = 'https://www.simplyhired.com/search?q=data+scientist&l=New+York'

    current_task.update_state(state=TaskState.SCHEDULED)
    par1 = searchSyntax[searchSyntax.find('?') + 1:searchSyntax.find('=')]
    par2 = searchSyntax[searchSyntax.find('&') + 1:searchSyntax.rfind('='):]
    encodedurl = {par1: jobTtile, par2: location}
    url =  searchSyntax[:searchSyntax.find('?') + 1] + urllib.urlencode(encodedurl)
    soup = getSoap(url)
    initParameter(csvName)
    fieldnames = ['JobTitle', 'JobLocation', 'Company']
    csvF = csv_file_name_generation(csvName)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    current_task.update_state(state=TaskState.STARTED)
    parse_each_page(soup,writer)
    current_task.update_state(state=TaskState.RUNNING)
    if int(property['directPagination']) != 1:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
        try:
            go_to_next_page(next['href'],writer)
        except:
            pass
    else:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        # print pagination[0]['href']
        try:
            go_to_next_page(pagination[0]['href'],writer)
        except:
            pass

    current_task.update_state(state=TaskState.SUCCESS)



