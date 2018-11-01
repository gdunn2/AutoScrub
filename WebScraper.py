import time
import requests
import bs4 as bs
import webbrowser as wb

googleUrl = 'https://www.google.com/search?q='

def googleSearch(search):
    searchLink = googleUrl + search
    print(searchLink)
    googleSite = requests.get(searchLink)
    wb.open(searchLink)
    b = bs.BeautifulSoup(googleSite.content,'html.parser')
    e = b.select('h3 a')
    for child in e:
        link = child['href']
        if link.find('realtor.com') != -1: #make sure it is the right adrress too
            start = link.find('https')
            stop = link.find('&aqs')
            newLink = link[start:stop]
            return newLink
        else:
            return

    return

def recentlySold(search, minTime, sold): #called when a url needs to be scraped
   link = googleSearch(search)
   if link:
       print(link)
   else:
        print('property not found on realtor.com' + search)
