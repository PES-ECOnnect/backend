from data.DBUtils import *


def getReviewableIdForType(typeName: str) -> int:
    q = "SELECT TypeId FROM ReviewableType WHERE name = ?"
    return selectQuery(q, (typeName,), True)

