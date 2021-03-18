import os, sys, json

def FileToList(f):
    try:
        l = []
        with open(f, 'r') as x:
            for line in x.readlines():
                l.append(line.strip())
        return l
    except Exception as e:
        sys.stdout.write(str(e) + '\n')
        sys.stdout.flush()
        sys.exit(1)
    return False

def FileToDict(f, delimiter, remove_quotes=False):
    try:
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
    except Exception as e:
        sys.stdout.write(str(e) + '\n')
        sys.stdout.flush()
        sys.exit(1)
    return False

def LoadDevicesFromJson(f):
    try:
        with open(f, 'rb') as devices_file:
            return json.load(devices_file)["devices"]
    except Exception as e:
        sys.stdout.write(str(e) + '\n')
        sys.stdout.flush()
        sys.exit(1)