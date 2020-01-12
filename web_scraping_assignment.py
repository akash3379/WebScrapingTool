"""
@File:web_scraping_assignment.py
@Owner:Akashkumar Patel
@E-mail:akashkum@usc.edu
@Date:2019/01/11
@Desc:This script will be used to find an automated way of getting the number of orbital launches in the 
'Orbital launches' table from link https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches
"""
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import datetime

url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#Fetch the whole table content
tb = soup.find('table', class_='wikitable')
#Fetch all rows
rows = tb.find_all('tr');
#used to get ,pmth in int from string
monthDic = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06","July":"07", "August":"08", "September":"09", "October":"10","November":"11", "December":"12"}

dic = defaultdict(int)
flag=0
#Iterate all rows and foe each day increment the count in dic if at least one payload has outcome ['Successful', 'Operational', 'En Route']
for row in rows:
    cols = row.find_all('td')
    if(len(cols)==5):
        date=cols[0].find('span',class_='nowrap')
        date = str("2019-"+ monthDic[date.text.split(' ')[1].split('[')[0]] +"-" +'%02d'%int(date.text.split(' ')[0])+ "T00:00:00+00:00")
        flag=1
    
    elif (len(cols) == 6):
        payload = cols[0].text.split('[')[0].strip()
        if(len(cols[0].find_all('abbr'))>0):
            payload = payload[3:]
        
        outcome = cols[-1].text.strip()
        
        if outcome in ['Successful', 'Operational', 'En Route']:
            if(flag==1):
                dic[date]+=1
                flag=0

#Open file output.csv to write output          
f = open("output.csv", "w")

start = datetime.datetime.strptime("2019-1-1", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-1-1", "%Y-%m-%d")
    
#Iterate though all cate of year 2019 and write into file
for x in range(0, (end-start).days):
    date_object = (start + datetime.timedelta(days=x))
    date = str(date_object.strftime("%Y-%m-%d")+"T00:00:00+00:00")
    if date in dic:
        f.write(date+","+str(dic[date])+"\n")
    else:
        f.write(date+",0\n")
f.close()