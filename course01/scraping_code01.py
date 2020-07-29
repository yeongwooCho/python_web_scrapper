import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=python&limit={LIMIT}"

result = requests.get(URL)
# print(result.text) # html문서를 다 가져온다.
soup = BeautifulSoup(result.text,"html.parser")

pagination = soup.find('div',{'class': 'pagination'})
links = pagination.find_all('a')

pages = []
for link in links[:-1]:
    pages.append(int(link.string))
    # pages.append(link.find('span').string)

max_page = pages[-1]
print(max_page)

for page in range(max_page):
    print(f"&start={page*50}")