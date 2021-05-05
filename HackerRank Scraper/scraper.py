from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def get_url(search_term):
    temp = 'https://www.hackerrank.com/{}?hr_r=1'
    search_term = search_term.replace(' ','+')
    return temp.format(search_term)

def main(search_term):
    global userdata_list
    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = get_url(search_term)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    fname = soup.find('h1',{'class':'profile-heading'}).text[:]
    
    badges = soup.find_all('text',{'class':'badge-title'})
    
    badges_list = []
    for badge in badges:
        badges_list.append(badge.text[:])
    
    stars = soup.find_all('g',{'class':'star-section'})
    
    stars_list = []
    for res in stars:
        res = str(res)
        count=re.findall('class="badge-star"',res)
        stars_list.append(len(count))
    
    
    badge_stars = dict()
    for i,j in zip(badges_list,stars_list):
        badge_stars.update({i:j})
        
    
    badge_stars = str(badge_stars)[1:-1]

    userdata_list.append((search_term,fname,badge_stars))
    
    driver.close()

if __name__ == "__main__":
    users = pd.read_csv("users.csv")
    userdata_list=[]
    for user in users.username:
        main(user)

    userdata_ = pd.DataFrame(userdata_list,columns=['Username','Fullname','Badges and Stars'])
    userdata_.to_csv("usersdata.csv")
    userdata_.to_html("usersdata.html")