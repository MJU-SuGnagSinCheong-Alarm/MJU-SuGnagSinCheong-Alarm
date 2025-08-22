# 명지대학교 수강신청 시스템 크롤링 기술문서

## 개요

본 문서는 명지대학교 수강신청 시스템(`https://class.mju.ac.kr`)의 구조 분석과 크롤링 방법에 대한 기술적 설명을 다룹니다.

## 1. 시스템 구조 분석

### 1.1 기본 URL 구조
- **베이스 URL**: `https://class.mju.ac.kr`
- **로그인 페이지**: `https://class.mju.ac.kr/`
- **로그인 처리**: `https://class.mju.ac.kr/loginproc`
- **메인 페이지**: `https://class.mju.ac.kr/main?lang=ko`
- **강의 검색 AJAX**: `https://class.mju.ac.kr/ajax/lectureSearch`

> lectureSearch 이외에도 수강신청처리 ajax url 이 있지만 사용하면 안된다

### 1.2 인증 및 보안 체계

#### CSRF (Cross-Site Request Forgery) 보호
시스템은 CSRF 공격을 방지하기 위해 두 가지 방식의 토큰을 사용합니다:

1. **로그인 시 CSRF 토큰**
   - 위치: 로그인 페이지의 `<input name="_csrf" value="토큰값">`
   - 용도: 로그인 요청 시 함께 전송
   - 추출 방법: HTML 파싱(BeautifulSoup, 정규식 등등)

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
    "courseCls": "",
    "curiNm": "",
    "campusDiv": "10",
    "deptCd": "10000",
    "displayDiv": "01",
    "searchType": "1",
    "excludeDay": ""
}
```

### 4.2 검색 파라미터 설명

| 파라미터 | 설명 | 예시값 |
|---------|------|--------|
| `courseCls` | 키워드 검색시 강좌번호 |  |
| `campusDiv` | 캠퍼스 구분 | "10" (자연캠퍼스), "20" (인문캠퍼스) |
| `deptCd` | 학과 코드 | "15611" (컴퓨터 공학과) |
| `displayDiv` | 소분류(교양 과목 분류) | 02 채플, 03 영어, 04 영어회화 ... |
| `searchType` | 검색 타입 | 1 기본값 , 2 키워드 검색 |
| excludeDay | 제외 요일 |  |

### 4.3 응답 데이터 구조

#### 성공 응답 (JSON Array)

```json
[
  {
    "lectureCd": "강의 코드 (예: 6223)",
    "lectureName": "강의 명 (예: 배려의행복학)",
    "professorName": "교수 명 (예: 미배정 또는 교수 이름)",
    "credit": "학점 수 (예: 3)",
    "timeSchedule": "시간표 (예: 화 10:00~11:15, 목 10:00~11:15)",
    "classroom": "강의실 (예: 공학관 203호 또는 미정)",
    "capacity": "수강 정원 (예: 1)",
    "enrolled": "현재 신청 인원 (예: 0)",
    "deptName": "개설 학과 명 (예: 미래융합대학)",
    "curiyear": "개설 연도 (예: 2025)",
    "curismt": "학기 코드 (예: 20 → 2학기, 10 → 1학기)",
    "campusdiv": "캠퍼스 구분 (예: 10 → 서울, 20 → 용인)",
    "classdiv": "분반 번호 (예: 01)",
    "gbn": "수강 구분 (예: 1 → 교양, 2 → 전공)",
    "curigbn": "세부 과목 구분 코드 (예: null 또는 특정 코드)",
    "comyear": "공통 개설 여부 (예: 0 → 일반, 1 → 공통)",
    "curinum": "과목 번호 (예: KMB02163)",
    "coursecls": "강의 반 코드 (예: 6223)",
    "curinum2": "과목 약어 번호 (예: 기인163)",
    "groupcd": "그룹 코드 (예: 기인 → 기초인문)",
    "cdtnum": "학점 수 (예: 3)",
    "cdttime": "이론 시간 (주당 수업 시간 수, 예: 3)",
    "takelim": "정원 (최대 수강 가능 인원)",
    "listennow": "현재 수강 인원",
    "deptcd": "학과 코드 (예: 17200)",
    "profid": "교수 ID (예: null 또는 교수 사번)",
    "profnm": "교수 명",
    "largetp": "대분류 코드 (예: 00)",
    "smalltp": "소분류 코드 (예: 11)",
    "abotp": "AB 옵션 여부 (Y/N)",
    "lecttime": "강의 시간 및 장소 정보 (예: 화목 10:00~11:15, 공학관 203) 또는 null",
    "dislevel": "장애 학생 배려 수준 코드 (예: 00)",
    "curicontent": "강의 개요 및 내용 (텍스트 또는 null)",
    "bagcnt": "수강 제한 그룹 수 (예: 1)",
    "dbtimelist": "데이터베이스용 시간 정보 배열 (구조화된 시간 데이터, 예: null)",
    "sugyn": "수강신청 가능 여부 (Y/N)",
    "addtime": "추가 개설 시간 (예: null 또는 시간 정보)",
    "internetyn": "온라인 강의 여부 (Y/N 또는 null)",
    "flexyn": "플렉스 강의 여부 (Y/N)",
    "classtype": "수업 유형 (1: 면대면, 2: 온라인, 3: 혼합)",
    "lecperiod": "강의 기간 (예: 2025-09-01 ~ 2025-12-12)",
    "bagorder": "수강 우선순위 그룹 (예: null)",
    "pastcuridata": "과거 수강 데이터 (예: null)",
    "pastcurigrade": "과거 성적 정보 (예: null)",
    "pastcurigpa": "과거 평점 (예: null)",
    "lang": "강의 언어 (ko: 한국어, en: 영어 .. )"
  }
  ,
    ...........
]
```

#### 4.4 응답 파리마터 설명(LLM)

| 필드 | Full Form (약어 의미) | 값 | 설명 |
|------|------------------------|----|------|
| `curiyear` | **Curriculum Year** | `"2025"` | 개설 연도: 이 과목이 2025년도에 개설됨 |
| `curismt` | **Curriculum Semester** | `"20"` | 학기 코드: `20` = 2학기, `10` = 1학기 |
| `campusdiv` | **Campus Division** | `"20"` | 캠퍼스 구분: <br>• `10`: 인문(서울) 캠퍼스 <br>• `20`: 자연(용인) 캠퍼스 |
| `classdiv` | **Class Division** | `"01"` | 분반: 1분반 (예: 01, 02, ...) |
| `gbn` | **Gubun (구분)** | `"1"` | 수강 구분 코드 (예: 전공, 교양 등)<br>• 예: `1`=교양, `2`=전공 |
| `curigbn` | **Curriculum Gubun** | `null` | 세부 과목 구분 코드 (예: 교양영역 등)<br>• 현재 미지정 또는 미사용 |
| `comyear` | **Common Year** | `"0"` | 공통 개설 연도 기준 (통합 과목 여부 등)<br>• `0`: 일반, `1`: 공통 개설 과목 |
| `curinum` | **Curriculum Number** | `"KMB02163"` | 과목 번호: 학과에서 부여한 고유 코드<br>• 예: `KMB02163` = 미래융합대학 관련 과목 |
| `coursecls` | **Course Class** | `"6223"` | 강의 반 코드: 수강신청 시 구분용 고유 번호<br>• 학생이 수강신청할 때 이 코드로 선택 |
| `curinum2` | **Curriculum Number 2** | `"기인163"` | 과목 약어 번호: 사용자 친화적인 과목 코드<br>• `기인` = 기초인문, `기과` = 기초과학 등 |
| `curinm` | **Curriculum Name** | `"배려의행복학"` | 과목명: 수업의 이름 |
| `groupcd` | **Group Code** | `"기인"` | 그룹 코드: 교양 영역 또는 과목 그룹<br>• 예: `기인`=기초인문, `기과`=기초과학, `핵교`=핵심교양 |
| `cdtnum` | **Credit Number** | `"3"` | 학점 수: 이 과목은 3학점 |
| `cdttime` | **Credit Time** | `"3"` | 이론 시간: 주당 3시간 강의 |
| `takelim` | **Take Limit** | `"30"` | 정원: 최대 30명 수강 가능 |
| `listennow` | **Listen Now** | `"23"` | 현재 수강 인원: 현재 23명 수강 중 |
| `deptcd` | **Department Code** | `"17200"` | 학과 코드: `17200` = 미래융합대학 |
| `deptnm` | **Department Name** | `"미래융합대학"` | 개설 학과명: 이 과목을 개설한 학과 |
| `profid` | **Professor ID** | `null` | 교수 ID: 아직 교수 배정되지 않음 |
| `profnm` | **Professor Name** | `"미배정"` | 교수명: "미배정" → 아직 담당 교수 없음 |
| `largetp` | **Large Type** | `"00"` | 대분류 코드: 과목 분류 체계의 상위 코드 (예: 교양, 전공 등) |
| `smalltp` | **Small Type** | `"11"` | 소분류 코드: 세부 분류 (예: 인문, 사회, 자연 등) |
| `abotp` | **A/B Option** | `"N"` | AB옵션 여부: `N`=해당 없음, `Y`=성적을 A/B로만 부여 |
| `lecttime` | **Lecture Time** | `null` | 강의 시간표 정보: 아직 시간/요일/강의실 미정 |
| `dislevel` | **Disability Level** | `"00"` | 장애 학생 배려 수준 코드: 특별한 배려 없음 |
| `curicontent` | **Curriculum Content** | `null` | 강의 개요/내용: 아직 입력되지 않음 |
| `bagcnt` | **Bag Count** | `"1"` | 수강 제한 그룹: 같은 그룹의 과목 중 1개까지만 수강 가능 |
| `dbtimelist` | **Database Time List** | `null` | 강의 시간 데이터 (구조화된 시간 정보): 아직 없음 |
| `sugyn` | **Sugang Y/N** | `"N"` | 수강신청 가능 여부: `N`=불가능, `Y`=가능 (현재는 신청 불가) |
| `addtime` | **Additional Time** | `null` | 추가 개설 시간: 아직 예정되지 않음 |
| `internetyn` | **Internet Y/N** | `null` | 온라인 강의 여부: 정보 없음 |
| `flexyn` | **Flex Y/N** | `"N"` | 플렉스 강의 여부: `N`=일반 강의, `Y`=시간 유연한 플렉스 수업 |
| `classtype` | **Class Type** | `"1"` | 수업 유형: `1`=면대면, `2`=온라인, `3`=혼합 등 |
| `lecperiod` | **Lecture Period** | `"2025-09-01 ~ 2025-12-12"` | 강의 기간: 2025년 9월 1일 ~ 12월 12일 (2학기) |
| `bagorder` | **Bag Order** | `null` | 수강 우선순위 그룹: 없음 |
| `pastcuridata` | **Past Curriculum Data** | `null` | 과거 수강 데이터: 이 과목의 과거 이력 없음 |
| `pastcurigrade` | **Past Curriculum Grade** | `null` | 과거 성적: 제공되지 않음 |
| `pastcurigpa` | **Past Curriculum GPA** | `null` | 과거 평점: 제공되지 않음 |
| `lang` | **Language** | `"ko"` | 강의 언어: `ko`=한국어, `en`=영어 등 |


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