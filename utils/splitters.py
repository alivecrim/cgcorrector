def splitByDigit(str_for_split: str) -> list:
    splitIndex: int = 0
    for idx, c in enumerate(str_for_split):
        if str.isdigit(c):
            splitIndex = idx
            break
    returnList = [str_for_split[:splitIndex], str_for_split[splitIndex:]]
    return returnList
