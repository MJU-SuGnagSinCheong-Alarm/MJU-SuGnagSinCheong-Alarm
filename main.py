import os
import json
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator
from mju_sugang_alarm.course_list_crawler.ajax_data_fetcher import LectureDataFetcher
from mju_sugang_alarm.course_list_crawler.lecture_crawler import LectureCrawler
from mju_sugang_alarm.repository.course_repository import CourseRepository
from mju_sugang_alarm.dto.request_lecture import RequestLecture


def main():
    # 로그인 정보 (실제 사용 시 환경변수나 설정파일 사용 권장)
    username = "YOUR_USERNAME"  # 예: "6022"
    password = "YOUR_PASSWORD"
    
    # 1. authenticator 생성
    auth = Authenticator(verbose=True)
    
    # 2. repository 생성
    repository = CourseRepository()
    
    # 3. data_fetcher 생성 (repository 의존성 없음)
    data_fetcher = LectureDataFetcher(auth, verbose=True)
    
    # 4. crawler 생성 (외부에서 주입받음)
    crawler = LectureCrawler(data_fetcher, repository, verbose=True)
    
    # 5. 로그인
    if not auth.login(username, password):
        return
    
    # 6. JSON 파일에서 모든 카테고리 검색
    json_file_path = "lecture_search.json"
    
    success_count = crawler.crawl_from_json_file(json_file_path)
    
    # 수집된 모든 강의 가져오기
    all_lectures = repository.get_all_lectures()
    # 결과를 lecture_result.json으로 저장
    output_file_path = "lecture_result.json"
    try:
        # Lecture 객체를 JSON으로 직렬화하기 위해 dict로 변환
        from dataclasses import asdict
        lectures_as_dict = [asdict(lecture) for lecture in all_lectures]
    except (ImportError, TypeError):
        # dataclass가 아니거나 다른 구조일 경우, __dict__를 시도
        lectures_as_dict = [lecture.__dict__ for lecture in all_lectures]
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(lectures_as_dict, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    main()