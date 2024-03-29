## 👨🏻‍💻Contributors

| 김동훈                                                                                         | 엄한결                                                                                                                             |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------:|
| [![](README_assets/2e2889645591e47e3e3c520252dcc740b624a344.png)](https://github.com/hun23) | [<img title="" src="README_assets/f3da24db7a9dde1e72166fa6d9ec5b24fd48360d.png" alt="" width="818">](https://github.com/ah9mon) |
| **프론트엔드**                                                                                   | **백엔드**                                                                                                                         |

<span style="color:gray">커밋 컨벤션 rule : AngularJS Commit Message Convention</span>

## 🔗 목차

- Information Architecture
- System Architecture

- 개발 핵심 기능
  - Back Server
  - Front Server

### 서비스 정보 구조 <span style="color:gray">Information Architecture</span>

![](README_assets/2023-05-25-19-40-30-image.png)

### 시스템 아키텍처 <span style="color:gray">System Architecture</span>

![](README_assets/2023-05-25-20-20-50-image.png)

- 백엔드
  
  - MSA의 개념을 토대로 기능별로 나누어 하나의 프로젝트에 하나의 앱만 있도록 구성하고
    
    통합 DB가 아닌 각각의 기능과 관련된 데이터만 들어가도록 개별의 DB를 가지도록  했다
  
  - 각각의 기능(프로젝트)를 Docker를 이용해 Container로 만들고 다수의 Container들을 통합 관리 및 실행

## ⚙️ 개발 핵심 기능

![](README_assets/2023-05-25-19-42-58-image.png)

### Back Server

> ⚙️django REST framework, Spring boot, docker, SQLite3
> 
> 📡Oauth2(Naver, Kakao), Papago API, TMDB API, Youtube API

### 🎯 목표

1. REST API 구축
   
   - URI 도 REST API URI규칙을 최대한 지켜가며 설정하기

2. API
   
   - 최대한 많은 API 사용해보며 API사용에 익숙해지기
   - OAuth2 소셜로그인을 사용해 인증과정을 구현해보기

3. MicroService Architecture (MSA)
   
   - 소규모의 프로젝트에서는 **MSA**보다는
     
     기존의 (소프트웨어의 구성요소가 한 프로젝트에 통합되어 있는 형태인)
     
     **Monolithic Architecture**가 더 효율적인 것을 알고 있지만
     
     그래도 MSA의 개념을 직접 느껴보기 위해
     
     실제 MSA가 나누는 정도보다 비교적 크더라도 기능별로 나눠보기
- 기술 스택을 기능별로 다르게 가져갈 수 있는 장점을 보여주기 위해
  
  하나의 기능은 꼭 Spring boot로 구현하기
4. Docker
   
   - 추후 해당 프로젝트를 개발, 관리, 배포를 편하게 하기위해 도커를 사용해
     
     각각의 기능의  Docker image 생성하기
   
   - 그렇게 생성된 Container들을 Docker-compose를 이용해 여러개의 Container로 이루어진 서비스를 구축 및 실행 자동화하기

#### ERD <span style="color:gray">Entity Relationship Diagram</span>

![](README_assets/2023-05-25-21-54-01-image.png)

#### URI

- REST API URI 규칙
  
  1. URI 마지막에 슬래시(/)를 붙이지 마세요
  2. 관계를 나타내기 위해 슬래시(/)를 사용하세요
  3. 하이픈(-)를 사용하세요
  4. 언더바(_)를 사용하지 마세요
  5. 소문자를 선호하세요
  6. URI에 파일 확장자를 사용하지 마세요

<img title="" src="README_assets/2023-05-25-22-01-50-image.png" alt="" width="533">

<img title="" src="README_assets/2023-05-25-22-02-11-image.png" alt="" width="627">

![](README_assets/2023-05-25-22-02-31-image.png)

![](README_assets/2023-05-25-22-03-06-image.png)

![](README_assets/2023-05-25-22-03-23-image.png)

<img title="" src="README_assets/2023-05-25-22-15-57-image.png" alt="" width="622">

<img title="" src="README_assets/2023-05-25-22-16-15-image.png" alt="" width="431">

#### 주요 기능 프로세스 <span style="color:gray">Process</span>

##### 1. Authentication, Authorization

인증 및 인가 방식은 Oauth2.0 방식인 Kakao, Naver Login API를 이용함

![](README_assets/2023-05-25-23-44-38-image.png)

##### 2. MicroService Architecture CRUD

MicroService Architecture 이기 때문에 각각이 하나의 기능만을 수행

TMDB API 서비스와 Community 서비스는 `<b>`Django Rest Framework `</b>`로

Youtube API 서비스는 **Spring boot**로 구현하여

MSA의 장점인 **기술 스택을 다르게할 수 있음**을 보였다

![](README_assets/2023-05-26-00-09-59-image.png)

##### 3. Movie Recommend

front에서 날씨 데이터를 바탕으로 Chat GPT에게 받은 추천영화 데이터를 받으면

TMDB API 서비스에서 TMDB API에 요청하고 응답 받은 정확한 영화 데이터를

저장 및 응답한다

![](README_assets/2023-05-26-00-24-00-image.png)

##### 4. Movie Search

Front에서 사용자가 검색을 위해 입력한 Text를 TMDB API서비스로 보내면

TMDB API서비스가 Papago API 서비스로 Text를 보내어 어떤 언어인지 감지하고

영어로 번역하여 DB에서 해당 (번역된)Text가 포함된 영화들을 응답한다

![](README_assets/2023-05-26-00-36-28-image.png)

### 😮‍💨 고찰 및 수정사항

9일 (23년 5월 17일 ~ 5월 25일) 정도의 짧은 기간동안 빠르게 개발해야하는 상황이어서

알고있지만 신경쓰지 못한 부분과 다 하고나서야 알게된 부분들이 많았다

이러한 부분들을 정리해놓고 수정하며 발전시켜 나갈 예정이기 때문에 정리 해놓으려 한다

- 객체지향 프로그래밍
  
  - 무작정 돌아가는 함수만 짜고 객체지향 프로그래밍은 전혀 신경 쓰지 않았다.
    
    사실 전혀 할 줄 모른다.
    
    객체지향 프로그래밍, 클린코드를 공부하고
    
    Class를 통한 추상화, 상속, 다형성, 캡슐화 4가지 특징을 살리는
    
    코드가 무엇인지 공부할 것이다.

- 코드 리팩토링
  
  - 인증과 인가 부분을 Oauth2.0을 사용하기로 결심했을 때
    
    처음에 Kakao Login API만 사용하자라고 생각했다가
    
    하나만 있으면 허전할 것 같아서 프로젝트 마감 하루전에
    
    Naver Login API도 추가했다.
    
    둘다 Oauth2.0 방식이고 프로세스가 100% 똑같기 때문에
    
    충분히 같은 함수 코드를 가지고 API url만 갈아 끼워주는 방식으로
    
    재활용 할 수 있는  코드를 작성할 수 있지만
    
    시간 부족으로 인해 빠르게 Naver login만 하는 함수를 하나 더 만들어서
    
    기능 추가를 진행했다.
    
    중복코드를 제거하고 리팩토링해야 하는 부분이 많을 것이기 때문에 수정할 것이다.

- MSA 답지 못하고 마이크로라고 부르기 너무 애매한 서비스들
  
  - 진짜 MSA는 기능 단위가 더 세부적으로 나뉘어져 있고 연결성도 더 약하다
  
  - 이번(23.05.25) 프로젝트는 어설픈 MSA이며 하나의 프로젝트로 구축하는 것이 훠얼씬 효율적이고 간결한 형태였기에 시작한 것이 후회가 조금 된다
  
  - TMDB API 서비스는 처음엔 정말 API요청만 받고 응답하는 서비스로 구상했지만
    
    결국 영화 데이터를 저장하고 처리하는 Movie 서비스가 되어 버렸고
    
    Community도 게시글, 댓글, 좋아요 기능들이 한번에 들어있는 마이크로라부르기 너무나 힘든 서비스였다

### 🤔 향후 진행 방향

- ~~docker 이미지 docker hub에 올리기~~
  - https://velog.io/@eoveol/docker-docker-hub%EC%97%90-image-%EC%98%AC%EB%A6%AC%EA%B8%B0
- ~~docker compose에서 이미지를 docker hub에서 가져오도록 하기~~ 
  - https://velog.io/@eoveol/Docker-Docker-compose%EC%8B%9C-docker-hub%EC%97%90-%EC%9E%88%EB%8A%94-image-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B2%8C-%ED%95%98%EA%B8%B0
- ~~github action으로 CI/CD 자동화 해보기~~
  - CI : https://velog.io/@eoveol/CI-Github-Action%EC%9C%BC%EB%A1%9C-Docker-image-upload-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0
  - CD : https://github.com/AnywayClear/mokumoku-backend 
    - 위의 프로젝트에서 구현 성공
- ~~백엔드의 마이크로 서비스들을 하나의 AWS EC2로 배포해보기~~
  - https://github.com/AnywayClear/mokumoku-backend
  - 위의 프로젝트에서 구현 성공

### Front Server

[AMOTH_project/final-pjt-front at main · ah9mon/AMOTH_project · GitHub](https://github.com/ah9mon/AMOTH_project/tree/main/final-pjt-front)
