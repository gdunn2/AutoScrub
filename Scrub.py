import requests
import xml.etree.ElementTree as et

from WebScraper import recentlySold

zillowSearchEP = "http://www.zillow.com/webservice/GetSearchResults.htm"
zillowZestimateEP = "http://www.zillow.com/webservice/GetZestimate.htm"
zillowUPDEP = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"
zID = 'X1-ZWz1gpt9peznrf_9ljvt' #zillow ID for using API

def getZestimate(ZPID, maxPrice): #get approximate worth from Zillow

    searchParams = {"zws-id":zID, "zpid":ZPID}

    request = requests.get(zillowZestimateEP,searchParams)
    root = et.fromstring(request.content)

    code = root.find('message').find('code').text

    if code == '0': #if the request was a success
        zestimate = root.find('response').find('zestimate').find('amount').text #stores the approcimate worth in zestimate
        if int(zestimate) > maxPrice: #if zestimate is over $400,000 then return false
            return False
        else:
            return True
    elif code == '3' or code == '4': #zillow is being stupid
        return 'ZillowDown'
    else:
        return True
   
#REMEMBER TO SEARCH FOR APARTMENT NUMBERS IN TEXT AND REMOVE THEM

def scrub(address, zip, maxPrice, minTime, sold):

    searchParams = {"zws-id":zID, "address":address, "citystatezip": zip} #Paramaters needed to access Zillow Search

    request = requests.get(zillowSearchEP, searchParams) #Response of the search
    root = et.fromstring(request.content) #parses the xml text. gives root element of element tree

    code = root.find('message').find('code').text

    if code == '0':
        results = root.find('response').find('results').find('result') #goes in all the way to the result element(where zpid is contained)
        ZPID = results.find('zpid').text #stores the zpid in a variable
        search = address + ' ' + zip
        if getZestimate(ZPID, maxPrice) and not recentlySold(search, minTime, sold): #if the estimated worth of the property is below the max price and it has not been sold recently, returns true
            return True
        else:
            return address + ': False'
    elif code == '3' or code == '4':
        #try again later('zillow is messed up or something')
        return 'ZillowDown' 
    else:
        return True
