import lxml.etree as et
from collections import OrderedDict
from utility.jsbon import JSBON
import json

PY_FILE_PATH = "data\\0000002488-18-000042-ex-101-ins---xbrl-instance-document.xml"
CY_FILE_PATH = "data\\0000002488-19-000011-ex-101-ins---xbrl-instance-document.xml"


def parse_nsmap(NS_MAP, file):
    """
        Used to gather missing namespaces to all events in root of XML document.

        Attr:
            NS_MAP(dictionary): Dictionary of key value pairings for namespaces.
            file(str): The path where the file is stored.

        Brought over from http://effbot.org/zone/element-namespaces.htm
        Used only with import xml package.
    """
    events = "start", "start-ns", "end-ns"

    root = None
    ns_map = []

    for event, elem in et.iterparse(file, events):
        if event == "start-ns":
            ns_map.append(elem)
        elif event == "end-ns":
            ns_map.pop()
        elif event == "start":
            if root is None:
                root = elem
            elem.set(NS_MAP, dict(ns_map))

    return et.ElementTree(root)


def parse_period(text):
    """XBRL docs contain a concatenated period of performance for each item. Use this to break string up.

        Attr:
            text(str): The initial part of the contextRef attribute.
    """ 
    period_dict = OrderedDict()
    prefix = ""
    year = ""
    quarter = ""
    start = ""

    while text[0] is not "2":
        prefix += text.pop(0)

    while text[0] is not "Q":
        year += text.pop(0)
    #This will fail if there is a different concat
    for t in range(2):
        quarter += text.pop(0)

    start = text

    period_dict["prefix"] = prefix
    period_dict["year"] = year
    period_dict["quarter"] = quarter
    period_dict["start"] = start

    return period_dict
    

def create_dict(element):
    """Used to create an organized dict of all values necessary for key audit.

        Attr:
            element: Element obj from xml package to be parsed.
    """
    item_dict = {"period":"temp","amount":"temp","id":"temp","tags":[]}
    for name, value in sorted(element.items()):
        if name == "contextRef":
            #Double check to see if other XBRL Docs use "." in their data
            # Found one issue with AMD XBRL 10K should not happen
            value = value.split(".")[0]
            # End of additional code
            values = value.split("_")
            item_dict['period'] = parse_period(values.pop(0))
            while values:
                pair = (values.pop(0), values.pop(0))
                item_dict['tags'].append(pair)
        elif name == "id":
            item_dict["id"] = value
        elif name == "decimals":
            item_dict["decimals"] = value
        item_dict["amount"] = element.text
    return item_dict
    

def remove_namespace(tag, name, ns_dict):
    """Used to remove namespaces from tags to create keys in dictionary for quick key lookup.

        Attr:
            tag(str): Full tag value. Should include namespace by default.
            name(str): The namespace key. Usually the ticker of the company.
            ns_dict(dictionary): Mapping of all the namespace links.
    """
    tag = tag.replace('{}'.format(ns_dict[name]), '')
    tag = tag.replace('{', '')
    tag = tag.replace('}', '')
    return tag

# Specifically for XBRL files with events in attributes. Not including this would result in blank namespaces.
CY_COMP_DICT = {}
PY_COMP_DICT = {}

jsbon = JSBON()
jsbon.parse_XML(CY_FILE_PATH)

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

writeToJSONFile('','JSBON', jsbon.instance)

print("End of File")