import os
import json

def writeToJSONFile(path, fileName, data):
    path =   '.\\' + path + '\\'
    if not os.path.exists(path):
        os.makedirs(path)
    filePathNameWExt = path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


def truncateFilePath(string, suffix=None, parts=1):
    """Function that takes a file that was loaded already and truncates it to make a sub folder with a child folder specified.

        Attr:
            string(str): Original path to be truncated.
            suffix(str): Altered path inside of truncated path.
            parts(int): How far you would like to truncate it. Set to 1 by default for directories with a file at the end.

    """
    string = string.split("\\")
    string.pop()
    new_string = ""
    for s in string:
        new_string += s + "\\"
    if suffix:
        new_string += suffix + "\\"
    new_string = new_string[:-1]
    return new_string