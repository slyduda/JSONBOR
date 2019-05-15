import xml.etree.ElementTree as et

PY_FILE_PATH = "data\\0000002488-18-000042-ex-101-ins---xbrl-instance-document.xml"
CY_FILE_PATH = "data\\0000002488-19-000011-ex-101-ins---xbrl-instance-document.xml"

NS_MAP = "xmlns:map"

def parse_nsmap(file):
    """
        Used to gather missing namespaces to all events in root of XML document.

        Attr:
            file(str): The path where the file is stored.

        Brought over from http://effbot.org/zone/element-namespaces.htm

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

def create_dict(tree):
    dic = {}
    for child in tree:
        pass
        
# Specifically for XBRL files with events in attributes. Not including this would result in blank namespaces.
tree = parse_nsmap(PY_FILE_PATH)
root = tree.getroot()


print(root.tag)
print(root.attrib)

#for child in root:
#    temp = str(child.tag)
#    if temp.startswith(root.attrib["xmlns:map"]["us-gaap"],1):
#        if len(str(child.text)) < 100:
#            print(child.text)

financial_list = et.SubElement(root, root.attrib["xmlns:map"]["amd"])
us_gaap_list = et.SubElement(root, root.attrib["xmlns:map"]["us-gaap"])
print(financial_list)
print(us_gaap_list)

print("End of File")