from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from datetime import datetime, date, time
import random



url = urllib.request.urlopen("https://web.archive.org/web/*/http://www.alexa.com/topsites/countries/US").read()
soup = BeautifulSoup(url,"lxml")
timesrun = 0
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
        arr.append(y)
        if site not in sitelist: #name of the site is not in dictionary yet
            r = lambda: random.randint(0,255) #pick a random color
            randcolor = ('#%02X%02X%02X' % (r(),r(),r()))
            sitelist[site]= randcolor #set as 1, if not set then add
        plt.plot_date(dtobject,y,"o",color= sitelist[site],label=site if timesrun==0 else "") #if it hasn't been added to the legend yet
        pylab.legend(loc='upper right')
    global timesrun
    timesrun += 1

#implement date range
usertimestamp = input('what is the farthest back you want to search for the most searched websites. Please type your answer in the following format for 2016 January 5: 2016/01/05')
useryear = usertimestamp[:4]
usermonth = usertimestamp[5:7]
userday = usertimestamp[8:10]
for link in soup.find_all("div",class_="date captures"):
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


plt.show()
