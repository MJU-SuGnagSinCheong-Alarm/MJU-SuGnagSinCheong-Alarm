"""
강의 크롤링 전체 흐름을 관리하는 모듈

이 모듈은 Authenticator와 LectureDataFetcher를 조합하여
JSON 파일 로딩부터 전체 카테고리 순회까지의 크롤링 작업을 총괄합니다.
"""
import json
from typing import List, Dict, Any

from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator
from mju_sugang_alarm.course_list_crawler.ajax_data_fetcher import LectureDataFetcher
from mju_sugang_alarm.repository.course_repository import CourseRepository
from mju_sugang_alarm.dto.request_lecture import RequestLecture


class LectureCrawler:
    """강의 크롤링 전체 프로세스를 관리하는 클래스 - 작업 총괄 및 조정 책임"""
    
    def __init__(self, data_fetcher: LectureDataFetcher, repository: CourseRepository, verbose: bool = False):
        """
        초기화 - 의존성 주입 방식
        
        Args:
            data_fetcher: 강의 데이터를 가져올 LectureDataFetcher 인스턴스
            repository: 강의 데이터를 저장할 레포지토리
            verbose: 상세 로그 출력 여부
        """
        self.data_fetcher = data_fetcher
        self.repository = repository
        self.verbose = verbose
        
    def _log(self, message: str) -> None:
        """로그 메시지를 출력합니다."""
        if self.verbose:
            print(message)
    
    def _validate_category_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        카테고리 데이터의 유효성을 검증하고 필터링
        
        Args:
            data: 원본 카테고리 데이터 리스트
            
        Returns:
            List[Dict[str, Any]]: 유효한 카테고리 데이터만 포함된 리스트
        """
        valid_data = []
        required_fields = ["campusDiv", "deptCd", "displayDiv", "searchType"]
        
        for item in data:
            if not isinstance(item, dict):
                self._log(f"⚠️ 잘못된 데이터 형식 건너뜀: {item}")
                continue
                
            if "name" not in item:
                self._log(f"⚠️ 'name' 필드가 없는 데이터 건너뜀: {item}")
                continue
                
            if len(item) <= 1:  # name만 있는 경우
                self._log(f"⚠️ 빈 카테고리 데이터 건너뜀: {item}")
                continue
                
            # 필수 필드 확인
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                self._log(f"⚠️ 필수 필드 누락 데이터 건너뜀: {item.get('name', 'Unknown')} - 누락된 필드: {missing_fields}")
                continue
                
            valid_data.append(item)
        
        self._log(f"📊 유효성 검증 완료: {len(valid_data)}/{len(data)} 개 카테고리가 유효함")
        return valid_data
    
    def crawl_categories(self, categories_data: List[Dict[str, Any]]) -> int:
        """
        카테고리 목록에 대해 강의 검색 수행
        
        Args:
            categories_data: 카테고리 데이터 리스트
            
        Returns:
            int: 성공적으로 처리된 카테고리 수
        """
        valid_categories = self._validate_category_data(categories_data)
        
        if not valid_categories:
            self._log("❌ 유효한 카테고리 데이터가 없습니다.")
            return 0
        
        success_count = 0
        total_lectures = 0
        
        for i, category_data in enumerate(valid_categories):
            # name 필드 제외하고 RequestLecture 객체 생성
            category_data_copy = category_data.copy()
            category_name = category_data_copy.pop("name")
            request = RequestLecture.from_dict(category_data_copy)
            
            self._log(f"📚 [{i+1}/{len(valid_categories)}] '{category_name}' 카테고리 검색 중...")
            
            # 데이터 가져오기
            result = self.data_fetcher.fetch_lectures(request)
            
            if result is not None:
                # 데이터 저장
                self.repository.save_lecture_response(result)
                success_count += 1
                current_count = self.repository.count()
                new_lectures = current_count - total_lectures
                total_lectures = current_count
                self._log(f"✅ '{category_name}': {new_lectures}개 강의 추가 (누적: {total_lectures}개)")
            else:
                self._log(f"❌ '{category_name}' 검색 실패")
            
            # 요청 간 잠시 대기 (서버 부하 방지)
            # import time
            # time.sleep(0.01)
        
        self._log(f"🎉 전체 결과: {success_count}/{len(valid_categories)} 카테고리 성공, 총 {total_lectures}개 강의 수집")
        return success_count
    
    def crawl_categories_dict(self, categories_dict: Dict[str, Dict[str, Any]]) -> int:
        """
        딕셔너리 형태의 카테고리 데이터에 대해 강의 검색 수행
        
        Args:
            categories_dict: 카테고리명을 키로 하는 딕셔너리
            
        Returns:
            int: 성공적으로 처리된 카테고리 수
        """
        if not categories_dict:
            self._log("❌ 유효한 카테고리 데이터가 없습니다.")
            return 0
        
        success_count = 0
        total_lectures = 0
        required_fields = ["campusDiv", "deptCd", "displayDiv", "searchType"]
        
        valid_categories = []
        for category_name, category_data in categories_dict.items():
            # 필수 필드 확인
            missing_fields = [field for field in required_fields if field not in category_data]
            if missing_fields:
                self._log(f"⚠️ 필수 필드 누락 데이터 건너뜀: {category_name} - 누락된 필드: {missing_fields}")
                continue
            valid_categories.append((category_name, category_data))
        
        self._log(f"📊 유효성 검증 완료: {len(valid_categories)}/{len(categories_dict)} 개 카테고리가 유효함")
        
        for i, (category_name, category_data) in enumerate(valid_categories):
            request = RequestLecture.from_dict(category_data)
            
            self._log(f"📚 [{i+1}/{len(valid_categories)}] '{category_name}' 카테고리 검색 중...")
            
            # 데이터 가져오기
            result = self.data_fetcher.fetch_lectures(request)
            
            if result is not None:
                # 데이터 저장
                self.repository.save_lecture_response(result)
                success_count += 1
                current_count = self.repository.count()
                new_lectures = current_count - total_lectures
                total_lectures = current_count
                self._log(f"✅ '{category_name}': {new_lectures}개 강의 추가 (누적: {total_lectures}개)")
            else:
                self._log(f"❌ '{category_name}' 검색 실패")
            
            # 요청 간 잠시 대기 (서버 부하 방지)
            # import time
            # time.sleep(0.01)
        
        self._log(f"🎉 전체 결과: {success_count}/{len(valid_categories)} 카테고리 성공, 총 {total_lectures}개 강의 수집")
        return success_count
    
    def crawl_from_json_file(self, json_file_path: str) -> int:
        """
        JSON 파일에서 검색 조건을 로드하여 강의 크롤링 수행
        
        Args:
            json_file_path: lecture_search.json 파일 경로
            
        Returns:
            int: 성공적으로 처리된 카테고리 수
        """
        try:
            self._log(f"📁 JSON 파일 로딩 중: {json_file_path}")
            
            with open(json_file_path, 'r', encoding='utf-8') as f:
                lecture_search_data = json.load(f)
            
            if not isinstance(lecture_search_data, dict):
                self._log(f"❌ JSON 파일 형식 오류: 딕셔너리가 아닌 {type(lecture_search_data)} 타입")
                return 0
            
            self._log(f"📁 JSON 파일에서 {len(lecture_search_data)}개 항목 로드 완료")
            
            return self.crawl_categories_dict(lecture_search_data)
            
        except FileNotFoundError:
            self._log(f"❌ 파일을 찾을 수 없습니다: {json_file_path}")
            return 0
        except json.JSONDecodeError as e:
            self._log(f"❌ JSON 파싱 오류: {e}")
            return 0
        except Exception as e:
            self._log(f"❌ 파일 로드 오류: {e}")
            return 0
    
    def crawl_single_category(self, category_name: str, request_data: Dict[str, Any]) -> bool:
        """
        단일 카테고리에 대해 강의 검색 수행
        
        Args:
            category_name: 카테고리 이름
            request_data: 검색 요청 데이터
            
        Returns:
            bool: 성공 여부
        """
        try:
            request = RequestLecture.from_dict(request_data)
            self._log(f"📚 '{category_name}' 카테고리 검색 중...")
            
            # 데이터 가져오기
            result = self.data_fetcher.fetch_lectures(request)
            
            if result is not None:
                # 데이터 저장
                self.repository.save_lecture_response(result)
                count = self.repository.count()
                self._log(f"✅ '{category_name}' 검색 완료 (총 {count}개 강의)")
                return True
            else:
                self._log(f"❌ '{category_name}' 검색 실패")
                return False
            
        except Exception as e:
            self._log(f"❌ '{category_name}' 검색 중 오류: {e}")
            return False
    
    def get_crawl_statistics(self) -> Dict[str, int]:
        """
        크롤링 통계 정보 반환
        
        Returns:
            Dict[str, int]: 통계 정보 (총 강의 수 등)
        """
        total_count = self.repository.count()
        return {
            "total_lectures": total_count,
            "repository_type": type(self.repository).__name__
        }
