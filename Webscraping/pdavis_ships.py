from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from lxml import etree
import io
import re

superout = ""
u = 0
def followlink(newurl):
## Funktion zum Aufruf und Auslesen der Detailseiten zu Schiffen
    newcontent = urlopen(newurl).read()
    suppe = BeautifulSoup(newcontent)
    newdata = suppe.prettify()
    
    table = suppe.find("table", { "class" : "tbl width100" })
    ## Aufruf des tags <table class:"tbl width100"
    d = table.find_all('td', { "class" : "pright"})
    ## alle td-tags der Tabelle
    dates  =list()
    eventlist = list()
    for date in d:
	## normaisierung der Datumsangaben auf YYYY.MM
        nope = True
        date = re.sub("<td class=\"pright\">|</td>|<a id=\"d[0-9]+\"></a>|^<td class=\"tblfil pright\".*|\(various\)|\(|\)","",str(date))
        
        year = re.findall("[0-9]{4}",date)
        jan = re.findall("January",date)
        feb = re.findall("February",date)
        mar = re.findall("March",date)
        apr = re.findall("April",date)
        may = re.findall("May",date)
        jun = re.findall("June",date)
        jul = re.findall("July",date)
        aug = re.findall("August",date)
        sep = re.findall("September",date)
        okt = re.findall("October",date)
        nov = re.findall("November",date)
        dez = re.findall("December",date)

        if len(year) == 1: 
            year=str(year[0])
            if len(jan) > 0 and nope == True:		    
                nope = False
                dates.append(str(year)+".01")
            if len(feb) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".02")
            if len(mar) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".03")
            if len(apr) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".04")
            if len(may) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".05")
            if len(jun) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".06")
            if len(jul) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".07")
            if len(aug) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".08")
            if len(sep) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".09")
            if len(okt) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".10")
            if len(nov) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".11")
            if len(dez) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".12")

        if len(year) == 2: 
            year=str(year[0])
            if len(jan) > 0 and nope == True:		    
                nope = False
                dates.append(str(year)+".01")
            if len(feb) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".02")
            if len(mar) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".03")
            if len(apr) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".04")
            if len(may) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".05")
            if len(jun) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".06")
            if len(jul) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".07")
            if len(aug) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".08")
            if len(sep) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".09")
            if len(okt) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".10")
            if len(nov) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".11")
            if len(dez) > 0 and nope == True:
                nope = False
                dates.append(str(year)+".12")
    
    for item in table.find_all('td', {"colspan" : "3"}):
	## Auslesen der Events
        if item.text != "Event" and len(item.text) < 100:
            
            eventlist.append(item.text)
    z = 0
    out2 = ""    
    for eve in eventlist:
	## Zusammenbringen von Event und Datum
       if len(dates) > z:
           out2+="<event><date>"+str(dates[z])+"</date><name>"+str(eve)+"</name></event>"
           z+=1
    return(out2)      
 
str_all = ""
linkliste = []
superlist = list()
for i in range (1,14):
    ## Schleife über alle Shiplists
    url = "http://pdavis.nl/MidVicShips.php?page="+str(i)
    content = urlopen(url).read()
    soup = BeautifulSoup(content)
    
    data = soup.prettify()
    
    table1 = soup.find("table", { "class" : "tbl width100" })
    
    out = ""
    for line in table1:
        newout = ""
        
        if re.match("<tr class=\"top\"><td><a href=\"ShowShip\.php",str(line)):
            itemlink = re.findall("ShowShip.php\?id=[0-9]{1,5}",str(line))
            
            itemlink=re.sub("\[|\]|\'","",str(itemlink[0]))
            superlist = list()
            newurl = "http://www.pdavis.nl/"+itemlink
            
            out2=followlink(newurl)
                       
            
            newout+=str(itemlink)+"\t"
        else:
            newout+="\t"
        items = re.findall("<td>[^<]*</td>|<a href=\"ShowShip.php\?id=[0-9]{1,5}\">[^<]*</a>",str(line))
        if len(items) > 0:
            out2 = "<ship id='"+str(u)+"' name='"+re.sub("</td>|</a>|<td>|<a href=\"ShowShip.php\?id=[0-9]{1,5}\">","",str(items[0]))+"'>"+ out2+"</ship>"
            superout += out2
        
        u+=1
        if len(items) > 0:
            
            if re.match("<td></td>",items[1]):
                print("no_date")
            if re.match(".*r",items[1]):
                if len(out) < 2: 
                   newout+="\tr\t"
                else:
                   newout+="r\t"
            else:   
                newout+="\t"
            items[1]=items[1][:8]+"0000\t"
            
        
        
        for item in items:
            item = re.sub("<td>|<a href=\"ShowShip.php\?id=[0-9]{1,5}\">","\t",item)
            item = re.sub("</td>|</a>","",item)
            newout += item
            
        if len(newout) > 1:
            newout+= "\n"
            out+=newout
    str_all += re.sub("\t\t","\t",out)
    
str_all ="Link\tR\t\tShipname\tLaunch\t\tH.\tP.\tType\tB.M.\tDisp.\tGuns\tFate\tS.B.\tNote\n" + str_all
superout = "<shiplist>"+superout+"</shiplist>"
with io.FileIO("locations.xml", "w") as file:
        file.write(superout.encode(u"utf-8"))
with io.FileIO("ships.csv", "w") as file:
        file.write(str_all.encode(u"utf-8"))

