import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any

class MJULectureSearchUpdater:
    def __init__(self, session_cookies: Dict[str, str] = None):
        """
        MJU 수강 검색 데이터 업데이터
        
        Args:
            session_cookies: 로그인 후 세션 쿠키 정보
        """
        self.session = requests.Session()
        if session_cookies:
            self.session.cookies.update(session_cookies)
    
    def fetch_search_page(self) -> str:
        """검색 페이지 HTML을 가져옵니다."""
        try:
            response = self.session.get('https://class.mju.ac.kr/main/search')
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"페이지 요청 실패: {e}")
            return None
    
    def parse_department_options(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """학과 옵션들을 파싱합니다."""
        departments = {}
        
        # 자연캠퍼스와 인문캠퍼스 select 태그 찾기
        dept_selects = soup.find_all('select', class_='deptlistclass')
        
        for select in dept_selects:
            campus_id = select.get('id')
            campus_div = "10" if "10" in campus_id else "20"
            campus_name = "자연캠퍼스" if campus_div == "10" else "인문캠퍼스"
            
            options = select.find_all('option')
            
            for option in options:
                dept_cd = option.get('value')
                dept_name = option.text.strip()
                
                if dept_cd and dept_name:
                    # 교양과목인지 확인
                    if "교양과목" in dept_name:
                        continue  # 교양과목은 별도 처리
                    
                    # 전공과목 처리
                    departments[dept_name] = {
                        "courseCls": "",
                        "curiNm": "",
                        "campusDiv": campus_div,
                        "deptCd": dept_cd,
                        "displayDiv": "27",  # 전공과목은 보통 27
                        "searchType": "1",
                        "excludeDay": ""
                    }
        
        return departments
    
    def parse_liberal_options(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """교양 옵션들을 파싱합니다."""
        liberal_courses = {}
        
        # 교양구분 select 태그 찾기
        liberal_select = soup.find('select', id='liberallist')
        
        if not liberal_select:
            return liberal_courses
        
        optgroups = liberal_select.find_all('optgroup')
        
        for optgroup in optgroups:
            category = optgroup.get('label')
            options = optgroup.find_all('option')
            
            for option in options:
                display_div = option.get('value')
                option_text = option.text.strip()
                
                # 자연캠퍼스와 인문캠퍼스 각각 생성
                for campus_div, campus_name in [("10", "자연캠퍼스"), ("20", "인문캠퍼스")]:
                    course_name = f"{campus_name} {category} {option_text.split(' - ')[1] if ' - ' in option_text else option_text}"
                    
                    liberal_courses[course_name] = {
                        "courseCls": "",
                        "curiNm": "",
                        "campusDiv": campus_div,
                        "deptCd": f"{campus_div}000",  # 교양은 캠퍼스코드 + 000
                        "displayDiv": display_div,
                        "searchType": "1",
                        "excludeDay": ""
                    }
        
        return liberal_courses
    
    def generate_lecture_search_json(self) -> Dict[str, Any]:
        """완전한 lecture_search.json 구조를 생성합니다."""
        html_content = self.fetch_search_page()
        
        if not html_content:
            print("HTML 콘텐츠를 가져올 수 없습니다.")
            return {}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 교양과목 파싱
        liberal_courses = self.parse_liberal_options(soup)
        
        # 전공과목 파싱
        departments = self.parse_department_options(soup)
        
        # 두 딕셔너리 합치기
        all_courses = {**liberal_courses, **departments}
        
        return all_courses
    
    def save_to_file(self, filename: str = 'lecture_search.json'):
        """JSON 파일로 저장합니다."""
        data = self.generate_lecture_search_json()
        
        if data:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"데이터가 {filename}에 저장되었습니다.")
        else:
            print("저장할 데이터가 없습니다.")

def main():
    """메인 실행 함수"""
    # 세션 쿠키가 필요한 경우 여기에 추가
    # cookies = {'JSESSIONID': 'your_session_id', 'other_cookie': 'value'}
    
    updater = MJULectureSearchUpdater()
    updater.save_to_file()

if __name__ == "__main__":
    main()