import urllib2
from bs4 import BeautifulSoup
import csv

players=csv.reader(open('result.csv','rb'))
bowling_csv=csv.writer(open('bowlingv2.csv','wb'))

def year_score(soup,year):
	try:
		data2014 = soup.findAll(text='year '+str(year))[0].parent.parent.parent
		data=data2014.findAll("td")
		innings=int(data[3].get_text())
		overs=float(data[4].get_text())
		runs=int(data[6].get_text())
		maidens=int(data[5].get_text())
		wickets=int(data[7].get_text())
		fourw=int(data[12].get_text())
		fivew=int(data[13].get_text())
		pace=6*overs-runs
		score=30*wickets+15*maidens+45*fourw+70*fivew+pace
		return (score,innings)
	except:
		return (0,0)

def balling_score(country_id,country_name,player_id,player_name):
	url='http://stats.espncricinfo.com/ci/engine/player/'+str(player_id)+'.html?class=2;template=results;type=bowling'
	try:
		print url
		response = urllib2.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)
		(score14,innings14)=year_score(soup,2014)
		(score15,innings15)=year_score(soup,2015)
		avgscore=float((score14*1+score15*2)/(innings14+2*innings15))
		bowling_csv.writerow([country_id,country_name,player_id,player_name,avgscore,score14,innings14,score15,innings15])
	except:
		return


for row in players:
	print row
	balling_score(row[0],row[1],row[2],row[3])
