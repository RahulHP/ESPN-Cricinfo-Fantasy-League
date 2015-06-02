import urllib2
from bs4 import BeautifulSoup
import re
import csv

stats=csv.writer(open('stats.csv','wb'))


def get_country_id():
	root_url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/current/series/509587.html'
	root_response=urllib2.urlopen(root_url)
	root_html=root_response.read()
	root_soup=BeautifulSoup(root_html)
	country_links= root_soup.findAll('a',href=re.compile('/icc-cricket-world-cup-2015/content/squad/'))
	for i in country_links:
		country_name=i.text
		country_id=i.get('href').split('/')[-1].split('.')[0]
		print country_id ,'--',country_name
		get_country_squad(str(country_id),str(country_name))

def get_country_squad(country_id,country_name):
	url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/'+str(country_id)+'.html'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	image_links=soup.findAll('a', href=re.compile('/icc-cricket-world-cup-2015/content/player/'))
	for i in image_links:
		if i.text:
			player_id=i.get('href').split('/')[-1].split('.')[0]
			player_name=i.text.strip()
			statsf(country_id,country_name,player_id,player_name)


def statsf(country_id,country_name,player_id,player_name):
	print player_name
	print 'Bowling ...'
	(bowlinnings,overs,runsgiven,maidens,wickets,fourw,fivew) = stat_scraper(country_id,country_name,player_id,player_name,'bowling')
	print 'Batting ...'
	(runs_made,sixes,fours,ducks,fifties,hundreds,balls_faced,batinnings) = stat_scraper(country_id,country_name,player_id,player_name,'batting')
	stats.writerow([country_id,country_name,player_id,player_name,bowlinnings,overs,runsgiven,maidens,wickets,fourw,fivew,runs_made,sixes,fours,ducks,fifties,hundreds,balls_faced,batinnings])
	print 'Done'

def stat_scraper(country_id,country_name,player_id,player_name,action):
	year=2014
	url='http://stats.espncricinfo.com/ci/engine/player/'+str(player_id)+'.html?class=2;template=results;type='+str(action)+';view=innings;year='+str(year)
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	if action=='bowling':
		array=(3,4,6,5,7,12,13)
	else:
		array=(4,13,12,11,10,9,7,2)
	year_data = soup.findAll(text='filtered')[0].findParents('tr')[0].findAll("td")
	results=[]
	for i in array:
		try:
			results.append(float(year_data[i].get_text()))
		except:
			results.append(0)
	print action,'----',results
	return results

get_country_id()
