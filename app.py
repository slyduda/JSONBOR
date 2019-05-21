import lxml.etree as et
from collections import OrderedDict
from utility.jsbron import jsbron
import json

INSTANCE = "data\\fb\\2019\\10-K\\fb-20181231"
SCHEMA = "data\\fb\\2019\\10-K\\fb-20181231" #NEED TO IMPORT OTHER
CALCULATION = "data\\fb\\2019\\10-K\\fb-20181231_cal"
DEFINITION = "data\\fb\\2019\\10-K\\fb-20181231_def"
LABEL = "data\\fb\\2019\\10-K\\fb-20181231_lab"
PRESENTATION = "data\\fb\\2019\\10-K\\fb-20181231_pre"



jsbron = jsbron()
jsbron.convert_XML(instance=INSTANCE, schema=SCHEMA, calculation=CALCULATION, definition=DEFINITION, label=LABEL, presentation=PRESENTATION)

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

writeToJSONFile('','fb_2019_instance', jsbron.instance)
writeToJSONFile('','fb_2019_calculation', jsbron.taxonomy_calculation)
writeToJSONFile('','fb_2019_definition', jsbron.taxonomy_definition)
writeToJSONFile('','fb_2019_label', jsbron.taxonomy_label)
writeToJSONFile('','fb_2019_presentation', jsbron.taxonomy_presentation)
writeToJSONFile('','fb_2019_schema', jsbron.taxonomy_schema)

print("End of File")