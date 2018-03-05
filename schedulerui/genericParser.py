import csv
import requests
from bs4 import BeautifulSoup
import urllib

def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

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

def parse_each_page(soup):
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
        print(jobTitle)
        print(company)
        print(jobLocation)


def go_to_next_page(url):
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
    parse_each_page(soup)
    if int(property['directPagination']) != 1:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
        try:
            go_to_next_page(next['href'])
        except:
            return

    else:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        print(pagination[0]['href'])
        try:
            go_to_next_page(pagination[0]['href'])
        except:
            return








def runParser(jobURL,location,jobTtile,searchSyntax,csvName):
    soup = getSoap('https://www.monster.com/jobs/search/?q=Data-Scientist&where=new-york&intcid=skr_navigation_nhpso_searchMain')


    property = {}
    identifierofEachJobAttr = {}
    identifierofEachJobUrl = {}
    jobTitileAttr = {}
    jobCompanyAttr = {}
    jobLocationAttr = {}
    paginationAttr = {}


    initParameter('monster.csv')

    parse_each_page(soup)

    if int(property['directPagination']) != 1:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        next = pagination[0].find_all(property['jobPaginationBranchAttr'])[int(property['jobPaginationBranchInedex'])]
        try:
            go_to_next_page(next['href'])
        except:
            pass
    else:
        pagination = soup.find_all(property['paginationIn'], attrs=paginationAttr)
        # print pagination[0]['href']
        try:
            go_to_next_page(pagination[0]['href'])
        except:
            pass
