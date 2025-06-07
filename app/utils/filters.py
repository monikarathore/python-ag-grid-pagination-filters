# app/utils/filters.py
from sqlalchemy.sql import func, and_, or_

def build_text_filter_condition(column_attr, filter_type, filter_value):
    filter_value_lower = (filter_value or "").lower()

    if filter_type == "contains":
        return func.lower(column_attr).like(f"%{filter_value_lower}%")
    elif filter_type == "notContains":
        return ~func.lower(column_attr).like(f"%{filter_value_lower}%")
    elif filter_type == "equals":
        return func.lower(column_attr) == filter_value_lower
    elif filter_type == "notEqual":
        return func.lower(column_attr) != filter_value_lower
    elif filter_type == "startsWith":
        return func.lower(column_attr).like(f"{filter_value_lower}%")
    elif filter_type == "endsWith":
        return func.lower(column_attr).like(f"%{filter_value_lower}")
    elif filter_type == "blank" or filter_type == "empty":
        return or_(column_attr == None, func.trim(column_attr) == "")
    elif filter_type == "notBlank":
        return and_(column_attr != None, func.trim(column_attr) != "")
    else:
        # Unknown filter type, no filter applied
        return True

def build_filter_for_column(column_attr, filter_data):
    operator = filter_data.get("operator")
    cond1 = filter_data.get("condition1")
    cond2 = filter_data.get("condition2")

    if not operator:
        return build_text_filter_condition(
            column_attr,
            filter_data.get("type"),
            filter_data.get("filter")
        )
    
    cond1_expr = build_text_filter_condition(
        column_attr,
        cond1.get("type"),
        cond1.get("filter")
    ) if cond1 else True

    cond2_expr = build_text_filter_condition(
        column_attr,
        cond2.get("type"),
        cond2.get("filter")
    ) if cond2 else True

    if operator.upper() == "AND":
        return and_(cond1_expr, cond2_expr)
    elif operator.upper() == "OR":
        return or_(cond1_expr, cond2_expr)
    else:
        return and_(cond1_expr, cond2_expr)
