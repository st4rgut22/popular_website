from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime, date, time
import random

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Date')
ax.set_ylabel('Ranking')
fig.suptitle('Top 10 Websites in the US (Alexa)',fontsize=20,fontweight='bold')

url2016 = urllib.request.urlopen("https://web.archive.org/web/2016*/http://www.alexa.com/topsites/countries/US").read()
url2015 = urllib.request.urlopen("https://web.archive.org/web/2015*/http://www.alexa.com/topsites/countries/US").read()
soup2016 = BeautifulSoup(url2016,"lxml")
soup2015 = BeautifulSoup(url2015,"lxml")

timesrun = 0
numlink = 0
sitelist={} #for colorcoding different sites
def analyze(urlcrawled,timestamp):
     #tracker to prevent duplicate legend keys
    dtobject = datetime.strptime(timestamp,'%Y/%m/%d') #create a datetime object
    newurl = "https://web.archive.org" + urlcrawled
    dateurl = urllib.request.urlopen(newurl).read()
    stirsoup = BeautifulSoup(dateurl,"xml")
    rankings = stirsoup.find_all("li",class_="site-listing")
    for rank in rankings:
        ranknum = rank.find('div',class_='count').get_text()
        if ranknum=='11':
            break;
        site = rank.find('p',class_='desc-paragraph').get_text()
        y=int(ranknum)
        if site not in sitelist: #name of the site is not in dictionary yet
            r = lambda: random.randint(0,255) #pick a random color
            randcolor = ('#%02X%02X%02X' % (r(),r(),r()))
            sitelist[site]= randcolor,[],[]
        sitelist[site][1].append(y)
        sitelist[site][2].append(dtobject) 
        ax.plot_date(dtobject,y,"o",color= sitelist[site][0],label=site if timesrun==0 else "") #if it hasn't been added to the legend yet
        pylab.legend(loc='upper right')
    global timesrun
    timesrun += 1

def finddate(soupobject):    
    for link in soupobject.find_all("div",class_="date captures"):
        numlinks = len(soupobject.find_all("div",class_="date captures")) #find length of array
        urltext = link.find('a').get('href')
        #now we work on the time range
        timestamp = urltext[5:13]
        year = timestamp[:4]
        month = timestamp[4:6]
        day = timestamp[6:]
        dateformat = year + '/' + month + '/' + day
        #compare user input for date range with dates for crawled pages
        if year>useryear:
            analyze(urltext,dateformat)
        elif year==useryear:
            if month>usermonth:
                analyze(urltext,dateformat)
            elif month==usermonth:
                if day>userday:
                    analyze(urltext,dateformat) #pass the url and date time format
        global numlink
        numlink+=1
        if numlink==numlinks and soupobject==soup2015:
            finddate(soup2016)

#implement date range
usertimestamp = input('what is the farthest back you want to search for the most searched websites. Please type your answer in the following format for 2016 January 5: 2016/01/05')
useryear = usertimestamp[:4]
print(useryear)
usermonth = usertimestamp[5:7]
userday = usertimestamp[8:10]
if useryear=='2016':
    print('hello 2016')
    finddate(soup2016)
elif useryear=='2015':
    print('hello 2015')
    finddate(soup2015)


            

for site in sitelist:
    ax.plot(sitelist[site][2],sitelist[site][1],color=sitelist[site][0]) #plot the array of dates (x) and array of ranks (y) matched with each site



plt.show()
