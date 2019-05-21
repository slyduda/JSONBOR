import os
import json
import lxml.etree as et
from collections import OrderedDict
from utility.string import truncateFilePath
from utility.jsbron import jsbron

SUFFIX = "output"

INSTANCE = "data\\fb\\2019\\10-K\\fb-20181231.xml"
SCHEMA = "data\\fb\\2019\\10-K\\fb-20181231.xsd" #NEED TO IMPORT OTHER
CALCULATION = "data\\fb\\2019\\10-K\\fb-20181231_cal.xml"
DEFINITION = "data\\fb\\2019\\10-K\\fb-20181231_def.xml"
LABEL = "data\\fb\\2019\\10-K\\fb-20181231_lab.xml"
PRESENTATION = "data\\fb\\2019\\10-K\\fb-20181231_pre.xml"

jsbron = jsbron()
jsbron.convert_XML(instance=INSTANCE, calculation=CALCULATION, definition=DEFINITION, label=LABEL, presentation=PRESENTATION, delimiter="  ")

def writeToJSONFile(path, fileName, data):
    path =   '.\\' + path + '\\'
    if not os.path.exists(path):
        os.makedirs(path)
    filePathNameWExt = path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

writeToJSONFile(truncateFilePath(INSTANCE, suffix=SUFFIX),'fb_2019_instance', jsbron.instance)
writeToJSONFile(truncateFilePath(CALCULATION, suffix=SUFFIX),'fb_2019_calculation', jsbron.taxonomy_calculation)
writeToJSONFile(truncateFilePath(DEFINITION, suffix=SUFFIX),'fb_2019_definition', jsbron.taxonomy_definition)
writeToJSONFile(truncateFilePath(LABEL, suffix=SUFFIX),'fb_2019_label', jsbron.taxonomy_label)
writeToJSONFile(truncateFilePath(PRESENTATION, suffix=SUFFIX),'fb_2019_presentation', jsbron.taxonomy_presentation)
#writeToJSONFile(truncateFilePath(SCHEMA, suffix=SUFFIX),'fb_2019_schema', jsbron.taxonomy_schema)

print("End of File")