def float_text(string):
    for i in xrange(len(string)):
        if float_substring(string[:len(string)-i]):
            return string[:len(string)-i]
    return ""

def float_substring(string):
    string=string.strip()
    if string == "":
        return True
    special_chars = ["+", "-", ".", "e", "E"]
    try:
        if string[-1] in special_chars:
            string = string + "0"
        float(string)
        return True
    except ValueError:
        return False
