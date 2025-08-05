from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestLecture:
    """강의 검색 요청 DTO"""
    courseCls: str = ""
    curiNm: str = ""
    campusDiv: str = ""
    deptCd: str = ""
    displayDiv: str = ""
    searchType: str = ""
    excludeDay: str = ""
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환 (API 요청용)"""
        return {
            "courseCls": self.courseCls,
            "curiNm": self.curiNm,
            "campusDiv": self.campusDiv,
            "deptCd": self.deptCd,
            "displayDiv": self.displayDiv,
            "searchType": self.searchType,
            "excludeDay": self.excludeDay
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RequestLecture':
        """딕셔너리에서 객체 생성"""
        return cls(
            courseCls=data.get("courseCls", ""),
            curiNm=data.get("curiNm", ""),
            campusDiv=data.get("campusDiv", ""),
            deptCd=data.get("deptCd", ""),
            displayDiv=data.get("displayDiv", ""),
            searchType=data.get("searchType", ""),
            excludeDay=data.get("excludeDay", "")
        )
