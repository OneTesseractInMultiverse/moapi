import datetime

from moapi.adapters.query_string import QueryString

from moapi.models.core.entity import Entity

SEVERITY_VALUE: str = "High"
SCORE_VALUE: int = 0
CVSS_VALUE: float = 1.3
CREATED_VALUE: datetime = datetime.datetime(day=10, month=10, year=2023)
TAGS_VALUE: list[str] = ["a", "b", "c"]


class DummyModel(Entity):
    severity: str = None
    score: int = 0
    cvss: float = 1.3
    created: datetime.datetime = datetime.datetime.now(datetime.UTC)
    tags: list[str] = []


def get_dummy_model() -> DummyModel:
    return DummyModel(
        severity=SEVERITY_VALUE,
        score=SCORE_VALUE,
        cvss=CVSS_VALUE,
        created=CREATED_VALUE,
        tags=TAGS_VALUE,
    )


class DummyModelQuery(QueryString[DummyModel]):
    def __init__(self, query_string: dict):
        super().__init__(query_string)


DUMMY_MODEL_QUERY_EQUALITY: dict = {
    "severity": SEVERITY_VALUE,
    "score": SCORE_VALUE,
    "cvss": CVSS_VALUE,
    "created": CREATED_VALUE,
}

# ---------------------------------------------------------
# NOT EQUALS OPERATOR CASES
# ---------------------------------------------------------

NOT_EQUALS_STR_QUERY: dict = {"severity": "~neq~Low"}
NOT_EQUALS_INT_QUERY: dict = {"score": "~neq~10"}
NOT_EQUALS_FLOAT: dict = {"cvss": "~neq~1.3"}
NOT_EQUALS_DATE: dict = {"cvss": "~neq~2023-10-10"}

# ---------------------------------------------------------
# GREATER THAN OPERATOR CASES
# ---------------------------------------------------------

# Should produce value error
GREATER_THAN_STR: dict = {"severity": "~gt~High"}
GREATER_THAN_INT: dict = {"score": "~gt~2"}
GREATER_THAN_FLOAT: dict = {"cvss": "~gt~0.5"}
GREATER_THAN_DATE: dict = {"created": "~gt~2023-10-10"}
