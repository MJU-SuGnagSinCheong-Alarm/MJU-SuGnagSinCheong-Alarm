import os
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator
from mju_sugang_alarm.course_list_crawler.ajax_data_fetcher import LectureDataFetcher
from mju_sugang_alarm.repository.lecture_repository import CourseRepository
from mju_sugang_alarm.dto.request_lecture import RequestLecture


def main():
    # 로그인 정보 (실제 사용 시 환경변수나 설정파일 사용 권장)
    username = "60222100"
    password = "Jaja8794@"
    
    # 컴포넌트 초기화
    auth = Authenticator(verbose=True)
    repository = CourseRepository()
    
    # 로그인
    print("🔐 로그인 시도 중...")
    if not auth.login(username, password):
        print("❌ 로그인 실패")
        return
    
    print("✅ 로그인 성공!")
    
    # 강의 검색 페처 초기화
    fetcher = LectureDataFetcher(auth, repository, verbose=True)
    
    # JSON 파일에서 모든 카테고리 검색
    json_file_path = "lecture_search.json"
    
    if os.path.exists(json_file_path):
        print(f"📁 {json_file_path} 파일에서 검색 조건 로드 중...")
        success_count = fetcher.load_and_fetch_from_json(json_file_path)
        
        print(f"\n📊 최종 결과:")
        print(f"- 성공한 카테고리: {success_count}개")
        print(f"- 총 수집된 강의: {repository.count()}개")
        
        # 예시: 일부 결과 출력
        all_lectures = repository.get_all_lectures()
        if all_lectures:
            print(f"\n📚 첫 번째 강의 예시:")
            first_lecture = all_lectures[0]
            print(f"- 강의명: {first_lecture.curinm}")
            print(f"- 교수명: {first_lecture.profnm}")
            print(f"- 학과: {first_lecture.deptnm}")
            print(f"- 시간: {first_lecture.lecttime}")
            print(f"- 학점: {first_lecture.cdtnum}")
        
        # 예시: 특정 검색
        print(f"\n🔍 '팀프로젝트' 관련 강의 검색:")
        team_lectures = repository.get_lectures_by_course_name("팀프로젝트")
        for lecture in team_lectures[:3]:  # 최대 3개만 출력
            print(f"- {lecture.curinm} ({lecture.profnm}, {lecture.lecttime})")
    
    else:
        print(f"❌ {json_file_path} 파일을 찾을 수 없습니다.")
        
        # 수동으로 하나의 카테고리 테스트
        print("🧪 수동 테스트: 공통교양 - 성서와인간이해")
        test_request = RequestLecture(
            courseCls="",
            curiNm="",
            campusDiv="10",
            deptCd="10000",
            displayDiv="01",
            searchType="1",
            excludeDay=""
        )
        
        if fetcher.fetch_and_save_lectures(test_request):
            print(f"✅ 테스트 성공! {repository.count()}개 강의 수집됨")
        else:
            print("❌ 테스트 실패")


if __name__ == "__main__":
    main()
