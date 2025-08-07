from getpass import getpass
import os
import json
from dotenv import load_dotenv
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator
from mju_sugang_alarm.course_list_crawler.ajax_data_fetcher import LectureDataFetcher
from mju_sugang_alarm.course_list_crawler.lecture_crawler import LectureCrawler
from mju_sugang_alarm.repository.course_repository import CourseRepository





def main():
    # .env 또는 사용자 입력을 통해 로그인 정보 가져오기
    username, password = get_credentials()

    # 1. authenticator 생성
    auth = Authenticator(verbose=False)

    # 2. repository 생성
    repository = CourseRepository()

    # 3. data_fetcher 생성 (repository 의존성 없음)
    data_fetcher = LectureDataFetcher(auth, verbose=False)

    # 4. crawler 생성 (외부에서 주입받음)
    crawler = LectureCrawler(data_fetcher, repository, verbose=True)

    # 5. 로그인
    if not auth.login(username, password):
        return

    # 6. JSON 파일에서 모든 카테고리 검색
    json_file_path = "lecture_search.json"

    crawler.crawl_from_json_file(json_file_path)

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

    print(f"✅ 모든 강의 정보를 '{output_file_path}' 파일에 저장했습니다.")

def get_credentials() -> tuple[str, str]:
    """
    .env 파일에서 사용자 정보를 로드하거나, 파일이 없으면 사용자에게 직접 입력을 받습니다.

    Returns:
        tuple[str, str]: (사용자 이름, 비밀번호)
    """
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if username and password:
        print("✅ .env 파일에서 사용자 정보를 성공적으로 로드했습니다.")
        return username, password
    else:
        print("⚠️ INFO: 프로젝트 최상위에 .env 파일을 만들고 다음 형식으로 사용자 정보를 저장할 수 있습니다.")
        print("USERNAME=your_username\nPASSWORD=your_password")
        print("✅ .env 파일이 없으므로 직접 입력을 시작합니다.")
        username_input = input("학번을 입력하세요: ").strip()
        password_input = getpass("비밀번호를 입력하세요: ").strip()
        return username_input, password_input
    

if __name__ == "__main__":
    main()
