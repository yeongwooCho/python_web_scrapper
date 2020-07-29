import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():  # 최대 페이지 수를 반환하는 함수
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {'class': 'pagination'})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    # title = html.find('h2', {'class':'title'})
    # anchor = title.find('a')['title'] # 여기서 title은 attribute(속성)이다.
    # print(anchor) # 정상적으로 직무를 가져왔다. 한방에하자
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    # print(title)
    # 이제 company를 들고오자. 이 경우 회사이름에 a 가 있는게 있고 span으로만 추가된것이 있다.
    company = html.find('span', {'class': 'company'})
    # if company.find('a') is not None:
    #     print(company.find('a').string)
    # else :
    #     print(company.string)

    if company:
        company_anchor = company.find('a')
        if company_anchor is not None:
            company = str(company_anchor.string).strip()
        else:
            company = str(company.string).strip()
    else:
        company = None

    # string로 긁어올때 display가 none인 것들이 있지만, data-rc-loc 속성에 주소가 존재한다.
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']

    # 해당 란을 클릭하면 링크로 연결된 정보가 나온다
    # &vjk=84a541c104b5b24c 이런 식으로 해당 링크가 아이디로 메겨져있고 html의 속성 data-jk다
    job_id = html['data-jk']

    return {'title': title, 'company': company, 'location': location, 'link': f"{URL}&vjk={job_id}"}


# request를 20개, 50개 처럼 원하는 만큼 만들어 주는 함수를 만들어 가독성을 높히자!!
# request를 어떻게 만들까?
# print문을 request.get()로 하여 request를 발생시키자!!
def extract_indeed_jobs(last_page):  # parameter에 최대 페이지 개수를 받는다
    jobs = []
    for page in range(last_page):
        print(f'Scrapping page {page}')
        # print(f"start={page*LIMIT}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        # print(result) #200OK
        # print(result.status_code) # 200은 정상적 통신을 의미한다.

        # 일자리에 대한 정보를 추출하기 위해 beautifulsoup을 사용한다. 이제 일자리 추출하는 것만 하면 된다.
        soup = BeautifulSoup(result.text, 'html.parser')

        # results는 soup를 사용했기에 html리스트이다.
        results = soup.find_all('div', {'class': "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)  # result는 html을 갖고있기에
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page()
    # print(max_indeed_pages) # 20이 정상 출력이 된다.
    jobs = extract_indeed_jobs(last_page)
    return jobs
