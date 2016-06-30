# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 12:09:20 2016

@author: Hin
"""

import pandas as pd
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime

def getPitcherVSBatterTable(season, page): 
    url = 'http://mlb.mlb.com/pubajax/wf/flow/stats.splayer?season='+str(season)+
    '&sort_order=%27desc%27&sort_column=%27fpct%27&stat_type=fielding&page_type=SortablePlayer'+
    '&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000&recSP='+str(page)+'&recPP=50'
    
    resp = urllib2.urlopen(url).read()
    
    try:
       content = re.findall('\[(.+?)\]', resp)
    except ValueError:
#        print("Oops!  That was no valid number. pitcher_id:"+str(pitcher_id)+' team_id: '+str(team_id))
        return(pd.DataFrame())
    if(not len(content)):
        return(pd.DataFrame())
    content = content[0]
    rows = re.findall('\{(.+?)\}', content)   
    
    #creates table heading
    r_0 = rows[0]
    r_0 = r_0.replace('""', '"NA"')
    cols = re.findall('"(.+?)":"(.+?)"', r_0)
    
    col_names = []
    for el in cols:
        col_names = col_names + [el[0]]
        
    d_f = pd.DataFrame(index = range(len(rows)), columns = col_names)
        
    for i in range(len(rows)):
        row = rows[i]    
        row = row.replace('""', '"NA"')
        cols = re.findall('"(.+?)":"(.+?)"', row)
        for j in range(len(cols)):
            d_f.iloc[i,j] = cols[j][1]
            
    return(d_f)



def loopMatrix(season, page):
    fin_df = pd.DataFrame()
#    for k in range(len(season)):
 #       print('season: ' + str(season[k]))
    for i in range(len(page)):
 #           df_i = getPitcherVSBatterTable(season[k], pitchers_ids[j], teams_ids[i])
            df_i = getPitcherVSBatterTable(season, page[i])
            if df_i.empty:
                continue
            fin_df = df_i if fin_df.empty else fin_df.append(df_i)    
            
    return(fin_df)
                

#Initialized page and season               
page = range(1,27)
season = 2015                   

# Call function "loopMatrix" to get the well formatted data
data_2015 = loopMatrix(season, page)

                
                
