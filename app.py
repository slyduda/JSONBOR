from utility.string import truncateFilePath, writeToJSONFile
from utility.jsbron import jsbron

# In order to use this converter simply place each filepath into their respective variable names.
# To change the path outputs change each name in the write to json Function.
# Updates to the structure of the the JSBRON object will be coming soon to better support its multidimensionality.

SUFFIX = "output"

INSTANCE = "data\\fb\\2019\\10-K\\fb-20181231.xml"
SCHEMA = "data\\fb\\2019\\10-K\\fb-20181231.xsd"
CALCULATION = "data\\fb\\2019\\10-K\\fb-20181231_cal.xml"
DEFINITION = "data\\fb\\2019\\10-K\\fb-20181231_def.xml"
LABEL = "data\\fb\\2019\\10-K\\fb-20181231_lab.xml"
PRESENTATION = "data\\fb\\2019\\10-K\\fb-20181231_pre.xml"

jsbron = jsbron()
jsbron.convert_XML(schema=SCHEMA, calculation=CALCULATION, definition=DEFINITION, label=LABEL, presentation=PRESENTATION, delimiter="  ")

writeToJSONFile(truncateFilePath(INSTANCE, suffix=SUFFIX),'fb_2019_instance', jsbron.instance)
writeToJSONFile(truncateFilePath(CALCULATION, suffix=SUFFIX),'fb_2019_calculation', jsbron.taxonomy_calculation)
writeToJSONFile(truncateFilePath(DEFINITION, suffix=SUFFIX),'fb_2019_definition', jsbron.taxonomy_definition)
writeToJSONFile(truncateFilePath(LABEL, suffix=SUFFIX),'fb_2019_label', jsbron.taxonomy_label)
writeToJSONFile(truncateFilePath(PRESENTATION, suffix=SUFFIX),'fb_2019_presentation', jsbron.taxonomy_presentation)
writeToJSONFile(truncateFilePath(SCHEMA, suffix=SUFFIX),'fb_2019_schema', jsbron.taxonomy_schema)

print("End of File")