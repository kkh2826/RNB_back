# RNB_back

### 프로젝트 설명
- 국내주식 시장에 상장된 종목들을 대상으로 가격 Data와 가격의 추이를 그래프로 나타내며 관심 있는 종목에 대해 즐겨찾기 및 정보를 입력함에 따라 주식 Portfolio를 구성할 수 있는 서비스

### 개발담당
- **RNB의 Backend 부분을 담당**
- **데이터 처리에 대한 API 작성**

### 주요 모듈 정리
```json
  "Python": "^3.8.5",
  "djangorestframework": "^3.12.4",
  "django": "^3.2.5",
  "djangorestframework-jwt": "^1.11.0",
```

### 주요기능
1. KOSPI / KOSDAQ 종목 리스트 및 가격정보
- https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage에 공시되어 있는 Excel 파일을 통해 주식기본정보(종목코드/종목명)를 가져온다.
- OTP 생성 및 유효한 OTP를 통해 인증 후, Excel 접근
2. 특정종목에 대한 가격리스트 (1개월, 3개월 6개월, 1년, 10년)
- PyKRX 모듈을 통한 특정종목에 대한 가격정보 추출.
3. 로그인 / 로그아웃 / 회원가입 실행
- JWT(Json Web Token) 방법을 통한 로그인과 회원가입 진행.
4. 개인별 종목관리 입력/수정/삭제 실행
5. JWT 정보를 활용한 개인정보 및 종목관리

### 로컬 Setting
- python -m venv venv (venv 가상환경 생성 - manage.py 같은 위치)
- venv\Scripts\activate (venv 가상환경 실행)
- python -m pip install --upgrade pip (pip 업그레이드 실행)
- pip install -r requirements.txt (필요한 모듈 설치 - requirements.txt에 필요한 모듈 명시)
- python manage.py makemigrations
- python manage.py migrate
### Server 실행
- python manage.py runserver
