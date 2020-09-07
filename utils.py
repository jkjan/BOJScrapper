from math import ceil

from seleniumrequests import Chrome
import sys
import time

# 중복 피하기 위함
solved_problems = {}

# 웹 드라이버
webdriver = None

# 기본 주소
base_url = 'https://www.acmicpc.net'

# 현재 페이지
cur_page = 1

# 총 페이지
total_page = 0

# 에러 리스트
err_list = []

# 확장자 리스트
extensions = {
    'C': '.c',
    'C (Clang)': '.c',
    'C11': '.c',
    'C11 (Clang)': '.c',
    'C++': '.cpp',
    'C++ (Clang)': '.cpp',
    'C++11': '.cpp',
    'C++11 (Clang)': '.cpp',
    'C++14': '.cpp',
    'C++14 (Clang)': '.cpp',
    'C++17': '.cpp',
    'C++17 (Clang)': '.cpp',
    'Python 2': '.py',
    'Python 3': '.py',
    'Pypy': '.py',
    'Pypy 3': '.py',
    'Java': '.java',
    'Text': '.txt'
}

def sign_in(id, pw):
    # id 입력
    username = webdriver.find_element_by_name("login_user_id")
    username.clear()
    username.send_keys(id)

    # password 입력
    password = webdriver.find_element_by_name("login_password")
    password.clear()
    password.send_keys(pw)

    # 로그인 버튼 클릭하기
    webdriver.find_element_by_id("submit_button").click()

    # 사용자가 리캡차 풀 동안 기다리기
    input("리캡차를 다 푸신 후 아무 문자나 입력해주세요. : ")
    sys.stdout.write("로그인 성공!\n\n")


def get_page():
    global cur_page, err_list
    sys.stdout.write("현재 페이지 : %d/%d\n" % (cur_page, total_page))

    for i in range(1, 21):
        trs = webdriver.find_elements_by_tag_name("tr")
        solved_id = trs[i].find_element_by_tag_name("td").text
        solved_problem = trs[i].find_element_by_class_name('problem_title').text

        # 중복 무시, 가장 최근에 푼 것만 허용
        if solved_problem not in solved_problems:
            solved_problems[solved_problem] = solved_id
            lang = trs[i].find_elements_by_tag_name("td")[6].text[0:-5]
            sys.stdout.write("채점 번호 : " + solved_id + " | 문제 번호 : " + solved_problem + " | 언어 : " + lang + "\n")
            trs[i].find_element_by_link_text('수정').click()
            time.sleep(2)
            try:
                get_code(solved_problem, lang)
            except:
                err_list.append((solved_id, solved_problem))

    # 다음 페이지로 이동
    webdriver.find_element_by_id('next_page').click()
    cur_page += 1
    time.sleep(3)
    sys.stdout.write("\n")


def get_statics(i):
    # 유저 정보로부터 통계 값 알아내기
    user_info = webdriver.find_element_by_id("statics")
    table = user_info.find_element_by_tag_name("tbody")
    trs = table.find_elements_by_tag_name("tr")
    td = trs[i].find_element_by_tag_name("td")
    a = td.find_element_by_tag_name("a")
    return a


def init():
    # 드라이버 얻기
    global webdriver
    driver_path = open("driver_path.txt", "rt")
    webdriver = Chrome(driver_path.readline())


def report():
    # 완료 보고
    sys.stdout.write("모든 작업이 끝났습니다.\n")
    sys.stdout.write("%d개의 에러가 발생했습니다 :\n" % len(err_list))
    for err in err_list:
        sys.stdout.write("채점 번호 : " + err[0] + " | 문제 번호 : " + err[1] + "\n")


def predict_time_required(cnt, solved_cnt):
    # 예상 소요시간
    global total_page
    total_page = ceil(cnt/20)
    predicted_sec = solved_cnt * 4 + total_page-1 * 3
    predicted_sec = int(predicted_sec)
    predicted = time.strftime('%-H시간 %-M분 %-S초', time.gmtime(predicted_sec))
    sys.stdout.write("예상 소요시간 : " + str(predicted) + "\n")


def boj_scrapper(id, pw):
    global total_page
    init()
    target_url = base_url + '/user/' + id
    webdriver.get(target_url)
    time.sleep(2)

    # 맞은 문제 수
    solved_cnt = int(get_statics(1).text)

    # 맞았습니다 수
    ac_cnt = int(get_statics(3).text)
    predict_time_required(ac_cnt, solved_cnt)

    sys.stdout.write("맞은 문제 : %d | 맞았습니다 : %d | 페이지 수 : %d\n" % (solved_cnt, ac_cnt, total_page))

    webdriver.find_element_by_link_text("로그인").click()
    sign_in(id, pw)


    get_statics(1).click()
    time.sleep(2)

    # 스크랩 시작
    while True:
        try:
            get_page()
        except IndexError:
            break

    report()


def get_code(solved_problem, lang):
    file = open("downloaded/" + str(solved_problem) + extensions[lang], "wt")
    textarea = webdriver.find_element_by_tag_name("textarea").get_attribute('value')
    sys.stdout.write("코드 : " + textarea[:25] + "...\n\n")
    file.writelines(textarea)
    file.close()
    webdriver.execute_script("window.history.go(-1)")
    time.sleep(2)
