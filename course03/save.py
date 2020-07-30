import csv

# CSV(Comma Separated Values) 파일에 데이터를 저장하자
# CSV파일은 column을 comma로 나누어 주고, 각 row는 new line 로 구분해줘


def save_to_file(jobs):
    # https://livedata.tistory.com/18 --> 인코딩을 utf-8로 전체파일을 읽어야 UnicodeEncodeError: 'cp949'가 발생하지 않는다!!!!!
    with open("jobs.csv", 'w', -1, 'utf-8') as f: 
        writer = csv.writer(f)
        writer.writerow(['title', 'company', 'location', 'link'])

        for job in jobs:
            writer.writerow(list(job.values())) 
            # values 만 dict-value 형식으로 반환되어, list형식으로 바꾸어 준 다음 write하게 된다.
    