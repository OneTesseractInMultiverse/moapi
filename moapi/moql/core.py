from typing import Optional, Callable
from urllib import parse

from moapi.moql.constants import (
    FILTERS_KEY,
    SORT_KEY,
    SKIP_KEY,
    LIMIT_KEY,
    PROJECTION_KEY,
    QUERY_STRING_PARAM_SEPARATOR,
    FIELDS_KEY,
    TEXT_KEY,
    FILTER,
)
from moapi.moql.filter_handler import MoQLFilter
from moapi.moql.limit_skip_handler import MoQLLimitHandler, MoQLSkipHandler
from moapi.moql.projection_handler import MoQLProjection
from moapi.moql.sort_handler import MoQLSortHandler
from moapi.moql.text_search_handler import MoQLTextSearch


MONGO_QUERY_TEMPLATE: dict[str, any] = {
    FILTERS_KEY: {},
    SORT_KEY: None,
    SKIP_KEY: 0,
    LIMIT_KEY: 0,
    PROJECTION_KEY: None,
}
EMPTY_STRING: str = ""


# ---------------------------------------------------------
# PARSE QUERY AS KEY VALUE
# ---------------------------------------------------------
def extract_parameter_list(hql_query: str) -> list[str]:
    return list(
        parse.unquote(hql_query).split(QUERY_STRING_PARAM_SEPARATOR)
    )


# ---------------------------------------------------------
# REMOVE BLACKLISTED
# ---------------------------------------------------------
def remove_blacklisted(hql_query: str, blacklist: tuple[str, ...] | None):
    raw_parameters: list[str] = extract_parameter_list(hql_query=hql_query)
    if blacklist:
        return [
            parameter
            for parameter in raw_parameters
            if not parameter.startswith(blacklist)
        ]
    return raw_parameters


def is_text_search_argument(parameter):
    return parameter.startswith(f"{TEXT_KEY}=")


def is_projection_argument(parameter):
    return parameter.startswith(f"{FIELDS_KEY}=")


def is_skip_argument(parameter):
    return parameter.startswith(f"{SKIP_KEY}=")


def is_limit_argument(parameter):
    return parameter.startswith(f"{LIMIT_KEY}=")


def is_sort_argument(parameter):
    return parameter.startswith(f"{SORT_KEY}=")


class MoQL:
    # -----------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(
        self,
        moql: str,
        blacklist: Optional[tuple[str, ...]] = None,
        casters: Optional[dict[str, Callable]] = None,
    ):
        self.moql: str = moql
        self.blacklist = blacklist
        self.raw_parameters: list[str] = remove_blacklisted(
            hql_query=self.moql, blacklist=self.blacklist
        )
        self.casters: Optional[dict[str, Callable]] = casters
        self.output_query: dict[str, any] = {
            FILTER: {},
            SORT_KEY: None,
            SKIP_KEY: 0,
            LIMIT_KEY: 0,
            PROJECTION_KEY: None,
        }
        self.process_parameters()

    # -----------------------------------------------------
    # METHOD PROCESS PARAMETERS
    # -----------------------------------------------------
    def process_parameters(self):
        for parameter in self.raw_parameters:
            if is_sort_argument(parameter):
                self.sort(parameter)
            elif is_limit_argument(parameter):
                self.limit(parameter)
            elif is_skip_argument(parameter):
                self.skip(parameter)
            elif is_projection_argument(parameter):
                self.project(parameter)
            elif is_text_search_argument(parameter):
                self.search_text(parameter)
            elif parameter != EMPTY_STRING:
                self.filter(parameter)

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------
    def filter(self, parameter):
        for key, sub_filter in MoQLFilter(
            filter_parameter=parameter, custom_casters=self.casters
        ).filter.items():
            if key in self.output_query[FILTER]:
                self.output_query[FILTER][key] = {
                    **self.output_query[FILTER][key],
                    **sub_filter,
                }
            else:
                self.output_query[FILTER][key] = sub_filter

    # -----------------------------------------------------
    # SEARCH TEXT
    # -----------------------------------------------------
    def search_text(self, parameter):
        self.output_query[FILTER].update(
            MoQLTextSearch(text_search_parameter=parameter).filter
        )

    # -----------------------------------------------------
    # PROJECT
    # -----------------------------------------------------
    def project(self, parameter):
        self.output_query[PROJECTION_KEY] = MoQLProjection(
            projection_parameter=parameter
        ).projection

    # -----------------------------------------------------
    # SKIP
    # -----------------------------------------------------
    def skip(self, parameter):
        self.output_query[SKIP_KEY] = MoQLSkipHandler(
            skip_parameter=parameter
        ).skip

    # -----------------------------------------------------
    # LIMIT
    # -----------------------------------------------------
    def limit(self, parameter):
        self.output_query[LIMIT_KEY] = MoQLLimitHandler(
            limit_parameter=parameter
        ).limit

    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------
    def sort(self, parameter):
        self.output_query[SORT_KEY] = MoQLSortHandler(
            sort_parameter=parameter
        ).query_element

    # -----------------------------------------------------
    # PROPERTY MONGO QUERY
    # -----------------------------------------------------
    @property
    def mongo_query(self) -> dict[str, any] | None:
        return self.output_query
