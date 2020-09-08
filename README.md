## 백준 스크래퍼 (BOJ Scrapper)

### 사용법
1. 크롬을 설치합니다.
2. 설치된 크롬의 [버전을 확인]("chrome://version")합니다.
3. 버전에 맞는 [크롬 드라이버]("https://chromedriver.chromium.org/downloads") 를 설치합니다.
4. 최상단에 `downloaded` 폴더를 생성합니다.
5. `pip install selenium-requests`로 필요한 라이브러리를 설치합니다.
6. `driver_path.txt` 파일 생성 후, 설치된 드라이버의 절대 경로를 적습니다.
7. `python scrap.py`로 파이썬 파일을 실행합니다.
8. `downloaded` 폴더를 확인합니다.

&nbsp;

### 지원되는 언어
1. C
2. C (Clang)
3. C11
4. C11 (Clang)
5. C++
6. C++ (Clang)
7. C++11
8. C++11 (Clang)
9. C++14
10. C++14 (Clang)
11. C++17
12. C++17 (Clang)
13. Python 2
14. Python 3
15. Pypy
16. Pypy 3
17. Java
18. Text

&nbsp;

### 주의점
1. 일반적인 스크래퍼가 아닌 크롬을 조작하는 일종의 매크로입니다.
2. 따라서 속도가 매우 느립니다.
3. 사용 중 페이지를 이동하면 안 됩니다.
4. 번호가 같은 문제가 있다면 가장 최근에 푼 문제만 저장됩니다.

&nbsp;

### 예상 소요시간 계산법
페이지 수 = ceil(맞았습니다/20)
&nbsp;

소요시간 = 맞은 문제x4 + 페이지 수x3 (초)