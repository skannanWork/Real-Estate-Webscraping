import requests
from bs4 import BeautifulSoup
import pandas

# Get contents from the century21 website


webSource = requests.get("https://www.century21.com/real-estate/california-riverside-san-bernardino-ontario-ca/LR92583CALIFORNIA/?sa=CCAFORESTFALLS%2CCCAMORENOVALLEY%2CCCAWINCHESTER")
webSource.raise_for_status()

soup = BeautifulSoup(webSource.text,"html.parser")

housingInfo = soup.find_all("div",{"class":"infinite-container"})
infoList =[]

for items in housingInfo:
    
    address = items.find_all("div",{"class":"property-address"})
    cities = items.find_all("div",{"class":"property-city"})
    beds = items.find_all("div",{"class":"property-beds"})
    baths = items.find_all("div",{"class":"property-baths"})
    areas = items.find_all("div",{"class":"property-sqft"})
    prices = items.find_all("a",{"class":"listing-price"})
    
    for address, city,bed,bath,sqft,price in zip(address,cities,beds,baths,areas,prices):
        
        d={}
        
        try:
            d["Address"]=address.text.replace("\n","").replace("   ","")
        except:
            pass
        
        try:
            d["City"]=city.text.replace("\n","").replace("  ","")
        except:
            pass
        
        try:
            d["Bed's"]=bed.find("strong").text
        except:
            pass
        
        try:
            d["Bath's"]=bath.find("strong").text
        except:
            pass
        
        try:
            d["SqFt"]=sqft.find("strong").text
        except:
            pass
        
        try:
            d["Price"]=price.text.replace("\n","").replace(" ","")
        except:
            pass
        infoList.append(d)

df = pandas.DataFrame(infoList)

df.to_csv("CaliRealEstate.csv")