# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:08:53 2016

@author: SIA
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime


######################################################################## 
def GetMatchupInfo(date = "20150521"):
    """Obtain a dataframe of all the matchups of one day"""
    #game_date = datetime.datetime(2015,5,21)
    game_date = datetime.datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))
    day = str(game_date).split(' ')[0]
    day = str(day).replace('-','')
    href_link = []
#    info_data = pd.DataFrame(columns=["Date", "GameName", "GameNumber",
#                                  "FirstName", "LastName", "Set1", "Set2", 
#                                  "Set3", "Set4", "Set5", "Opening", "Closing"])
    column_names = ["Date", "GameNumber","GameTime", "Name",
                                  "Set1", "Set2", "Set3", "Set4", "Set5", 
                                  "Closing", "Opening"]

    info_data = pd.DataFrame(columns = column_names, dtype = "str")
    # Get the summary link
    html = urlopen("http://feeds.donbest.com/ScoresWebApplication/servicePage."+
    "jsp?type=SCHED&leagueId=12&schedDate="+day+"&subscr=1")
########################################################################
    # If there is no data for this date
########################################################################  
    bsObj_org = BeautifulSoup(html, "lxml")
    test = bsObj_org.findAll(name ="a",  attrs= {"id": "summaryLink"})
    if test == []:
        print("There is no data availble in this day: ", date)
    
    else:
        for i in test:
           # print (i["href"])
            url = "http://feeds.donbest.com/"+ str(i["href"])
            href_link.append(url)
    ########################################################################
        # If there is no summary link for that day
    ########################################################################             
        if href_link == []:
            print("There is no data availble in this day: ", date)
        else:
    ########################################################################
            # Should record gamename in here
            # Be careful, date like 20100503, they fuck up the name of the tennis game
            # What if there is no name for gamename variable?
    ########################################################################     
            for i in href_link:
                href_html = urlopen(i)
                bsObj_href = BeautifulSoup(href_html, "lxml")
        
                # Get Game number, scores of the sets and closing lines 
                part = bsObj_href.findAll(name = "td", attrs = {"class":"scores-greybg"})
                player1 = part[0:9]    
                player2 = part[9:18]
        ########################################################################
            # Can we use feature in the html struture instead of hard code it ?
        ######################################################################## 
                player1_opening = part[-4].get_text()
                player2_opening = part[-2].get_text()
                
                
                player1_info = [day]
                player2_info = [day]
                for i in range(len(player1)):
                    player1_info.append(player1[i].get_text())
                    player2_info.append(player2[i].get_text())
                
                # Appending the opening line in the end
                player1_info.append(player1_opening)
                player2_info.append(player2_opening)        
        
                
                
                player1_info = pd.DataFrame(player1_info, dtype = "str").T
                player1_info.columns = column_names       
          
                player2_info = pd.DataFrame(player2_info, dtype = "str").T
                player2_info.columns = column_names
                
                info_data = info_data.append(player1_info)
                info_data = info_data.append(player2_info)
        ########################################################################
            # Is it prosible to append two in the sametime ?
        ######################################################################## 
                info_data = info_data[column_names]
            
            return(info_data)
            
        

