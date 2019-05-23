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

jsb_2018 = jsbron()
jsb_2018.convert_XML(instance=INSTANCE, schema=SCHEMA, calculation=CALCULATION, definition=DEFINITION, label=LABEL, presentation=PRESENTATION, delimiter="  ")

INSTANCE = "data\\fb\\2018\\10-K\\fb-20171231.xml"
SCHEMA = "data\\fb\\2018\\10-K\\fb-20171231.xsd"
CALCULATION = "data\\fb\\2018\\10-K\\fb-20171231_cal.xml"
DEFINITION = "data\\fb\\2018\\10-K\\fb-20171231_def.xml"
LABEL = "data\\fb\\2018\\10-K\\fb-20171231_lab.xml"
PRESENTATION = "data\\fb\\2018\\10-K\\fb-20171231_pre.xml"

jsb_2017 = jsbron()
jsb_2017.convert_XML(instance=INSTANCE, schema=SCHEMA, calculation=CALCULATION, definition=DEFINITION, label=LABEL, presentation=PRESENTATION, delimiter="  ")

writeToJSONFile(truncateFilePath(INSTANCE, suffix=SUFFIX),'fb_2017_instance', jsb_2017.instance)
writeToJSONFile(truncateFilePath(CALCULATION, suffix=SUFFIX),'fb_2017_calculation', jsb_2017.taxonomy_calculation)
writeToJSONFile(truncateFilePath(DEFINITION, suffix=SUFFIX),'fb_2017_definition', jsb_2017.taxonomy_definition)
writeToJSONFile(truncateFilePath(LABEL, suffix=SUFFIX),'fb_2017_label', jsb_2017.taxonomy_label)
writeToJSONFile(truncateFilePath(PRESENTATION, suffix=SUFFIX),'fb_2017_presentation', jsb_2017.taxonomy_presentation)
writeToJSONFile(truncateFilePath(SCHEMA, suffix=SUFFIX),'fb_2017_schema', jsb_2017.taxonomy_schema)

print("End of File")