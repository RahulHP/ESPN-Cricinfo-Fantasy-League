import urllib2
from bs4 import BeautifulSoup
import csv

players=csv.reader(open('result.csv','rb'))
batting_csv=csv.writer(open('battingv2.csv','wb'))

def year_score(soup,year):
	try:
		data2014 = soup.findAll(text='year '+str(year))[0].parent.parent.parent
		data=data2014.findAll("td")
		runs=int(data[5].get_text())
		sixes=int(data[14].get_text())
		fours=int(data[13].get_text())
		ducks=int(data[12].get_text())
		fifties=int(data[11].get_text())
		hundreds=int(data[10].get_text())
		balls=int(data[8].get_text())
		innings=int(data[3].get_text())
		if runs > balls:
			pace=2*(runs-balls)
		else:
			pace=(.5)*(balls-runs)
		score=1*runs+3*sixes+1*fours+(-5)*ducks+10*fifties+45*hundreds+pace
		return (score,innings)
	except:
		return (0,0)


def batting_score(country_id,country_name,player_id,player_name):
	url='http://stats.espncricinfo.com/ci/engine/player/'+str(player_id)+'.html?class=2;template=results;type=batting'
	try:
		print url
		response = urllib2.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)
		(score14,innings14)=year_score(soup,2014)
		(score15,innings15)=year_score(soup,2015)
		avgscore=float((score14*1+score15*2)/(innings14+2*innings15))
		batting_csv.writerow([country_id,country_name,player_id,player_name,avgscore,score14,innings14,score15,innings15])
	except:
		return

for row in players:
	print row
	batting_score(row[0],row[1],row[2],row[3])
