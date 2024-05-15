import re
from typing import Optional, Union
from settings.db import Base, Row, SessionLocal


def row_dict(query_result):
    if isinstance(query_result, Base):
        return query_result.to_dict()
    elif isinstance(query_result, Row):
        _map = dict(query_result._mapping)
        dic = {}
        for key, value in _map.items():
            if isinstance(value, Base):
                dic.update(value.to_dict())
            else:
                dic[key] = value
        return dic
    else:
        raise Exception("query_result should be a Row or Base~")


class CommonQueryParams:
    def __init__(self, q: Optional[str] = "", page: int = 1, page_size: int = 10):
        self.q = re.sub(r'[^[\u4E00-\u9FA5A-Za-z0-9-\u2014_.,，\s()（）]+', '', q)
        self.page = page
        self.page_size = page_size
