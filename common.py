# Builds up a single string on multiple lines
def makeline(*args):
    result = ""
    for arg in args:
        result += arg

    result += "\n"
    return result