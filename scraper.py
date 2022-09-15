import csv
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

BASE_URL = "https://profiles.rice.edu"

All_MEMBERS_URL = f"{BASE_URL}/all-people"

page_url = All_MEMBERS_URL

all_members = []

while(page_url):
    print(f"getting members from {page_url} ...")
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    all_members_list = soup.find_all('div', class_="grid-mw--1380")
    profile_links = []
    
    for item in all_members_list:
        for link in item.find_all('a', href=True, class_="h6"):
            profile_links.append(BASE_URL + link['href'])

    for link in profile_links:
        r = requests.get(url=link, headers=headers)
        soup2 = BeautifulSoup(r.content, 'lxml')
        name = soup2.find('h2', class_="article__author-name").text.strip()

        try:
            email = soup2.find('a', class_="body").text.strip()
        except:
            email = 'no email'
        data = [name, email]
        all_members.append(data)

    next_page_li_elem  = soup.find('li', class_="pager__item--next")

    if next_page_li_elem:
        page_url = f"{All_MEMBERS_URL}{next_page_li_elem.find('a')['href']}"
    else:
        break

print(f"Total Members: {len(all_members)}")

header = ['name', 'email']

with open('members.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_members)