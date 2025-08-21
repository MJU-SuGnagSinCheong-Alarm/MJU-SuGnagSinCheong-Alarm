### login
```js
fetch("https://class.mju.ac.kr/main?lang=ko", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://class.mju.ac.kr/",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});


HTTP/1.1 200
Server: nginx
Date: Thu, 14 Aug 2025 02:09:23 GMT
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Content-Language: ko


```


### 미리담기 내역
```js
fetch("https://class.mju.ac.kr/main/bag", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://class.mju.ac.kr/main/class",
  "body": "_csrf=8e4b9cbe-fc28-4a14-82f1-3e34e72aba4b",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

### 수강신청한 내역
```js
fetch("https://class.mju.ac.kr/main/class", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://class.mju.ac.kr/main/bag",
  "body": "_csrf=8e4b9cbe-fc28-4a14-82f1-3e34e72aba4b",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```


### 강의 검색용 (ajax)
```js
fetch("https://class.mju.ac.kr/ajax/lectureSearch", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "8e4b9cbe-fc28-4a14-82f1-3e34e72aba4b"
  },
  "referrer": "https://class.mju.ac.kr/main/search",
  "body": "courseCls=&curiNm=&campusDiv=10&deptCd=15611&displayDiv=01&searchType=1&excludeDay=",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```


### 수강신청용
```js
fetch("https://class.mju.ac.kr/ajax/lectureRequest", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "8e4b9cbe-fc28-4a14-82f1-3e34e72aba4b"
  },
  "referrer": "https://class.mju.ac.kr/main/bag",
  "body": "courseCls=0762&curiNum=JEO01213&excludeCourse=0710%2C0084%2C0419%2C5469%2C0233%2C5431%2C0762%2C0238",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

### 수강취소
```js
fetch("https://class.mju.ac.kr/ajax/lectureRequestRemove", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "8e4b9cbe-fc28-4a14-82f1-3e34e72aba4b"
  },
  "referrer": "https://class.mju.ac.kr/main/class",
  "body": "courseCls=0762&curiNum=JEO01213&excludeCourse=0108%2C0375%2C0379%2C0711%2C0719%2C0727%2C0762",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```


###  수강신청 시간표 보기
```js
function timetablePopup(){
	const w = 1000;
	const h = 600;
	const title = "timetablePopup";
	
	const dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
	const dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;
	
	const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
	const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;
	
	const left = ((width / 2) - (w / 2)) + dualScreenLeft;
	const top = ((height / 2) - (h / 2)) + dualScreenTop;
	
	const newWindow = window.open("", title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
	
	let frm = document.mainfrm;
	frm.target = title;
	frm.action = "/popup/timetable";
	frm.submit();
	
	if(window.focus){
		newWindow.focus();
	}

}
```

```js
fetch("https://class.mju.ac.kr/popup/timetable", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://class.mju.ac.kr/main/class",
  "body": "_csrf=60ce7efa-b9bf-49ee-b384-149961502d34",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```



```html
<div id="statuslayer">
		<div id="statusshow" class="mobileblock" onclick="javascript:showCdtStatus(true);">
			수강신청 대상단계 및 신청학점 보이기
		</div>
		<table id="cdtstatus" class="defaultTable pcblock" onclick="javascript:showCdtStatus(false);" aria-describedby="수강신청에서 보여지는 단계는 신청이 가능한 교과목을 의미하며 MSI와는 다릅니다.">
			<thead>
				<tr>
					<th class="tooltip topoutline" colspan="3">
						수강신청 대상단계
						<span class="qmark">(?)</span>
						<span class="tooltiptext" role="tooltip">
							수강신청에서 보여지는 단계는 신청이 가능한 교과목을 의미하며 MSI와는 다릅니다.
						</span>
					</th>
				</tr>
				<tr>
					<th class="topdetail">
						영어
					</th>
					<th class="topdetail">
						영어회화
					</th>
					<th class="topdetail">
						미적분학
					</th>
				</tr>
			</thead>
			
			<tbody>
				<tr>
					<td>영어3 (R4)</td>
					<td>영어회화2 (L3)</td>
					<td>미적분학2 (A3)</td>
				</tr>
			</tbody>
			
			<thead>
				<tr>
					<th class="topdetail">
						수강가능학점
					</th>
					<th class="topdetail">
						총 수강신청 강좌 수
					</th>
					<th class="topdetail">
						총 수강신청 학점 수
					</th>
				</tr>
			</thead>
			
			<tbody>
				<tr>
					<td>18</td>
					<td id="stat-sugcnt">6</td>
					<td id="stat-sugcdt">15</td>
				</tr>
			</tbody>
		</table>
	</div>
```