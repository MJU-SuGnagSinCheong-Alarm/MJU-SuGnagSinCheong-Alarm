# 명주대학교 수강신청 시스템 크롤링 기술문서

## 개요

본 문서는 명주대학교 수강신청 시스템(`https://class.mju.ac.kr`)의 구조 분석과 크롤링 방법에 대한 기술적 설명을 다룹니다.

## 1. 시스템 구조 분석

### 1.1 기본 URL 구조
- **베이스 URL**: `https://class.mju.ac.kr`
- **로그인 페이지**: `https://class.mju.ac.kr/`
- **로그인 처리**: `https://class.mju.ac.kr/loginproc`
- **메인 페이지**: `https://class.mju.ac.kr/main?lang=ko`
- **강의 검색 AJAX**: `https://class.mju.ac.kr/ajax/lectureSearch`

### 1.2 인증 및 보안 체계

#### CSRF (Cross-Site Request Forgery) 보호
시스템은 CSRF 공격을 방지하기 위해 두 가지 방식의 토큰을 사용합니다:

1. **로그인 시 CSRF 토큰**
   - 위치: 로그인 페이지의 `<input name="_csrf" value="토큰값">`
   - 용도: 로그인 요청 시 함께 전송
   - 추출 방법: BeautifulSoup으로 HTML 파싱

2. **AJAX 요청용 CSRF 토큰**
   - 위치: 메인 페이지의 메타태그
     ```html
     <meta name="_csrf" content="토큰값">
     <meta name="_csrf_header" content="헤더명">
     ```
   - 용도: 모든 AJAX 요청의 헤더와 데이터에 포함
   - 특징: 로그인 후에만 접근 가능

## 2. 로그인 프로세스

### 2.1 로그인 흐름
```
1. GET / → 로그인 페이지 접속
2. HTML 파싱 → CSRF 토큰 추출
3. POST /loginproc → 로그인 데이터 전송
4. 리다이렉션 확인 → 성공 시 /main으로 이동
5. GET /main → 메인 페이지 접속
6. 메타태그 파싱 → AJAX용 CSRF 토큰 캐싱
```

### 2.2 로그인 요청 데이터
```json
{
  "username": "학번",
  "password": "비밀번호", 
  "lang": "ko",
  "_csrf": "로그인페이지_CSRF_토큰"
}
```

### 2.3 로그인 성공 판단
- **성공**: 최종 URL에 `main` 또는 `main.do` 포함
- **실패**: 응답 내용에 "로그인", "Sign in", "login" 문자열 포함

## 3. 세션 관리

### 3.1 세션 유지 방식
- **쿠키 기반**: `requests.Session()`을 통한 자동 쿠키 관리
- **User-Agent**: 브라우저로 위장하여 차단 방지
  ```
  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
  ```

### 3.2 세션 검증 방법
- **검증 URL**: `https://class.mju.ac.kr/main?lang=ko`
- **검증 조건**: 응답 내용에 "로그아웃" 문자열 포함 여부
- **만료 시**: 재로그인 또는 CSRF 토큰 갱신 필요

## 4. 강의 검색 API 분석

### 4.1 AJAX 요청 구조

#### 요청 URL
```
POST https://class.mju.ac.kr/ajax/lectureSearch
```

#### 필수 헤더
```http
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest
Referer: https://class.mju.ac.kr/main?lang=ko
{csrf_header}: {csrf_token}
```

#### 요청 데이터 구조
```json
{
  "campusDiv": "캠퍼스구분",
  "deptCd": "학과코드", 
  "displayDiv": "표시구분",
  "searchType": "검색타입",
  "_csrf": "AJAX용_CSRF_토큰"
}
```

### 4.2 검색 파라미터 설명

| 파라미터 | 설명 | 예시값 |
|---------|------|--------|
| `campusDiv` | 캠퍼스 구분 | "1" (인문캠퍼스), "2" (자연캠퍼스) |
| `deptCd` | 학과 코드 | "10101" (국어국문학과) |
| `displayDiv` | 표시 구분 | "1" (전체), "2" (일부) |
| `searchType` | 검색 타입 | "dept" (학과별), "major" (전공별) |

### 4.3 응답 데이터 구조

#### 성공 응답 (JSON Array)
```json
[
  {
    "lectureCd": "강의코드",
    "lectureName": "강의명",
    "professorName": "교수명",
    "credit": "학점",
    "timeSchedule": "시간표",
    "classroom": "강의실",
    "capacity": "정원",
    "enrolled": "신청인원",
    "deptName": "학과명",
    // ... 기타 필드
  }
]
```

#### 오류 응답
- **403 Forbidden**: CSRF 토큰 만료 또는 권한 없음
- **500 Internal Server Error**: 서버 내부 오류
- **빈 배열 []**: 검색 결과 없음

## 5. 에러 처리 및 재시도 로직

### 5.1 CSRF 토큰 만료 처리
```
1. 403 Forbidden 응답 수신
2. CSRF 토큰 갱신 시도
3. 새 토큰으로 요청 재시도
4. 여전히 403이면 권한 문제로 판단
```

### 5.2 세션 만료 처리
```
1. 세션 검증 실패 감지
2. 재로그인 수행
3. 새 세션으로 요청 재시도
```

## 6. 크롤링 최적화 전략

### 6.1 요청 간격 조절
- 서버 부하 방지를 위한 요청 간 딜레이 (현재 주석 처리됨)
- 필요시 `time.sleep(0.01)` 등으로 조절 가능

### 6.2 배치 처리
- 카테고리별 순차 처리
- 실패한 카테고리 재시도 로직
- 진행률 추적 및 로깅

### 6.3 데이터 중복 처리
- 동일한 강의가 여러 카테고리에서 검색될 수 있음
- Repository 레벨에서 중복 제거 로직 필요

## 7. 보안 고려사항

### 7.1 탐지 회피
- 실제 브라우저와 동일한 User-Agent 사용
- 자연스러운 요청 패턴 유지
- 과도한 요청 빈도 방지

### 7.2 인증 정보 보호
- 환경변수(.env) 사용
- 평문 저장 금지
- 세션 정보 메모리에만 보관

## 8. 알려진 제한사항

### 8.1 시스템 제약
- 동시 접속 제한 가능성
- 특정 시간대 접근 제한
- IP 기반 차단 가능성

### 8.2 데이터 일관성
- 실시간 데이터 변경 가능성
- 캐시된 데이터와 실제 데이터 차이
- 수강신청 기간별 접근 권한 변화

## 9. 문제 해결 가이드

### 9.1 자주 발생하는 오류

#### 로그인 실패
- 학번/비밀번호 확인
- 네트워크 연결 상태 확인
- 보안 차단 여부 확인

#### CSRF 토큰 오류
- 토큰 갱신 로직 확인
- 메인 페이지 접근 권한 확인
- HTML 구조 변경 여부 확인

#### 세션 만료
- 세션 검증 로직 재실행
- 필요시 재로그인 수행
- 장시간 대기 시 주기적 갱신

### 9.2 디버깅 팁
- `verbose=True` 옵션으로 상세 로그 확인
- 네트워크 요청/응답 내용 로깅
- 브라우저 개발자 도구와 비교 분석

---

*본 문서는 교육 목적으로 작성되었으며, 시스템의 구조 변경 시 업데이트가 필요할 수 있습니다.*