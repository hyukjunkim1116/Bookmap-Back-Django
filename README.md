# BookMap

## 프로젝트 소개

BookMap은 책에 관심이 많은 유저들을 대상으로한 커뮤니티 사이트입니다. 게시글 작성,수정,삭제 및 댓글을 통해 다른 유저들과 소통할 수 있으며 책 검색 기능을 탑재하여 원하는 책을 검색해 볼 수 있습니다. 또한 검색한 책이 어떤 서점에 몇권 있는지 확인할 수 있습니다.

## 시작 가이드

##### 1. Set-ExecutionPolicy RemoteSigned(Using Window)

##### 2. 파이썬 3.12.1 설치(파이썬 경로 체크)

##### 3. pip install virtualenv

##### 4. virtualenv venv -p python3.12.1

##### 5. .\venv\Scripts\activate or source venv/bin/activate // (deactivate)

##### 6. pip install -r requirements.txt

##### 7. python manage.py makemigrations

##### 8. python manage.py migrate

##### 9. python manage.py runserver

---

## Requirements

- [Python](https://www.python.org/)

---

## Stacks 🐈

### Environment

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)

### Communication

<img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white">

---

## 주요 기능 📦

### 회원가입,로그인

### 게시글 작성, 댓글 작성

### 좋아요,싫어요,구독,검색

### 결제

### 채팅,알림

### 신고

---

## 아키텍쳐

### 디렉토리 구조

```
foodmap-django
├─ .gitignore
├─ README.md
├─ manage.py
├─ templates
│  └─ users
├─ config
├─ payments
├─ posts
├─ reports
├─ requirements.txt
├─ users
└─ webchat

```

## API 명세

### [API 명세](https://denim-knot-470.notion.site/055b7ca4a10142f8a5a049d941b84455?v=dd168a4580ad4328afa9d36a5da7c49c&pvs=4)
