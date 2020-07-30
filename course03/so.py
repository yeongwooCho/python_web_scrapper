import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 's-pagination'})
    pages = pagination.find_all('a')

    return int(pages[-2].get_text(strip=True))
    # return int(links[-1].find('span').string)


def extract_job(html):
    title = html.find('a', {'class': 's-link'})['title']
    # print(title)

    # recursive = False 는 첫번째 단계의 span만 가져올 수 있음을 의미한다.
    # 그리고 반환이 리스트 형식이기에 다음과 같이 반환 가능하다. unpacking라고 한다.
    company, location = html.find(
        'h3', {'class': 'mb4'}).find_all('span', recursive=False)

    # print(company.string, location.string) # 결과는 잘나오나 공백이 지저분하다.
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)

    job_id = html['data-jobid']

    return {'title': title, 'company': company, 'location': location, 'link': f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page):
    jobs = []

    for page in range(last_page):
        print(f"Scrapping SO: Page : {page}")
        result = requests.get(f'{URL}&pg={page+1}')
        soup = BeautifulSoup(result.text, 'html.parser')

        results = soup.find_all('div', {'class': '-job'})
        for result in results:
            # print(result['data-jobid'])
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
