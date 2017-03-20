# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 21:10:40 2016

@author: hinnc
"""

from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from multiprocessing import Pool
import pandas as pd
import re


# SCNU 华师
#url = "http://career.scnu.edu.cn/Recruitment/index"
#url= 'http://career.scnu.edu.cn/Thinkcareer/index.php/Recruitment/select'
def teacherCareerSCNU(url, today, yesterday):   
    try:
        url_info = urlopen(url)
        career_info = BeautifulSoup(url_info, "lxml")
        url_info = career_info.findAll(name = 'a')
        id_name_job_date_views = career_info.findAll(name = 'td')
        
        if url_info == []:
            print("There is no websites data availble in this url: ", url)
            
        else:
            links = re.findall('a href=\"(.*?)\"', (str(url_info)))
            links = [link for i, link in enumerate(links) if i % 2 == 0]
            id_and_name = [v.get_text() for i, v in enumerate(url_info)]
            job_id = [ID for i, ID in enumerate(id_and_name) if i % 2 == 0]
            company = [name for i, name in enumerate(id_and_name) if i % 2 == 1]
        if id_name_job_date_views == []:
            print("There is no data availble in this url: ", url)
            
        else:
            job = []
            dates = []
            views =[]
            i = 2
            while i < len(id_name_job_date_views):
                job.append(id_name_job_date_views[i].get_text())
                dates.append(id_name_job_date_views[i+1].get_text())
                views.append(id_name_job_date_views[i+2].get_text())
                i += 5

        career_table = pd.DataFrame({'编号': job_id, '单位名称': company, '招聘职位': job, 
                                     '发布时间': dates, '浏览量': views, '网址': links}) 
        
        # Find all the employments info of teachers in the job name column
        bool_table = career_table['招聘职位'].str.contains('教师|老师')
        
        teacher_table = career_table.ix[bool_table].reset_index(drop=True)
        
        teacher_table.sort_values('发布时间', ascending = False, inplace = True)
        
        # Only care about '深圳|广州'
        gzsz_career = teacher_table['单位名称'].str.contains('深圳|广州')
        gzsz_career = teacher_table.ix[gzsz_career].reset_index(drop=True)
        
        # Extract the career info only was issued yesterday and today
        new_scnu_jobs = gzsz_career[(gzsz_career['发布时间'] == today) |
                                         (gzsz_career['发布时间'] == yesterday)]
        
        return(new_scnu_jobs)    
                              
    except URLError as e:
        print('The URLError Is:', e, '\n', 'URL: ', url)            
    
    except Exception as e:
        print('Catch An Exception: ', e, '\n', 'URL: ', url)                            

# shenzhenjiaoshi.com 深圳教师招聘网
#url = 'http://www.shenzhenjiaoshi.com/zhaopin/'
def teacherCareerSZJS(url, today, yesterday):
    shenzhen_career = []
    
    areas = ['gongbanxuexiao','longhuaqu','dapengqu','pingshan','baoanqu',
            'nanshanqu','futianqu','yantianqu','luohuqu', 'longgangqu' , 
            'guangmingxinqu']
                
    for area in areas:        
        try:
            shenzhen_url = urlopen(url + area)
            shenzhen_info = BeautifulSoup(shenzhen_url, "lxml")
            shenzhen_info = shenzhen_info.findAll(name = 'li')
            
            shenzhen_date = re.findall('<span>(.*?)</span>', str(shenzhen_info))
            shenzhen_company = re.findall('\">(.*?)</a>', str(shenzhen_info))[:len(shenzhen_date)]
            shenzhen_link = re.findall('<a href=\"(.*?)\" title=', str(shenzhen_info))[:len(shenzhen_date)]
            shenzhen_link = ['http://www.shenzhenjiaoshi.com'+ link for link in shenzhen_link]
            #shenzhen_jobid = [jobid for url in shenzhen_link for jobid in re.findall('\d+', url)]
            if 'gongbanxuexiao' in (url + area):
                shenzhen_job = '深圳教师招聘网_公办'
                
            else:
                shenzhen_job = '深圳教师招聘网_民办_' + area
            
            shenzhen_views = 'Unknown'
            shenzhen_jobid = 'Unknown'

            shenzhen_table = pd.DataFrame({'编号': shenzhen_jobid, '单位名称': shenzhen_company, 
                                       '招聘职位': shenzhen_job, '发布时间': shenzhen_date, 
                                       '浏览量': shenzhen_views, '网址': shenzhen_link}) 
                
            shenzhen_career.append(shenzhen_table)
        
        except URLError as e:
            print('The URLError Is:', e, '\n', 'URL: ', url)        
        
        except Exception as e:
            print('Catch An Exception: ', e, '\n', 'URL: ', url)
    
    shenzhen_career = pd.concat(shenzhen_career, ignore_index = True)    
    shenzhen_career.sort_values('发布时间', ascending = False, inplace = True)
    
    # Extract the career info only was issued yesterday and today
    new_shenzhen_career = shenzhen_career[(shenzhen_career['发布时间'] == today) |
                                         (shenzhen_career['发布时间'] == yesterday)]
    
    return(new_shenzhen_career)                                      
                                                                      
# 华图教师 - 深圳
#url = 'http://www.hteacher.net/shenzhen/jiaoshizhaopin/zp/'
def teacherCareerHTJS(url, today, yesterday):
    try:
        huatu_url = urlopen(url)
        huatu_info = BeautifulSoup(huatu_url, "lxml")
        huatu_info = huatu_info.findAll(name = 'li')
        
        huatu_date = re.findall('<span>(.*?)</span>', 
                                      str(huatu_info))
        huatu_date = ['-'.join(re.findall('\d+', ele)) for ele in huatu_date if re.findall('\d+', ele) != []]
         
        huatu_link = re.findall(']</a> <a href=\"(.*?)\" target=', 
                                      str(huatu_info))   
        huatu_link = ['http://www.hteacher.net'+ link for link in huatu_link]     
        
        huatu_company = re.findall(']</a> <a href=\"(.*?)<span>', 
                                          str(huatu_info))
            
        huatu_company = [company for ele in huatu_company for company in re.findall('target=\"_blank\">(.*?)</a>', 
                                          str(ele))]
               
        huatu_job = '华图教师网' 
        huatu_views = 'Unknown'
        huatu_jobid = 'Unknown'
        
        huatu_career = pd.DataFrame({'编号': huatu_jobid, '单位名称': huatu_company, 
                                       '招聘职位': huatu_job, '发布时间': huatu_date, 
                                       '浏览量': huatu_views, '网址': huatu_link}) 
        
        huatu_career.sort_values('发布时间', ascending = False, inplace = True)
    
        # Extract the career info only was issued yesterday and today
        new_huatu_career = huatu_career[(huatu_career['发布时间'] == today) |
                                         (huatu_career['发布时间'] == yesterday)]     
                                      
        return(new_huatu_career)                                                                            
                                                                                    
    except URLError as e:
        print('The URLError Is:', e, '\n', 'URL: ', url)      
    
    except Exception as e:
        print('Catch An Exception: ', e, '\n', 'URL: ', url) 
                                                                     
## 罗湖教育应用网
#url = 'http://www.luohuedu.net/news/zhaopin1.aspx?gonggaofenlei=1'
def teacherCareerLHJY(url, today, yesterday):    
    try:
        luohu_url = urlopen(url)
        # Special encoding method for certain Chinese websites
        luohu_info = BeautifulSoup(luohu_url, "lxml", from_encoding = 'gb18030')
        luohu_info = luohu_info.findAll(name = 'td')
        
        luohu_link = re.findall('<a href=\"(.*?)\" target=', str(luohu_info))
        luohu_link = [link.replace('amp;', '') for link in luohu_link]
        luohu_link = ['http://www.luohuedu.net/news/'+ link for link in luohu_link]
        
        luohu_company = re.findall('Label3\">(.*?)</span>', str(luohu_info))
        luohu_company = [company[1:] for company in luohu_company]
        
        luohu_date = re.findall('block;\">(.*?)</span>', str(luohu_info))
        
        luohu_job = re.findall('target=\"_blank\">(.*?)</a>', str(luohu_info))
        luohu_job = [''.join(re.findall('[^<b>\s\/\"=#A-Za-z0-9]', job)) for job in luohu_job]
           
        luohu_views = 'Unknown'
        luohu_jobid = 'Unknown'
        
        luohu_career = pd.DataFrame({'编号': luohu_jobid, '单位名称': luohu_company, 
                                     '招聘职位': luohu_job, '发布时间': luohu_date, 
                                     '浏览量': luohu_views, '网址': luohu_link}) 
        
        luohu_career.sort_values('发布时间', ascending = False, inplace = True)
    
        # Extract the career info only was issued yesterday and today
        new_luohu_career = luohu_career[(luohu_career['发布时间'] == today) |
                                         (luohu_career['发布时间'] == yesterday)]
                                      
        return(new_luohu_career)  
        
    except URLError as e:
        print('The URLError Is:', e, '\n', 'URL: ', url)      
    
    except Exception as e:
        print('Catch An Exception: ', e, '\n', 'URL: ', url)                                     
                                                                            
# 中公教育
#url = 'http://gd.offcn.com/html/jiaoshi/zhaokaoxinxi/'
def teacherCareerZGJY(url, today, yesterday):
    try:
        zhonggong_url = urlopen(url)
        zhonggong_info = BeautifulSoup(zhonggong_url, "lxml")
        zhonggong_info = zhonggong_info.findAll(name = 'li')
    
        zhonggong_date= re.findall('<span>(.*?)</span>', 
                                   str(zhonggong_info))
        zhonggong_date = ['-'.join(re.findall('\d+', ele)) for ele in zhonggong_date]
        zhonggong_company = re.findall('title=\"(.*?)\">', 
                                      str(zhonggong_info))[:len(zhonggong_date)]                                  
        zhonggong_link = re.findall('<a href=\"(.*?)\" target=', str(zhonggong_info))[:len(zhonggong_date)]
        
        zhonggong_job = '中公教育网' 
        zhonggong_views = 'Unknown'
        zhonggong_jobid = 'Unknown' 
        
        zhonggong_career = pd.DataFrame({'编号': zhonggong_jobid, '单位名称': zhonggong_company, 
                                       '招聘职位': zhonggong_job, '发布时间': zhonggong_date, 
                                       '浏览量': zhonggong_views, '网址': zhonggong_link}) 
         
        zhonggong_career.sort_values('发布时间', ascending = False, inplace = True)
    
        # Only care about '深圳|广州'
        gzsz_zhonggong_career = zhonggong_career['单位名称'].str.contains('深圳|广州')
        gzsz_zhonggong_career = zhonggong_career.ix[gzsz_zhonggong_career].reset_index(drop=True)
        
        # Extract the career info only was issued yesterday and today
        new_zhonggong_career = gzsz_zhonggong_career[(gzsz_zhonggong_career['发布时间'] == today) |
                                         (gzsz_zhonggong_career['发布时间'] == yesterday)]
        
        return(new_zhonggong_career)                                  
    
    except URLError as e:
        print('The URLError Is:', e, '\n', 'URL: ', url)      
    
    except Exception as e:
        print('Catch An Exception: ', e, '\n', 'URL: ', url)
            
# 中公教师
#url = 'http://gd.zgjsks.com/html/jszp/kszx/ggxx/'
def teacherCareerZGJS(url, today, yesterday):
    try:
        zhonggong_js_url = urlopen(url)
        zhonggong_js_info = BeautifulSoup(zhonggong_js_url, "lxml")
        zhonggong_js_info = zhonggong_js_info.findAll(name = 'li')
    
        zhonggong_js_link = re.findall('</a></font><a href=\"(.*?)\" target=', 
                                    str(zhonggong_js_info))
        
        zhonggong_js_date= re.findall('<span>(.*?)</span>', 
                                   str(zhonggong_js_info))[:len(zhonggong_js_link)]
                                      
        zhonggong_js_date = ['-'.join(re.findall('\d+', ele)) for ele in zhonggong_js_date]
                            
        zhonggong_js_company = re.findall(']</a></font>(.*?)>', 
                                          str(zhonggong_js_info))
        zhonggong_js_company = [company for ele in zhonggong_js_company for company in re.findall('title=\"(.*?)\"', ele)]
                                              
        zhonggong_js_job = '中公教师网' 
        zhonggong_js_views = 'Unknown'
        zhonggong_js_jobid = 'Unknown' 
        
        zhonggong_js_career = pd.DataFrame({'编号': zhonggong_js_jobid, '单位名称': zhonggong_js_company, 
                                       '招聘职位': zhonggong_js_job, '发布时间': zhonggong_js_date, 
                                       '浏览量': zhonggong_js_views, '网址': zhonggong_js_link}) 
         
        # Delete duplicate rows
        zhonggong_js_career.drop_duplicates(inplace = True)
        
        zhonggong_js_career.sort_values('发布时间', ascending = False, inplace = True)
    
        # Only care about '深圳|广州'
        gzsz_zhonggong_js_career = zhonggong_js_career['单位名称'].str.contains('深圳|广州')
        gzsz_zhonggong_js_career = zhonggong_js_career.ix[gzsz_zhonggong_js_career].reset_index(drop=True)
        
        # Extract the career info only was issued yesterday and today
        new_zhonggong_js_career = gzsz_zhonggong_js_career[(gzsz_zhonggong_js_career['发布时间'] == today) |
                                         (gzsz_zhonggong_js_career['发布时间'] == yesterday)]
                                          
        return(new_zhonggong_js_career)                                  
    
    except URLError as e:
        print('The URLError Is:', e, '\n', 'URL: ', url)       
    
    except Exception as e:
        print('Catch An Exception: ', e, '\n', 'URL: ', url)

# Choose function for scraping
def jobCrawler(url):
    # Today and yesterday
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now().date() - timedelta(1)).strftime('%Y-%m-%d')
    
    # All urls
    scnu= 'http://career.scnu.edu.cn/Thinkcareer/index.php/Recruitment/select'
    szjs = 'http://www.shenzhenjiaoshi.com/zhaopin/'
    htjs = 'http://www.hteacher.net/shenzhen/jiaoshizhaopin/zp/'
    lhjy = 'http://www.luohuedu.net/news/zhaopin1.aspx?gonggaofenlei=1'
    zgjy = 'http://gd.offcn.com/html/jiaoshi/zhaokaoxinxi/'
    zgjs = 'http://gd.zgjsks.com/html/jszp/kszx/ggxx/'
    
    if url == scnu:
        print('Checked scnu')
        result = teacherCareerSCNU(scnu, today, yesterday)
        
    elif url == szjs:
        print('Checked szjs')
        result = teacherCareerSZJS(szjs, today, yesterday)
        
    elif url == htjs:
        print('Checked htjs')
        result = teacherCareerHTJS(htjs, today, yesterday)
        
    elif url == lhjy:
        print('Checked lhjy')
        result = teacherCareerLHJY(lhjy, today, yesterday)
        
    elif url == zgjy:
        print('Checked zgjy')
        result = teacherCareerZGJY(zgjy, today, yesterday)
        
    else:
        print('Checked zgjs')
        result = teacherCareerZGJS(zgjs, today, yesterday)
        
    return(result)

        
#######################################
if __name__ == '__main__':    
    # All urls
    scnu_url = 'http://career.scnu.edu.cn/Thinkcareer/index.php/Recruitment/select'
    szjs_url = 'http://www.shenzhenjiaoshi.com/zhaopin/'
    htjs_url = 'http://www.hteacher.net/shenzhen/jiaoshizhaopin/zp/'
    lhjy_url = 'http://www.luohuedu.net/news/zhaopin1.aspx?gonggaofenlei=1'
    zgjy_url = 'http://gd.offcn.com/html/jiaoshi/zhaokaoxinxi/'
    zgjs_url = 'http://gd.zgjsks.com/html/jszp/kszx/ggxx/'
    
    urls = [scnu_url, szjs_url, htjs_url, lhjy_url, zgjy_url, zgjs_url]    
    
    #######################################
    # Multiprocessing; using "with" can allow us without writing "mp.close()" explicitly
    with Pool(processes = 6) as mp:
        data = mp.map(jobCrawler, [url for url in urls])
    #######################################    
    # Concatenate all new issue (today and yesterday) jobs
    all_new_jobs = pd.concat(data, ignore_index = True)
    all_new_jobs.sort_values('发布时间', ascending = False, inplace = True)
    
    # Today 
    today = datetime.now().strftime('%Y_%m_%d')
    
    path = ('C:/Users/hinnc/Desktop/Today_and_Yesterday_Teacher_Employment_' 
            + today + '.xlsx')
    
    all_new_jobs.to_excel(path, sheet_name='Sheet1', index = False)              
        
    print('''
          ********************
          Program Finished!!!
          ********************
          ''')    
