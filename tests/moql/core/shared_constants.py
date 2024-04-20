INPUT_HQL_URL_ENCODED: str = (
    "status=DISCOVERED&cvss_score%3E=5.6&active=true"
    "&created%3E2016-01-01&repository.name=/softlayer_sec/i"
    "&limit=100&skip=50&sort=-created&fields=-_id,-jira_id"
)
INPUT_HQL_NOT_ENCODED: str = (
    "status=DISCOVERED&cvss_score>=5.6&active=true"
    "&created>2016-01-01&repository.name=/softlayer_sec/i"
    "&limit=100&skip=50&sort=-created&fields=-_id,-jira_id"
)
EXPECTED_PARAMETER_LIST: list[str] = [
    "status=DISCOVERED",
    "cvss_score>=5.6",
    "active=true",
    "created>2016-01-01",
    "repository.name=/softlayer_sec/i",
    "limit=100",
    "skip=50",
    "sort=-created",
    "fields=-_id,-jira_id",
]

BLACKLIST: tuple[str, ...] = ("repository", "created")
EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED: list[str] = [
    "status=DISCOVERED",
    "cvss_score>=5.6",
    "active=true",
    "limit=100",
    "skip=50",
    "sort=-created",
    "fields=-_id,-jira_id",
]
LESS_OR_EQUALS_THAN: str = "<="
GREATER_OR_EQUALS_THAN: str = ">="
LESS_THAN: str = "<"
GREATER_THAN: str = ">"
NOT_EQUALS: str = "!="
EQUALS: str = "="
NOT: str = "!"
