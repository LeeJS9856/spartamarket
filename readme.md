# 스파르타 마켓 프로젝트

스파르타 마켓 프로젝트 '스파-마켓'은 스파르타 코딩클럽'의 프로젝트 일환으로,
중고 거래 게시판 형태의 웹 사이트 입니다. 

</br>
</br>

## 개발기간

- 2024.04.15(월) ~ 2024.04.18(목)

</br>
</br>

## 개발 환경

### 언어

- python


### 프레임워크

- django


### 데이터베이스

- django ORM


### 웹 기술

- HTML / CSS / JS
- Bootstrap


</br>
</br>

## 기능 상세

- **홈** : 메인 페이지입니다. 각 게시물들을 이미지와 함께 볼 수 있습니다.
- **물품 등록** : 물품을 이미지와 함께 등록할 수 있습니다.
- **물품 상세** : 작성자, 물품, 물품 설명, 가격, 등록날짜를 볼 수 있고, 마음에 든 물품은 "찜"할수 있습니다.
- **물품 수정** : 등록한 물품을 수정할 수 있습니다.
- **물품 삭제** : 등록한 물품을 삭제할 수 있습니다.

- **프로필** : 닉네임, 가입날짜, 찜/팔로잉/팔로워 수, 등록한 물품이 표시됩니다. 또한 팔로우 및 언팔로우를 통해 관심유저로 설정할 수 있습니다.
- **내정보** : 프로필의 대상이 로그인한 유저일 경우, 팔로우 대신 정보 수정이 가능합니다.

- **회원가입** : 회원가입한 유저만 로그인 할 수 있습니다.
- **로그인** : 로그인 한 유저는 글을 등록할 수 있고, 팔로우 및 찜 기능을 사용할 수 있습니다.


</br>
</br>

## 와이어프레임

![와이어프레임](https://github.com/LeeJS9856/spartamarket/blob/master/spartamarket%20%EC%99%80%EC%9D%B4%EC%96%B4%ED%94%84%EB%A0%88%EC%9E%84_240419_110408_0.png)


</br>
</br>

## ERD

![ERD](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/ERD.png)


</br>
</br>

## API 명세

| 분류     | 기능            | 메서드   | 분류  | 기능              | 메서드 |
|----------|-----------------|--------|--------|----------------- |--------|
| 회원관리 | 회원가입        | GET POST | 팔로우 | 팔로우 및 언팔로우 | POST  |
|          | 로그인          | GET POST| 찜    | 게시글 찜          | POST  |
|          |  정보 수정      | GET POST|       |                   |       |
| 게시글   | 게시글 작성     | GET POST |       |                   |       |
|          | 게시글 수정     | GET POST|       |                   |       |
|          | 게시글 삭제     | POST    |       |                   |       |


</br>
</br>


## 웹사이트 예시

![home](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%ED%99%88.png)

![create](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%EB%AC%BC%ED%92%88%20%EB%93%B1%EB%A1%9D.png)

![article](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%EB%AC%BC%ED%92%88%20%EC%83%81%EC%84%B8.png)

![profile](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%ED%94%84%EB%A1%9C%ED%95%84.png)

![editprofile](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%EC%A0%95%EB%B3%B4%20%EC%88%98%EC%A0%95.png)

![signup](https://github.com/LeeJS9856/spartamarket/blob/master/%EC%8A%A4%ED%8C%8C%EB%A7%88%EC%BC%93/%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85.png)
