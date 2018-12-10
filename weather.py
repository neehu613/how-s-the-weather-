import re, os, time
from bs4 import BeautifulSoup
from urllib.request import urlopen
def printline():
	lines = '-'*99
	print (lines)

os.system("clear")

city = input("Enter the city: ")
city1 = city
city = re.sub(' ', '+', city)
printline()
print ("\nSEARCH RESULTS\n")
url = 'https://www.bbc.com/weather/search?s='+city 

html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')


allLinks = soup.find_all('a', {'class' : 'location-search-results__result__link'})
newLinks = list()
maxTemps = list()
minTemps = list()
weatherList = list()
dateList = list()
dayList = list()
datesList = list()

i=1

if len(allLinks) == 0:
	print ("Couldn't find " + city1)
	print ("Please enter a specific city(Don't enter a state/continent)")
	quit()

for link in allLinks:
		uniqueId = link.get('href')
		newLinks.append('https://www.bbc.com/weather/'+uniqueId)
		print (i, link.text)
		i += 1

printline()

choice =  int(input("\n\nSelect the place from the above list: "))
print ("Gathering information, please be patient....")
time.sleep(1)
newUrl = newLinks[choice-1]

html = urlopen(newUrl)
soup = BeautifulSoup(html, "html.parser")

weatherToday = soup.find('div', {'class': 'wr-day__details__weather-type-description'})
todaysWeather = weatherToday.string
weatherList.append(todaysWeather)

print ("\n\n")
printline()
print ("Weather in " + city1 + " today:\t", todaysWeather)

weatherStatus = soup.find_all('div', {'class' : 'wr-day__weather-type-description wr-js-day-content-weather-type-description wr-day__content__weather-type-description--opaque'})
weatherStatus = weatherStatus[:9]

for day in weatherStatus:
	weatherList.append(day.string)

tempInCelcius = soup.find_all('span', {'class': 'wr-value--temperature--c'})
observationTemp = tempInCelcius[-1]
tempInCelcius = tempInCelcius[:20]
i=0
for temp in tempInCelcius:
	tempToAppend = re.findall('\d', temp.text[:2])
	tempToAppend = [str(item) for item in tempToAppend]
	temp = ''.join(tempToAppend)
	if i % 2 == 0:
		#maxTemps.append(str(temp.text[:2]))
		maxTemps.append(str(temp))
	else:
		#minTemps.append(str(temp.text[:2]))
		minTemps.append(str(temp))
	i+=1

date = soup.find('span', {'class':'wr-date'})
for i in date:
	today = date.string

today = str(today)+'   '
datesList.append(today)
'''
date1 = soup.find('span', {'class': 'wr-date__short'})
for i in date1:
	tomorrow = date1.string

tomorrow = str(tomorrow)
datesList.append(tomorrow)
'''
dates = soup.find_all('span', {'class': 'wr-date__longish'})

for date in dates:
	date[3] = ' '
	whichDay = date.text
	datesList.append(whichDay)

print ("\n\nDATE\t\t\tWEATHER\t\t\t\t\t\t\tMAX\tMIN")
for temp in range(len(maxTemps)):
	spaces = (56 - len(weatherList[temp]))*' '
	print (datesList[temp]+ "\t\t" + weatherList[temp] + spaces + maxTemps[temp] + "\t" + minTemps[temp])

'''
tempInFahr = soup.find('span', {'class': 'wr-value--temperature--f'})
print "Temperature in Fahrenheit:\t", tempInFahr.text
'''
printline()
observationTime = soup.find('span', {'class': 'wr-c-observations__timestamp gel-long-primer gs-u-mt--'})
print (observationTime.text)

print ("\nTemperature during observation\n", observationTemp.span.text)

Windspeed = soup.find('span', {'class': 'wr-value--windspeed wr-value--windspeed--mph'})
print ("\nWindspeed during observation\n", Windspeed.text)

obsDetails = soup.find_all('li', {'class': 'wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--'})
for obs in obsDetails:
	print (obs.text)

obsStation = soup.find('div', {'class': 'wr-c-observations__location gel-layout__item gel-1/1 gel-brevier gs-u-mt-- gs-u-mt@xl'})
print (obsStation.text)

sunrise = soup.find('span', {'class': 'wr-c-astro-data__sunrise gel-pica-bold gs-u-pl-'})
print (sunrise.text)

sunset = soup.find('span', {'class': 'wr-c-astro-data__sunset gel-pica gs-u-pl-'})
print (sunset.text)

printline()
