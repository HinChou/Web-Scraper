# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 22:11:52 2016

@author: hinnc
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
import pandas as pd
import re
import matplotlib.pyplot as plt


def getURL(station, house_type, page):
    url = '/'.join(['http://sh.58.com', station, 'chuzu', house_type, 'pn'])
    url = url + str(page)
    return(url)
# getURL('dongchangzhanditiekou', 'j1', 1)

def getHouseData(station, house_type, num_page):    
    house_table = []
    
    for i in range(1, num_page + 1):
        
        url = getURL(station, house_type, i)
        print(url)
        try:
            byte_cont = urlopen(url)
            content = BeautifulSoup(byte_cont, "lxml")
            house_tags = content.findAll(name = 'h2')
            if house_tags == []:
                print("There is no house data availble in this url: ", url)
            else:
                links = re.findall('a href=\"(.*?)\"', (str(house_tags)))
                titles = re.findall('>(.*?)<\/a>', (str(house_tags)))
            
            # Get Useful Information from URL    
            room_tags = content.findAll(name = 'p', attrs  =  {'class': 'room'})
            room_info = [room.get_text().split()[0] for room in room_tags]
            area = [room.get_text().split()[1] for room in room_tags]
            area = re.findall('([0-9]+[\.]*[0-9]*)', str(area))
            area = list(map(float, area))
            
            time_tags = content.findAll(name = 'div', attrs  =  {'class': 'sendTime'})
            time_info = [time.get_text().strip() for time in time_tags]
            
            rent_tags = content.findAll(name = 'div', attrs  =  {'class': 'money'})
            rent_info = [rent.get_text().strip() for rent in rent_tags]
            rent_info = re.findall('([0-9]+[\.]*[0-9]*)', str(rent_info))
            rent_info = list(map(float, rent_info))
                                 
        except URLError as e:
            print('The URLError Is:', e)            
        except Exception as e:
            print('Catch An Exception: ', e)
         
        house_data = pd.DataFrame({'Title': titles, 'Room_Type': room_info, 
                                   'Area(㎡)': area, 'Publish_Time': time_info, 
                                   'Rent(CNY/Mon)' : rent_info, 'Link': links})
        print(house_data.shape)
        
        house_table.append(house_data)
    
    house_result = pd.concat(house_table, ignore_index = True)
    return(house_result)
# house = getHouseData('dongchangzhanditiekou', 'j1', 5)

# Sorting method
def sortHouseData(house_tata, by_area = True, by_rent = False):
    if by_area & by_rent == False:
        house_tata.sort_values('Area(㎡)', ascending = False, inplace = True)
        return(house_tata)
        
    elif by_rent & by_area == False:
        house_tata.sort_values('Rent(CNY/Mon)', ascending = True, inplace = True)
        return(house_tata)
    # Sort by_rent first and then by_area    
    elif by_area & by_rent:
        house_tata.sort_values(['Rent(CNY/Mon)', 'Area(㎡)'], 
                               ascending = [True, False], inplace = True)
        return(house_tata)    
# house_d = sortHouseData(house, by_rent = True)       

# Graph of rent and area
house.hist('Rent(CNY/Mon)')

house.hist('Area(㎡)', bins= 200)
plt.xlim((0,80))