import urllib2
from bs4 import BeautifulSoup
import re
import csv

response = urllib2.urlopen('http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/current/series/509587.html')
html = response.read()
soup = BeautifulSoup(html)

result_file=open('results.txt','w')
result_csv=csv.writer(open('result.csv','wb'))
def get_country_squad(id,name):
	url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/'+str(id)+'.html'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	image_links=soup.findAll('a', href=re.compile('/icc-cricket-world-cup-2015/content/player/'))
	for i in image_links:
		if i.text:
			result_csv.writerow([id,name,i.get('href').split('/')[-1].split('.')[0],i.text.strip()])

def get_country_id():
	root_url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/current/series/509587.html'
	root_response=urllib2.urlopen(root_url)
	root_html=root_response.read()
	root_soup=BeautifulSoup(root_html)
	country_links= root_soup.findAll('a',href=re.compile('/icc-cricket-world-cup-2015/content/squad/'))
	for i in country_links:
	#print i
		country_name=i.text
		country_id=i.get('href').split('/')[-1].split('.')[0]
		print country_id ,'--',country_name
		result_file.write(str(country_id)+'----'+str(country_name)+'\n')
		get_country_squad(str(country_id),str(country_name))

#get_country_id()
#result_file.close()

get_country_id()