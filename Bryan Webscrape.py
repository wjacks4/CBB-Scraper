import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pandas as pd
import sys
import numpy as np

firstletters=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
firstletterstest=["a", "b"]

years=["2013","2014","2015","2016"]

teamstest=["arizona-cardinals", "atlanta-falcons"]

yearstest=["2013","2014"]

d=[]

for letter in firstletters:
			
			urltest='https://www.sports-reference.com/cbb/players/%s-index.html' %(letter)
			
			sauce=urllib.request.urlopen(urltest)
			soup=BeautifulSoup(sauce, 'lxml')
			
			divs = soup.find_all("div")
			#print(divs)
				
			for div in divs:
				entries = div.find_all("p")
				for entry in entries:
					#print(entry.text)
					info=entry.text
					words=info.split()
					name=words[0] + " " + words[1]
					career=words[2]
					d.append((name, career, words))
					df=pd.DataFrame(d, columns=('Player', 'Career', 'FullData'))
					
					
					
					
					
				
		#print(rosterdf)				
df.to_csv('C:/Users/whjac/Downloads/data science/BryanStuffFull.csv')		

			
#print(d)