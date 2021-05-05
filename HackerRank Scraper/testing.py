import requests
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
    headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

    url = get_url(search_term)
    webPage = requests.get(url=url,headers=headers)
    webPage = webPage.content

    soup = BeautifulSoup(webPage, 'html.parser')
    
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
    
    

if __name__ == "__main__":
    users = pd.read_csv("users.csv")
    userdata_list=[]
    for user in users.username:
        main(user)

    userdata_ = pd.DataFrame(userdata_list,columns=['Username','Fullname','Badges and Stars'])
    userdata_.to_csv("usersdata.csv")
    userdata_.to_html("usersdata.html")
    print(userdata_)
    
    
    