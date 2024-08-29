import requests, re, datetime

from bs4 import BeautifulSoup

request_domain = "https://vxvault.net/"

raw_data = requests.get("https://vxvault.net/ViriList.php",verify=False).text

soup = BeautifulSoup(raw_data, "html.parser")

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

data = soup.find("table")
rows = data.findAll('tr')

for tr in rows:
    cols = tr.findAll('td')
    if len(cols) == 5:
        date = cols[0].text
        detail_link = request_domain + cols[0].find('a').get("href")
        file_web = requests.get(detail_link, verify=False).text
        md5 = re.search(r'\s([A-Fa-f0-9]{32})', file_web).group(0).strip()
        sha1 = re.search(r'\s([A-Fa-f0-9]{40})', file_web).group(0).strip()
        sha256 = re.search(r'\s([A-Fa-f0-9]{64})', file_web).group(0).strip()
        link_VT,link_TR = cols[4].find_all('a')[0].get('href'), cols[4].find_all('a')[1].get('href')
        if f'{str(today.month)}-{str(today.day)}' in date or f'{str(yesterday.month)}-{str(yesterday.day)}' in date:
            print(f"{md5},{sha1},{sha256},{link_VT},{link_TR}")
