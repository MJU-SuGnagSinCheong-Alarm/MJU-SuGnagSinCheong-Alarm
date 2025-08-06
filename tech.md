# 명지대학교 수강신청 사이트 크롤링 분석

이 문서는 명지대학교 수강신청 사이트의 강의 정보를 수집하는 크롤링 프로세스의 기술적 구조를 설명합니다. 코드 구현 방식보다는 대상 사이트의 인증 방식, URL 구조, AJAX 통신 방법 등 핵심적인 크롤링 메커니즘에 초점을 맞춥니다.

## 1. 인증 및 세션 관리 (Authentication and Session Management)

세션 유지를 위해 `requests.Session` 객체를 사용하여 로그인 시 획득한 쿠키를 모든 후속 요청에 포함시켜 로그인 상태를 유지합니다.

### 1.1. 로그인 과정

1.  **초기 접속 및 CSRF 토큰 획득**:
    *   먼저 `GET https://class.mju.ac.kr/` 주소로 요청을 보내 로그인 페이지의 HTML을 가져옵니다.
    *   이 HTML 내부에 숨겨진 `<input type="hidden" name="_csrf" value="...">` 태그에서 첫 번째 CSRF 토큰 값을 추출합니다.

2.  **로그인 요청**:
    *   `POST https://class.mju.ac.kr/loginproc` 주소로 로그인을 요청합니다.
    *   요청 본문(Payload)에는 다음 `form-data`가 포함됩니다.
        *   `username`: 학번
        *   `password`: 비밀번호
        *   `lang`: `ko`
        *   `_csrf`: 1단계에서 획득한 CSRF 토큰

3.  **로그인 성공 확인**:
    *   로그인 성공 시, 서버는 `.../main` 또는 `.../main.do` 와 같은 메인 페이지로 리디렉션합니다. 응답 URL에 `main`이 포함되어 있는지 여부로 로그인 성공을 판별합니다.

### 1.2. 세션 유효성 검사

*   로그인된 세션의 유효성은 메인 페이지(`https://class.mju.ac.kr/main?lang=ko`)에 다시 접근하여 확인할 수 있습니다.
*   응답 받은 HTML 내용에 "로그아웃"이라는 문자열이 포함되어 있으면 현재 세션이 유효하다고 판단합니다. 만약 포함되어 있지 않다면 세션이 만료된 것으로 간주합니다.

## 2. CSRF 토큰 처리 (CSRF Token Handling)

이 사이트는 보안을 위해 CSRF(Cross-Site Request Forgery) 토큰을 사용하며, 로그인과 데이터 요청 시 각각 다른 방식으로 토큰을 관리해야 합니다.

### 2.1. 로그인 페이지 토큰

*   로그인 과정에서 사용되는 토큰은 로그인 페이지 HTML의 `<input>` 태그에서 직접 파싱하여 사용합니다.

### 2.2. 메인 페이지 토큰 (AJAX 요청용)

*   로그인에 성공한 후, 모든 AJAX 요청에 사용될 새로운 CSRF 토큰을 메인 페이지의 HTML에서 다시 획득해야 합니다.
*   이 토큰은 `<meta>` 태그에 저장되어 있습니다.
    *   **토큰 값**: `<meta name="_csrf" content="...">`
    *   **토큰 헤더 이름**: `<meta name="_csrf_header" content="...">` (예: `X-CSRF-TOKEN`)
*   이 두 값을 캐싱하여 이후 모든 강의 정보 요청에 사용합니다.

### 2.3. 토큰 사용 및 갱신

*   강의 정보를 요청하는 AJAX 호출 시, 2.2단계에서 획득한 토큰을 **두 곳**에 모두 포함해야 합니다.
    1.  **요청 헤더**: `_csrf_header`에서 얻은 이름(예: `X-CSRF-TOKEN`)으로 토큰 값을 전송합니다.
    2.  **요청 본문**: `_csrf`라는 필드명으로 토큰 값을 전송합니다.

*   만약 서버로부터 `403 Forbidden` 오류를 응답 받으면, 이는 CSRF 토큰이 만료되었을 가능성이 높습니다. 이 경우, 메인 페이지에 다시 접속하여 새로운 CSRF 토큰과 헤더를 받아온 후, 실패했던 AJAX 요청을 한 번 더 재시도하는 로직이 구현되어 있습니다.

## 3. 강의 데이터 크롤링 (AJAX)

전체 강의 목록은 정적 페이지가 아닌, 사용자의 검색 조건에 따라 동적으로 데이터를 가져오는 AJAX 방식으로 제공됩니다.

### 3.1. AJAX 엔드포인트

*   **URL**: `https://class.mju.ac.kr/ajax/lectureSearch`
*   **Method**: `POST`

### 3.2. 요청 구조

*   **Headers**:
    *   `Content-Type`: `application/x-www-form-urlencoded`
    *   `X-Requested-With`: `XMLHttpRequest` (서버에 AJAX 요청임을 알림)
    *   `Referer`: `https://class.mju.ac.kr/main?lang=ko`
    *   `[CSRF 헤더 이름]`: 2.2단계에서 획득한 CSRF 헤더 이름과 토큰 값 (예: `X-CSRF-TOKEN: ...`)

*   **Body (Payload)**:
    *   `x-www-form-urlencoded` 형식으로 전송되며, 다양한 검색 조건을 포함합니다.
    *   `lecture_search.json` 파일에 정의된 각 카테고리(캠퍼스, 개설학과, 교양 영역 등)의 검색 조건 파라미터가 포함됩니다.
    *   필수적으로 `_csrf` 토큰 값이 함께 전송되어야 합니다.

    ```
    # 예시 Payload
    campusDiv=1&deptCd=1234&displayDiv=1&searchType=1&_csrf=...
    ```

### 3.3. 응답 구조

*   서버는 요청된 검색 조건에 해당하는 강의 목록을 **JSON 배열** 형식으로 응답합니다.
*   배열의 각 요소는 하나의 강의 정보를 담고 있는 JSON 객체입니다.

    ```json
    [
      {
        "course_id": "...",
        "title": "소프트웨어공학",
        "professor": "홍길동",
        "time": "월1,수1",
        ...
      },
      ...
    ]
    ```

## 4. 전체 크롤링 흐름 요약

1.  **로그인**: `Authenticator`가 로그인 페이지에서 CSRF 토큰을 받아 로그인하고, 세션을 활성화합니다.
2.  **AJAX용 CSRF 토큰 획득**: 로그인 성공 후, 메인 페이지의 `meta` 태그에서 AJAX 요청에 사용할 새로운 CSRF 토큰과 헤더 정보를 캐싱합니다.
3.  **검색 조건 로드**: `lecture_search.json` 파일에서 미리 정의된 모든 강의 카테고리(전공, 교양 등)에 대한 검색 파라미터 목록을 불러옵니다.
4.  **카테고리 순회 및 데이터 요청**:
    *   `LectureCrawler`가 검색 조건 목록을 하나씩 순회합니다.
    *   각 조건에 대해 `LectureDataFetcher`가 `POST /ajax/lectureSearch`로 AJAX 요청을 보냅니다. 이 때, 2단계에서 캐싱한 CSRF 토큰을 헤더와 본문에 포함하여 전송합니다.
5.  **데이터 파싱 및 저장**: 서버로부터 받은 JSON 형식의 강의 목록을 파싱하여 `CourseRepository`를 통해 저장합니다.
6.  **반복**: 모든 검색 조건에 대한 요청이 완료될 때까지 4-5단계를 반복하여 전체 강의 데이터를 수집합니다.
