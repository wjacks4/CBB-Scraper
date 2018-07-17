import urllib
from urllib.request import urlopen
import requests
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment
import html5lib
import pandas as pd
import sys
import numpy as np
import csv

playerinfo=pd.read_csv('/home/ubuntu/WebscrapeInfo/Playername/BryanStuffFull.csv', header=1, names=['index', 'player', 'career', 'fulldata'])

#print(playerinfo)

namelist=playerinfo[['player']]

#print(namelist)

playerfirst=namelist.player.str.split('\s+').str[0]
playerlast=namelist.player.str.split('\s+').str[1]

namelistcat=playerfirst+ "-" +playerlast

namelisttest=["jimmer-fredette", "Copyright Â©"]

for eachplayer in namelistcat:
			player=eachplayer.replace("'", "")
			player=player.lower()
			player=player.encode('ascii', 'ignore').decode('ascii')

			playertable=pd.DataFrame()
			
			print(player)
			
			numlist=[1,2,3,4,5]
			for num in numlist:
				urltest='https://www.sports-reference.com/cbb/players/%s-%s.html' %(player, num)
				print(urltest)
				
				try:
					sauce=urllib.request.urlopen(urltest)
					soup=BeautifulSoup(sauce, 'lxml')
				except urllib.error.HTTPError as err:
					if err.code==404:
						print('next')
				else:

					comments=soup.find_all(string=lambda text:isinstance(text,Comment))
			
					accesslist=[]
			
					for comment in comments:
						soup2=BeautifulSoup(comment, 'lxml')
						table=soup2.find("table", attrs={"class":"row_summable sortable stats_table"})
				
						if table is not None:
							titlecode=table.find('caption').text
							#print(titlecode)
					
							tablehead = table.find('thead')					
							titles=[]					
							colno=0
							for tx in tablehead.find_all('th'):
								coltitle=tx.text
						
								titles.append(coltitle)
						
								colno=colno+1	
				
							#df=pd.DataFrame(columns=titles)
							#print(df)
				
							tablebody = table.find('tbody')
							rowno=0
					
					
							tabledata=[]
							rowdata=[]
							entryno=0
							for row in tablebody.find_all('tr'):						
								#for a in row.find_all('a', href=True):
								#	data.append(a.text)
								a = row.find('a', href=True)
								rowdata.append(a.text)
								for entry in row.find_all('td'):
									rowdata.append(entry.text)
									entryno=entryno+1
								rowno=rowno+1
					
							tabledata=pd.DataFrame(np.array(rowdata).reshape(rowno, colno), columns=titles)
					
							playersplit=player.split("-")
							playerspace=playersplit[0] + " " + playersplit[1]
							tabledata['Player']=pd.Series((playerspace), index=tabledata.index)
					
							#print(tabledata)		
				
							tabledata.to_csv('/home/ubuntu/WebscrapeInfo/Databyplayer/%s%s.csv' %(player,titlecode))
					
							access='/home/ubuntu/WebscrapeInfo/Databyplayer/%s%s.csv' %(player, titlecode)
							print(access)
							accesslist.append(access)
				
						#print(accesslist)
				


				

#dfstart=pd.read_csv('C:/Users/whjac/Downloads/data science/Databyplayer/jimmer-fredetteTotals Table.csv')
#print(dfstart)
#each=pd.read_csv('C:/Users/whjac/Downloads/data science/Databyplayer/jimmer-fredetteTotals Table.csv')
#print(each)


					dfstart=pd.DataFrame()
					for table in accesslist:
						each=pd.read_csv(table)
						dfstart=dfstart.append(each)

					#print(dfstart)

				dfstart.to_csv('/home/ubuntu/WebscrapeInfo/Outputdata/%sTOTAL.csv' %(player))

