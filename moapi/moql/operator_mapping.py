MONGO_OPERATOR_MAPPING: dict[str, str] = {
    "=": "$eq",
    "!=": "$ne",
    ">": "$gt",
    ">=": "$gte",
    "<": "$lt",
    "<=": "$lte",
    "!": "$exists",
    "": "$exists",
}

MOQL_OPERATORS: list[str] = ["<=", ">=", "!=", "=", ">", "<", "!"]
