## 프로젝트 설계도

크롤러 -> 백엔드 -> 프론트엔드


### 크롤러

`/loginproc` 에서 로그인 실행

`/main` 페이지 요청 및 해당 meta 태그에서 토큰 헤더 이름과 토큰값을 파싱
```html
<meta id="_csrf" name="_csrf" content="CSRF_TOKEN_CONTENTS"/>
<meta id="_csrf_header" name="_csrf_header" content="X-CSRF-TOKEN"/>
```
이후 요청마다 토큰을 포함해서 요청

강의 목록을 가져오기 위해 ajax 요청 필요

```
/lectureSearch
```

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

형태로 요청해서 검색한 강의를 가져옴 모든 검색 요청은  lecture_result.json  파일에 있으며 (name 필드를 제외한 모든 필드를 그대로 요청으로 보내면 응답함)

```json
    {
        "curiyear": "2025",
        "curismt": "20",
        "campusdiv": "10",
        "classdiv": "01",
        "gbn": "1",
        "curigbn": null,
        "comyear": "0",
        "curinum": "KMA00101",
        "coursecls": "0001",
        "curinum2": "교필127",
        "curinm": "성서와인간이해",
        "groupcd": "교필",
        "cdtnum": "2",
        "cdttime": "2",
        "takelim": "50",
        "listennow": "0",
        "deptcd": "10000",
        "deptnm": "자연캠퍼스교양",
        "profid": "20190384",
        "profnm": "김진옥",
        "largetp": "00",
        "smalltp": "01",
        "abotp": "N",
        "lecttime": "월09:00~10:50(Y2508)",
        "dislevel": "00",
        "curicontent": null,
        "bagcnt": "31",
        "dbtimelist": null,
        "sugyn": "N",
        "addtime": null,
        "internetyn": null,
        "flexyn": "N",
        "classtype": "1",
        "lecperiod": "2025-09-01 ~ 2025-12-12",
        "bagorder": null,
        "pastcuridata": "2022-2학기 : 성서와인간이해",
        "pastcurigrade": "C0",
        "pastcurigpa": "2",
        "lang": "ko"
    }
```

이러한 형태로 오게 됨
이렇게 온 결과를 모두 저장

