import os

def FileToList(f):
    if os.path.exists(f):
        l = []
        with open(f, 'r') as x:
            for line in x.readlines():
                l.append(line.strip())
        return l
    return False

def FileToDict(f, delimiter, remove_quotes=False):
    if os.path.exists(f):
        d = {}
        with open(f, 'r') as x:
            for line in x.readlines():
                try:
                    key, value = line.strip().split(delimiter)
                    if remove_quotes:
                        d[key] = value.replace("'","").replace("\"","")
                    else:
                        d[key] = value
                except:
                    pass
        return d
    return False