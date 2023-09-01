# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import date
import datetime
import time
import re
import locale
url = "https://asikkala.fi/koulujen-ruokalista/"

def translate_date(tomorrow):
    if tomorrow == "Monday":
        tomorrow = "Maanantai"
    if tomorrow == "Tuesday":
        tomorrow = "Tiistai"
    if tomorrow == "Wednesday":
        tomorrow = "Keskiviikko"
    if tomorrow == "Thursday":
        tomorrow = "Torstai"
    if tomorrow == "Friday":
        tomorrow = "Perjantai"
    return tomorrow

#only get weekday dates
#Skip weekends to monday and next day
def get_weekday_dates(input):
    if input.weekday() == 0 or input.weekday() == 1 or input.weekday() == 2 or input.weekday() == 3:
        monday = input + timedelta(days=1)
    if input.weekday() == 4:
        monday = input + timedelta(days=3)
    if input.weekday() == 5:
        input = input + timedelta(days=2)
    if input.weekday() == 6:
        monday = input + timedelta(days=1)
    return monday

def get_ruokalista() -> (str | int):
    from datetime import date
    # Send a GET request to the website and retrieve the HTML content
    response = requests.get(url)
    html_content = response.text

    # find current date
    today = date.today()

    monday = get_weekday_dates(today)

    d1 = today.strftime("X%d.X%m.%Y").replace('X0','X').replace('X','')
    d2 = monday.strftime("X%d.X%m.%Y").replace('X0','X').replace('X','')

    #get tomorrows days name and translate it to finnish
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.strftime("%A")


    tomorrow= str(translate_date(tomorrow))

    #if start is inside <meta> skip to next
    endnotfound = 0 

    #look for dates in html content
    start = html_content.find(d1)
    end = html_content.find(d2)
    #look for next d2
    #if diffrence between start and end is less than 1000, then there is no food for today
    if end - start > 500:
        endnotfound = 1

    #check if date is found if not print error and fallback to old method
    if end == -1 or endnotfound == 1:
        locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')
        pvm = datetime.datetime.today()
        date = datetime.datetime.today().strftime('%A')
        dateisona = date.capitalize()
        time = pvm.strftime("X%d.X%m.%Y").replace('X0','X').replace('X','')
        #print(time)
        start = "<p>"+ str(dateisona)+" "+ str(time)
        weekno = pvm.weekday()
        #print(dateisona)
        html_text = requests.get(url).text
        startofdate = html_text.find(time)
        if startofdate == -1:
                print("No food for today :)")
                return 1
        i = 1
        while i == 1:
            ruokastart = html_text.find(startdiv)
            #print(ruokastart)
            ruokaend = html_text.find("</p>", ruokastart)
            startofdate = ruokaend
            ruoka = html_text[ruokastart + 3:ruokaend]
            ruoka1 = ruoka.split("<br>")
            #print(ruoka)
            heittomerkkipois = str(ruoka1).replace("'","")
            pilkutpois = str(heittomerkkipois).replace(",","\n")
            reunatpois = str(pilkutpois).replace("[","")
            toinenreunapois = str(reunatpois).replace("]", "")
            lounaspoius = str(toinenreunapois).replace("LOUNAS", "")
            välipois = str(lounaspoius).replace("\n \n", "\n")
            modified_string = str(välipois).replace("\n ","\n")
            i = -1
            print(modified_string)

    #print between start and end
    osa = html_content[start:end]  
    modified_string = osa.replace(tomorrow, "")
    #if <p> is found, replace it with space
    #use beautifulsoup to remove html tags
    soup = BeautifulSoup(modified_string, 'html.parser')
    modified_string = soup.get_text()
    #remove LOUNAS from string
    modified_string = modified_string.replace("LOUNAS", "")

    # Check if it's holiday. It should contain "vapaapäivä"
    if "Vapaapäivä" in modified_string:
        return 0

    return modified_string

if __name__ == "__main__":
    print(get_ruokalista())