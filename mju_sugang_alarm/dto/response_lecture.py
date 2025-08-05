from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ResponseLecture:
    """강의 검색 응답 DTO"""
    curiyear: str
    curismt: str
    campusdiv: str
    classdiv: str
    gbn: str
    curigbn: Optional[str]
    comyear: str
    curinum: str
    coursecls: str
    curinum2: str
    curinm: str
    groupcd: str
    cdtnum: str
    cdttime: str
    takelim: str
    listennow: str
    deptcd: str
    deptnm: str
    profid: str
    profnm: str
    largetp: str
    smalltp: str
    abotp: str
    lecttime: str
    dislevel: str
    curicontent: Optional[str]
    bagcnt: str
    dbtimelist: Optional[str]
    sugyn: str
    addtime: Optional[str]
    internetyn: Optional[str]
    flexyn: str
    classtype: str
    lecperiod: str
    bagorder: Optional[str]
    pastcuridata: str
    pastcurigrade: str
    pastcurigpa: str
    lang: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ResponseLecture':
        """딕셔너리에서 객체 생성"""
        return cls(
            curiyear=data.get("curiyear", ""),
            curismt=data.get("curismt", ""),
            campusdiv=data.get("campusdiv", ""),
            classdiv=data.get("classdiv", ""),
            gbn=data.get("gbn", ""),
            curigbn=data.get("curigbn"),
            comyear=data.get("comyear", ""),
            curinum=data.get("curinum", ""),
            coursecls=data.get("coursecls", ""),
            curinum2=data.get("curinum2", ""),
            curinm=data.get("curinm", ""),
            groupcd=data.get("groupcd", ""),
            cdtnum=data.get("cdtnum", ""),
            cdttime=data.get("cdttime", ""),
            takelim=data.get("takelim", ""),
            listennow=data.get("listennow", ""),
            deptcd=data.get("deptcd", ""),
            deptnm=data.get("deptnm", ""),
            profid=data.get("profid", ""),
            profnm=data.get("profnm", ""),
            largetp=data.get("largetp", ""),
            smalltp=data.get("smalltp", ""),
            abotp=data.get("abotp", ""),
            lecttime=data.get("lecttime", ""),
            dislevel=data.get("dislevel", ""),
            curicontent=data.get("curicontent"),
            bagcnt=data.get("bagcnt", ""),
            dbtimelist=data.get("dbtimelist"),
            sugyn=data.get("sugyn", ""),
            addtime=data.get("addtime"),
            internetyn=data.get("internetyn"),
            flexyn=data.get("flexyn", ""),
            classtype=data.get("classtype", ""),
            lecperiod=data.get("lecperiod", ""),
            bagorder=data.get("bagorder"),
            pastcuridata=data.get("pastcuridata", ""),
            pastcurigrade=data.get("pastcurigrade", ""),
            pastcurigpa=data.get("pastcurigpa", ""),
            lang=data.get("lang", "")
        )
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "curiyear": self.curiyear,
            "curismt": self.curismt,
            "campusdiv": self.campusdiv,
            "classdiv": self.classdiv,
            "gbn": self.gbn,
            "curigbn": self.curigbn,
            "comyear": self.comyear,
            "curinum": self.curinum,
            "coursecls": self.coursecls,
            "curinum2": self.curinum2,
            "curinm": self.curinm,
            "groupcd": self.groupcd,
            "cdtnum": self.cdtnum,
            "cdttime": self.cdttime,
            "takelim": self.takelim,
            "listennow": self.listennow,
            "deptcd": self.deptcd,
            "deptnm": self.deptnm,
            "profid": self.profid,
            "profnm": self.profnm,
            "largetp": self.largetp,
            "smalltp": self.smalltp,
            "abotp": self.abotp,
            "lecttime": self.lecttime,
            "dislevel": self.dislevel,
            "curicontent": self.curicontent,
            "bagcnt": self.bagcnt,
            "dbtimelist": self.dbtimelist,
            "sugyn": self.sugyn,
            "addtime": self.addtime,
            "internetyn": self.internetyn,
            "flexyn": self.flexyn,
            "classtype": self.classtype,
            "lecperiod": self.lecperiod,
            "bagorder": self.bagorder,
            "pastcuridata": self.pastcuridata,
            "pastcurigrade": self.pastcurigrade,
            "pastcurigpa": self.pastcurigpa,
            "lang": self.lang
        }


@dataclass
class LectureSearchResponse:
    """강의 검색 응답 전체 DTO"""
    lectures: List[ResponseLecture]
    
    @classmethod
    def from_list(cls, data: List[dict]) -> 'LectureSearchResponse':
        """딕셔너리 리스트에서 객체 생성"""
        lectures = [ResponseLecture.from_dict(item) for item in data]
        return cls(lectures=lectures)
