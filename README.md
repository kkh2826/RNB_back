# RNB_back

### 설명
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
2. 특정종목에 대한 가격리스트 (1개월, 3개월 6개월, 1년, 10년)
3. 로그인 / 로그아웃 / 회원가입 실행
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
