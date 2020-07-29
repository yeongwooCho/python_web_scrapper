# url로 부터 제목과 상단 첫 이미지를 가져와서 페이스북 preview를 보여주는데 웹상의 데이터를 긁어오는 것을 scrapper 한다. 예를 들어 휴대폰을 구매한다고 가정할때, 아마존 마켓컬리 ssg 3개의 사이트에서 그것을 확인한다. 이때 파이썬 스크립트를 만들어서 매일 매 10초마다 그 세가지 웹사이트에서 휴대폰을 찾아서 웹사이트에 올라온 가격을 비교해서 할인과 가격 상승, 하강에 대한 정보를 파이썬 웹 스크립퍼로 알아볼 수 있다. 웹사이트에서 정보를 추출하는 것이다. google에서 검색한 데이터에 대한 정보(이미지, 설명, 동영상) 들 또한 scrapper를 이용한 것이다.

# 구인구직 사이트 중 유명한 Indeed, stackoverflow가 존재한다. 여기서 구인구직에 등록되어있는 모든 페이지의 일자리 정보를 가져올 것이다. 가져온 모든 일자리를 엑셀 시트에 옮길거야

# 자 프로젝트를 설명하면

1. scrapper로 일자리를 다 가져오고
2. 페이지 링크 다 들어가고 또 일자리 가져오고
3. 이것을 반복하여 정보를 가져온 다음 엑셀 시트에 옮긴다.

# 해야할 순서

1. 먼저 url로 접근해야 하겠지. 파이썬을 써서 두 사이트로 접근할거야
2. 그런 다음 페이지가 몇 개 인지 알아야해
3. 그리고 페이지 하나씩 들어가줘야 겠지
4. 일단 indeed에서 하나 확인하는데 고급검색(맞춤검색)을 보면 한 페이지 당 검색결과를 몇 개 보여줄지 설정가능한데 50으로 설정된 url을 이용할 꺼다.
5. 두 사이트의 url을 이용할 껀데 하나씩 하나씩 끊어서 하여 결과물을 엑셀시트로 보여주자

# python requests packge : 파이썬에서 요청을 만드는 기능을 모아 놓은 것이다.

--> https://github.com/psf/requests
Python HTTP for Humans packge install
import requests
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
웹브라우져에서 https://api.github.com/user를 접속한 것과 똑같은 이야기이다.
출처: https://dgkim5360.tistory.com/entry/python-requests [개발새발로그] -->
이런식으로 url로 요청을 만들고 URL 주소로 GET 요청(request)를 보내면
서버에서는 그 요청을 받아 뭔가를 처리한 후 요청자인 나에게 응답(response)를 줬다.
https://dgkim5360.tistory.com/entry/python-requests (모듈 간단 정리)

import requests
from bs4 import BeautifulSoup

indeed_result = requests.get("https://www.indeed.com/jobs?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch")

# print(indeed_result) -> 200 is OK -> requests객체는 text, json, header, status_code 도 가져올 수 있다. 우리는 text를 가져올 것이다. print(indeed_result.text) # html 전부를 가져오는 것이다.

# 이제 이 html에서 정보를 가져올 것이다. 우리가 가져올 정보는 페이지 숫자들이다. 이것 또한 수작업이기에 beautifulsoup를 사용한다. (beautifulsoup4 -> Screen-scraping library)

# html에서 정보를 추출할 때 매우 유용한 packge, 아래 두 사이트는 설명사이트다

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# https://twpower.github.io/84-how-to-use-beautiful-soup (한국어 설명)

# 복습하면 파이썬만 사용해서 url을 가져올 수 있었다.

# 그러나 온라인에 있는 라이브 러리를 통해서 더 강력한 기능을 사용할수 있다.

# 그래서 우리는 requests를 사용한 것이고 우리의 목적은 indeed웹사이트로 가서

# html의 정보를 추출할 것이다. 추출할 정보는 페이지 숫자이다.

# 지금 우리코드는 페이지가 몇개인지 알수 없다.

# 최대 페이지를 코드에 알려줘서 페이지 20까지 갈 수 있도록 할 것이다.

# 이제 html_doc을 넣어주고, html.parser를 사용할 거라고 알려주면 돼 BeautifulSoup은 여러정보를 알수 있는데 이 경우는 html의 정보를 아는데 쓰기에 기재해줌

# indeed_soup = BeautifulSoup(html_doc, 'html.parser')

indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')

# 파싱과 파서 --> https://blog.binple.net/98

# 파서는 파싱을 하는 프로세서를 파서라고 부립니다. 즉, 파서가 파싱 작업을 하는 것. 파서(parser)란 컴파일러의 일부로서 원시 프로그램 즉, 컴퍼일러나 인터프리터에서 원시 프로그램을 읽어 들여, 그문장의 구조를 알아내는 구문 분석(parsing)을 행하는 프로그램을 말한다. 그리고 그 분석은 컴터가 알아 볼 수 있도록 내부의 표현방식을 바꿔주는 과정을 말한다. html 문서와 html을 변환해주는 컴파일러를 parameter로 보내준다.!!

# print(indeed_soup)

# indeed_soup.title # Bring title tag

# indeed_soup.p # Bring p tag

# indeed_soup.p['class'] # p tag의 특정 클래스도 들고 올 수 있다.

# indeed_soup.find_all('a') # a tag 싹다 들고 와라 (a = anchor : 닻)

# # find_all의 경우 모든 링크의 리스트를 반환하기에 편리하게 이용가능하다.

pagination = indeed_soup.find("div", {'class': 'pagination'}) # <div class='pagination>를 찾는다.

# print(pagination) 해당 페이지중 div class pagination안에 span class pn 의 마지막이 20임을 확인하였다.

links = pagination.find_all('a')

# print(links) # links는 리스트다. find_all은 list를 반환한다 다시 말해서, indeed_soup의 find를 써서 찾은 결과를 pagination 변수에 넣어줬는데 거기서 리스트를 만들어서 links 변수에 넣어 준것이다

# for link in links:

# print(link.find('span')) # 마지막 데이터는 다음기호를 의미한다. 자 이제 정보를 찾아왔어. 나머지는 파이썬의 함수로 제일 큰 수를 뽑아내면 돼! 마지막 데이터 지워주자!!

pages = []
for link in links[:-1]:

# pages.append(link.find('span')) # soup.title.string 에 근거하여 tag 안의 string만 가져올 수 있다.

# pages.append(link.find('span').string)

pages.append(int(link.string)) # 위와 같은 결과가 나온다.

# 이유는 anchor tag 안에 다른 요소가 있고 그 요소에 string이 오직 하나 있다면 그냥 anchor에서 string메소드를 바로 실행하면 BeautifulSoup이 알아서 string찾는다.

max_page = pages[-1]

# 여기까지 복습해보자 requests 와 bs4를 import 해주었고, 얘들이 무슨 일을 하는 지 배웠다. 우리는 해당 웹페이즈의 url을 request로 get하여 indeed_result 변수에 넣었다. 그리고 페이지의 수에 대한 정보 수집을 위해 soup를 만들어 주었다. 여기서 soup 객체는 어떤 데이터를 편하게 찾도록 도와주는 class object이다. 우리는 이 soup 객체로부터 데이터를 탐색하고 추출하였다. pagination 또한 조금더 세부적인 soup이고, 그렇기에 fina_all함수를 사용하였다. 그리고 그 links 안의 link들에서 span tag를 찾았고 pages 테이블에 저장하였다.

# 이제 1, 2, 3 페이지의 url을 확인하면 limit와 start가 나온다. start 는 50 \* page의 index 가 된다. (page, start) 는 (2, 50), (3, 100) 이다. 이제 페이지를 계속해서 request하는 방법을 알아봐야해! 왜냐하면 결국 20개의 페이지를 요청한다는 것이 20개의 페이지에 들어간다는 의미와 일맥상통하니깐!! max_page를 알았으니 20개의 request를 만들어보자!!

# 이번시간에는 request를 여러개 만들어 보자. 수동으로 request를 보낼것이다. 최대 페이지 수만큼 request를 보내볼 건데 그것을 위해 range를 이용해보자 range의 현재값을 indeed에서 가져온 요소 개수만큼 곱해줄거야 그리고 해당 url의 start형식을 맞춰줄것이다. https://www.indeed.com/jobs?q=python&limit=50&radius=25&start=150

for n in range(max_page):
print(f"start={n\*50}") # 이게 우리가 요청할 값이다.

# f-string 출력형식은 중괄호 안을 변수로 인식한다. https://bluese05.tistory.com/70 (python3.7부터 지원)

# 이제 파일을 나누어서 사용해보자
