from typing import List, Optional
from mju_sugang_alarm.dto.response_lecture import ResponseLecture, LectureSearchResponse


class CourseRepository:
    """강의 정보를 저장하고 관리하는 레포지토리"""
    
    def __init__(self):
        self.lectures: List[ResponseLecture] = []
    
    def save_lectures(self, lectures: List[ResponseLecture]) -> None:
        """강의 목록을 저장"""
        self.lectures.extend(lectures)
    
    def save_lecture_response(self, response: LectureSearchResponse) -> None:
        """강의 검색 응답을 저장"""
        self.save_lectures(response.lectures)
    
    def get_all_lectures(self) -> List[ResponseLecture]:
        """모든 강의 목록 반환"""
        return self.lectures.copy()
    
    def get_lectures_by_department(self, dept_cd: str) -> List[ResponseLecture]:
        """학과별 강의 목록 반환"""
        return [lecture for lecture in self.lectures if lecture.deptcd == dept_cd]
    
    def get_lectures_by_professor(self, prof_name: str) -> List[ResponseLecture]:
        """교수별 강의 목록 반환"""
        return [lecture for lecture in self.lectures if lecture.profnm == prof_name]
    
    def get_lectures_by_course_name(self, course_name: str) -> List[ResponseLecture]:
        """강의명으로 검색"""
        return [lecture for lecture in self.lectures if course_name in lecture.curinm]
    
    def clear(self) -> None:
        """모든 강의 정보 삭제"""
        self.lectures.clear()
    
    def count(self) -> int:
        """저장된 강의 수 반환"""
        return len(self.lectures)
    
    def get_lecture_by_course_code(self, course_code: str) -> Optional[ResponseLecture]:
        """강의 코드로 강의 찾기"""
        for lecture in self.lectures:
            if lecture.curinum == course_code:
                return lecture
        return None
    
    def filter_lectures(self, **filters) -> List[ResponseLecture]:
        """다양한 조건으로 강의 필터링"""
        filtered = self.lectures
        
        for key, value in filters.items():
            if value is not None:
                filtered = [lecture for lecture in filtered 
                           if getattr(lecture, key, None) == value]
        
        return filtered
