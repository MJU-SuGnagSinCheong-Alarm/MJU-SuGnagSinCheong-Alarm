### request

courseCls : 키워드 검색시 강좌번호  => 불필요 

curiNm : 키워드 검색시 교과목명 (인코딩되어서 들어감) => 불필요

campusDiv : 자연캠퍼스 10, 인문캠퍼스 20

deptCd :             교양인지 과별 과목인지 마다 다름 (규칙을 모르겠음)  => 파일을 참고

displayDiv : 교양에서는 다르게 들어감 소분류 , 전공에서는 27 통일

searchType : 1 이면 개설강좌검색, 2이면 키워드 검색 => 1로 고정

excludeDay : 요일 제외 기능 => 불필요



### ✅ 자연캠퍼스 (campusDiv=10)

#### 🔹 교양과목 (과목명 기재)

```plaintext
공통교양 - 성서와인간이해: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=01&searchType=1&excludeDay=
공통교양 - 채플: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=02&searchType=1&excludeDay=
공통교양 - 영어: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=03&searchType=1&excludeDay=
공통교양 - 영어회화: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=04&searchType=1&excludeDay=
공통교양 - 기타교양필수: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=05&searchType=1&excludeDay=
핵심교양 - 핵심교양과목: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=06&searchType=1&excludeDay=
일반교양 - 기독교의이해와삶: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=19&searchType=1&excludeDay=
일반교양 - 인문과학: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=11&searchType=1&excludeDay=
일반교양 - 문화와예술: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=12&searchType=1&excludeDay=
일반교양 - 사회과학: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=13&searchType=1&excludeDay=
일반교양 - 자연과학: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=14&searchType=1&excludeDay=
일반교양 - 공학: courseCls=&curiNm=&campusDiv=10&deptCd=10000& displayDiv=15&searchType=1&excludeDay=
일반교양 - 건강과생활: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=16&searchType=1&excludeDay=
일반교양 - 외국어: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=17&searchType=1&excludeDay=
일반교양 - 컴퓨터: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=18&searchType=1&excludeDay=
일반교양 - 특별주제명사초대강좌: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=27&searchType=1&excludeDay=
교직 - 교직: courseCls=&curiNm=&campusDiv=10&deptCd=10000&displayDiv=30&searchType=1&excludeDay=
```

---

#### 🔹 전공과목 (학과명만 기재)

```plaintext
(스마트시스템공과대학) 스마트시스템공과대학: courseCls=&curiNm=&campusDiv=10&deptCd=15400&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 화공신소재공학부 화학공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15411&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 화공신소재공학부 신소재공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15412&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 스마트인프라공학부: courseCls=&curiNm=&campusDiv=10&deptCd=15420&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 스마트인프라공학부 환경시스템공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15421&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 스마트인프라공학부 건설환경공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15422&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 스마트인프라공학부 스마트모빌리티공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15423&displayDiv=27&searchType=1&excludeDay=
(스마트시스템공과대학) 기계시스템공학부 기계공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15431&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 반도체·ICT대학: courseCls=&curiNm=&campusDiv=10&deptCd=15600&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 컴퓨터정보통신공학부: courseCls=&curiNm=&campusDiv=10&deptCd=15610&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 컴퓨터정보통신공학부 컴퓨터공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15611&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 컴퓨터정보통신공학부 정보통신공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15612&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 전기전자공학부 전기공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15621&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 전기전자공학부 전자공학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15622&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 산업경영공학과: courseCls=&curiNm=&campusDiv=10&deptCd=15630&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 반도체공학부: courseCls=&curiNm=&campusDiv=10&deptCd=15640&displayDiv=27&searchType=1&excludeDay=
(반도체·ICT대학) 반도체시스템공학과: courseCls=&curiNm=&campusDiv=10&deptCd=15650&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 화학·생명과학대학: courseCls=&curiNm=&campusDiv=10&deptCd=15800&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 물리학과: courseCls=&curiNm=&campusDiv=10&deptCd=15808&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 수학과: courseCls=&curiNm=&campusDiv=10&deptCd=15809&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 화학·에너지융합학부 화학나노학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15811&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 융합바이오학부 식품영양학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15821&displayDiv=27&searchType=1&excludeDay=
(화학·생명과학대학) 융합바이오학부 시스템생명과학전공: courseCls=&curiNm=&campusDiv=10&deptCd=15822&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 바둑학과: courseCls=&curiNm=&campusDiv=10&deptCd=17609&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 디자인학부: courseCls=&curiNm=&campusDiv=10&deptCd=17610&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 스포츠학부(체육학전공, 스포츠산업학전공): courseCls=&curiNm=&campusDiv=10&deptCd=17621&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 스포츠학부 스포츠지도학전공: courseCls=&curiNm=&campusDiv=10&deptCd=17622&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 아트앤멀티미디어음악학부: courseCls=&curiNm=&campusDiv=10&deptCd=17630&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 아트앤멀티미디어음악학부 건반음악전공: courseCls=&curiNm=&campusDiv=10&deptCd=17631&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 아트앤멀티미디어음악학부 보컬뮤직전공: courseCls=&curiNm=&campusDiv=10&deptCd=17632&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 아트앤멀티미디어음악학부 작곡전공: courseCls=&curiNm=&campusDiv=10&deptCd=17633&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 공연예술학부: courseCls=&curiNm=&campusDiv=10&deptCd=17640&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 공연예술학부 연극·영화전공: courseCls=&curiNm=&campusDiv=10&deptCd=17641&displayDiv=27&searchType=1&excludeDay=
(스포츠·예술대학) 공연예술학부 뮤지컬공연전공: courseCls=&curiNm=&campusDiv=10&deptCd=17642&displayDiv=27&searchType=1&excludeDay=
(건축대학) 건축대학: courseCls=&curiNm=&campusDiv=10&deptCd=18000&displayDiv=27&searchType=1&excludeDay=
(건축대학) 건축학부: courseCls=&curiNm=&campusDiv=10&deptCd=18030&displayDiv=27&searchType=1&excludeDay=
(건축대학) 건축학부 건축학전공: courseCls=&curiNm=&campusDiv=10&deptCd=18031&displayDiv=27&searchType=1&excludeDay=
(건축대학) 건축학부 전통건축학전공: courseCls=&curiNm=&campusDiv=10&deptCd=18032&displayDiv=27&searchType=1&excludeDay=
(건축대학) 공간디자인학과: courseCls=&curiNm=&campusDiv=10&deptCd=18040&displayDiv=27&searchType=1&excludeDay=
(융합전공) 융합전공: courseCls=&curiNm=&campusDiv=10&deptCd=19000&displayDiv=27&searchType=1&excludeDay=
(융합전공) 제약바이오: courseCls=&curiNm=&campusDiv=10&deptCd=19034&displayDiv=27&searchType=1&excludeDay=
(융합전공) 멀티미디어콘텐츠크리에이션: courseCls=&curiNm=&campusDiv=10&deptCd=19038&displayDiv=27&searchType=1&excludeDay=
```

---

### ✅ 인문캠퍼스 (campusDiv=20)

#### 🔹 교양과목 (과목명 기재)

```plaintext
공통교양 - 성서와인간이해: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=01&searchType=1&excludeDay=
공통교양 - 채플: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=02&searchType=1&excludeDay=
공통교양 - 영어: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=03&searchType=1&excludeDay=
공통교양 - 영어회화: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=04&searchType=1&excludeDay=
공통교양 - 기타교양필수: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=05&searchType=1&excludeDay=
핵심교양 - 핵심교양과목: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=06&searchType=1&excludeDay=
일반교양 - 기독교의이해와삶: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=19&searchType=1&excludeDay=
일반교양 - 인문과학: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=11&searchType=1&excludeDay=
일반교양 - 문화와예술: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=12&searchType=1&excludeDay=
일반교양 - 사회과학: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=13&searchType=1&excludeDay=
일반교양 - 자연과학: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=14&searchType=1&excludeDay=
일반교양 - 공학: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=15&searchType=1&excludeDay=
일반교양 - 건강과생활: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=16&searchType=1&excludeDay=
일반교양 - 외국어: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=17&searchType=1&excludeDay=
일반교양 - 컴퓨터: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=18&searchType=1&excludeDay=
일반교양 - 특별주제명사초대강좌: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=27&searchType=1&excludeDay=
교직 - 교직: courseCls=&curiNm=&campusDiv=20&deptCd=20000&displayDiv=30&searchType=1&excludeDay=
```

---

#### 🔹 전공과목 (학과명만 기재)

```plaintext
14000 (인문대학) 인문대학: courseCls=&curiNm=&campusDiv=20&deptCd=14000&displayDiv=27&searchType=1&excludeDay=
(인문대학) 사학과: courseCls=&curiNm=&campusDiv=20&deptCd=14190&displayDiv=27&searchType=1&excludeDay=
(인문대학) 미술사학과: courseCls=&curiNm=&campusDiv=20&deptCd=14212&displayDiv=27&searchType=1&excludeDay=
(인문대학) 철학과: courseCls=&curiNm=&campusDiv=20&deptCd=14240&displayDiv=27&searchType=1&excludeDay=
(인문대학) 문예창작학과: courseCls=&curiNm=&campusDiv=20&deptCd=14250&displayDiv=27&searchType=1&excludeDay=
(인문대학) 아시아·중동어문학부 중어중문학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14411&displayDiv=27&searchType=1&excludeDay=
(인문대학) 아시아·중동어문학부 일어일문학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14412&displayDiv=27&searchType=1&excludeDay=
(인문대학) 아시아·중동어문학부 아랍지역학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14413&displayDiv=27&searchType=1&excludeDay=
(인문대학) 아시아·중동어문학부 글로벌한국어학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14414&displayDiv=27&searchType=1&excludeDay=
(인문대학) 인문콘텐츠학부 국어국문학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14421&displayDiv=27&searchType=1&excludeDay=
(인문대학) 인문콘텐츠학부 영어영문학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14422&displayDiv=27&searchType=1&excludeDay=
(인문대학) 인문콘텐츠학부 미술사·역사학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14423&displayDiv=27&searchType=1&excludeDay=
(인문대학) 인문콘텐츠학부 문헌정보학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14424&displayDiv=27&searchType=1&excludeDay=
(미디어·휴먼라이프대학) 미디어·휴먼라이프대학: courseCls=&curiNm=&campusDiv=20&deptCd=14600&displayDiv=27&searchType=1&excludeDay=
(미디어·휴먼라이프대학) 청소년지도·아동학부 청소년지도학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14611&displayDiv=27&searchType=1&excludeDay=
(미디어·휴먼라이프대학) 청소년지도·아동학부 아동학전공: courseCls=&curiNm=&campusDiv=20&deptCd=14612&displayDiv=27&searchType=1&excludeDay=
(미디어·휴먼라이프대학) 디지털미디어학부: courseCls=&curiNm=&campusDiv=20&deptCd=14620&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 사회과학대학: courseCls=&curiNm=&campusDiv=20&deptCd=16400&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 공공인재학부 행정학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16471&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 공공인재학부 정치외교학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16472&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 경상·통계학부 경제학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16481&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 경상·통계학부 응용통계학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16482&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 경상·통계학부 국제통상학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16483&displayDiv=27&searchType=1&excludeDay=
(사회과학대학) 법학과: courseCls=&curiNm=&campusDiv=20&deptCd=16490&displayDiv=27&searchType=1&excludeDay=
(경영대학) 경영대학: courseCls=&curiNm=&campusDiv=20&deptCd=16600&displayDiv=27&searchType=1&excludeDay=
(경영대학) 경영정보학과: courseCls=&curiNm=&campusDiv=20&deptCd=16640&displayDiv=27&searchType=1&excludeDay=
(경영대학) 국제통상학과: courseCls=&curiNm=&campusDiv=20&deptCd=16650&displayDiv=27&searchType=1&excludeDay=
(경영대학) 경영학부 경영학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16671&displayDiv=27&searchType=1&excludeDay=
(경영대학) 경영학부 글로벌비즈니스학전공: courseCls=&curiNm=&campusDiv=20&deptCd=16672&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 미래융합대학: courseCls=&curiNm=&campusDiv=20&deptCd=17200&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 뮤직콘텐츠학과: courseCls=&curiNm=&campusDiv=20&deptCd=17205&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 사회복지학과: courseCls=&curiNm=&campusDiv=20&deptCd=17220&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 부동산학과: courseCls=&curiNm=&campusDiv=20&deptCd=17230&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 아동심리상담학과: courseCls=&curiNm=&campusDiv=20&deptCd=17235&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 물류유통경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17250&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 융합예술실용음악학과: courseCls=&curiNm=&campusDiv=20&deptCd=17255&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 법무행정학과: courseCls=&curiNm=&campusDiv=20&deptCd=17260&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 복지경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17265&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 심리치료학과: courseCls=&curiNm=&campusDiv=20&deptCd=17270&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 복지상담학과: courseCls=&curiNm=&campusDiv=20&deptCd=17275&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 미래융합경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17280&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 유통산업경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17290&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 만화애니콘텐츠학과: courseCls=&curiNm=&campusDiv=20&deptCd=17295&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 멀티디자인학과: courseCls=&curiNm=&campusDiv=20&deptCd=17310&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 스포츠산업경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17320&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 융합디자인학과: courseCls=&curiNm=&campusDiv=20&deptCd=17330&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 복지상담경영학과: courseCls=&curiNm=&campusDiv=20&deptCd=17350&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 미용예술학과: courseCls=&curiNm=&campusDiv=20&deptCd=17355&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 웹툰콘텐츠학과: courseCls=&curiNm=&campusDiv=20&deptCd=17360&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 회계세무학과: courseCls=&curiNm=&campusDiv=20&deptCd=17362&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 미디어앤아트테크놀로지학과: courseCls=&curiNm=&campusDiv=20&deptCd=17365&displayDiv=27&searchType=1&excludeDay=
(미래융합대학) 영유아교육상담학과: courseCls=&curiNm=&campusDiv=20&deptCd=17367&displayDiv=27&searchType=1&excludeDay=
(인공지능·소프트웨어융합대학) 인공지능·소프트웨어융합대학: courseCls=&curiNm=&campusDiv=20&deptCd=18600&displayDiv=27&searchType=1&excludeDay=
(인공지능·소프트웨어융합대학) 디지털콘텐츠디자인학과: courseCls=&curiNm=&campusDiv=20&deptCd=18610&displayDiv=27&searchType=1&excludeDay=
(인공지능·소프트웨어융합대학) 융합소프트웨어학부: courseCls=&curiNm=&campusDiv=20&deptCd=18620&displayDiv=27&searchType=1&excludeDay=
(인공지능·소프트웨어융합대학) 융합소프트웨어학부 응용소프트웨어전공: courseCls=&curiNm=&campusDiv=20&deptCd=18621&displayDiv=27&searchType=1&excludeDay=
(인공지능·소프트웨어융합대학) 융합소프트웨어학부 데이터사이언스전공: courseCls=&curiNm=&campusDiv=20&deptCd=18622&displayDiv=27&searchType=1&excludeDay=
(융합전공) 융합예술학융합전공: courseCls=&curiNm=&campusDiv=20&deptCd=19036&displayDiv=27&searchType=1&excludeDay=
```

---

### ✅ 요약

- ✅ **교양과목**: `deptCd=10000` (자연) / `20000` (인문), `displayDiv`는 **과목명에 따라 다름**
- ✅ **전공과목**: `deptCd`는 학과별 고유코드, `displayDiv=27`, `searchType=1`
- ✅ **campusDiv**: 자연캠퍼스 `10`, 인문캠퍼스 `20`

---

필요하시면 이 목록을 **CSV 파일**, **링크 모음 HTML**, 또는 **엑셀 양식**으로도 만들어드릴 수 있어요.  
특정 학과만 추출하거나, 검색용 키워드 필터링 기능도 추가 가능합니다.



