import lxml.etree as et

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


def create_dict(element):
    """Used to create an organized dict of all values necessary for key audit.

        Attr:
            element: Element obj from xml package to be parsed.
    """
    item_dict = {"period":"temp","amount":"temp","id":"temp","tags":[]}
    for name, value in sorted(element.items()):
        if name == "contextRef":
            values = value.split("_")
            item_dict['period'] = values.pop(0)
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
tree = et.parse(CY_FILE_PATH)
root = tree.getroot()
name = 'us-gaap'
elements = tree.xpath('/xbrli:xbrl/{}:*'.format(name), namespaces=root.nsmap)

for element in elements:
    element_tag = remove_namespace(element.tag,name,root.nsmap)
    CY_COMP_DICT.setdefault(element_tag,[])
    CY_COMP_DICT[element_tag].append(create_dict(element))

for element in elements:
    element_tag = remove_namespace(element.tag,name,root.nsmap)
    CY_COMP_DICT.setdefault(element_tag,[])

print("End of File")