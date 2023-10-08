#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1.Extract United Nations press releases containing “crisis”:

import requests
from bs4 import BeautifulSoup

base_url = "https://press.un.org"
seed_url = "https://press.un.org/en"

def is_press_release(soup):
    """Check if the page is a press release based on the 'PRESS RELEASE' link."""
    anchor = soup.find('a', hreflang='en', href="/en/press-release")
    return anchor is not None

def get_press_releases_with_crisis(seed_url, part_number, limit=10):
    a = set()
    b = [seed_url]
    press_releases = []

    while b and len(press_releases) < limit:
        url = b.pop(0)
        if url in a:
            continue

        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        if is_press_release(soup) and "crisis" in soup.get_text().lower():
            press_releases.append(url)

            with open(f"{part_number}_{len(press_releases)}.txt", 'w', encoding='utf-8') as file:
                file.write(response.text)
            a.add(url)

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/'):
                full_link = base_url + link['href']
                if full_link not in a:
                    b.append(full_link)

    return press_releases

press_releases = get_press_releases_with_crisis(seed_url, 1, 10)
for pr in press_releases:
    print(pr)


# In[2]:


# 2. Crawl the press room of the European Parliament.


from bs4 import BeautifulSoup
import urllib.request

seed_url = "https://www.europarl.europa.eu/news/en/press-room"
urls = [seed_url]
seen = {seed_url}
opened_press = set()
min_links = 10
press_count = 0

while len(urls) > 0 and press_count < min_links:
    try:
        curr_url = urls.pop(0)
        request = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        a = soup.find('span', class_="ep_name", text='Plenary session')
        b = soup.find('span', class_="ep_name", text='Press Releases')
        if a and b:
            text = soup.get_text()
            if 'crisis' in text.lower():
                press_count += 1
                opened_press.add(curr_url)
                with open(f"2_{press_count}.txt", 'w', encoding='utf-8') as file:
                    file.write(str(soup))
    except:
        continue

    for a_tag in soup.find_all('a', href = True):
        org_child_url = a_tag.get('href')
        child_url = urllib.parse.urljoin(seed_url, org_child_url)
        if child_url not in seen and seed_url in child_url:
            seen.add(child_url)
            urls.append(child_url)

print("European Parliament press releases containing the word crisis")
for link in opened_press:
    print(link)


# In[ ]:




