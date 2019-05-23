import lxml.etree as et
import xmlschema

class jsbron():
    def __init__(self):
        self.instance = {}
        self.taxonomy_schema = {}
        self.taxonomy_calculation = {}
        self.taxonomy_definition = {}
        self.taxonomy_label = {}
        self.taxonomy_presentation = {} 
        self.dei = {}

    def get_dei(self):
        if self.instance:
            dei = self.instance["xbrli"]["xbrl"][0]['dei']
            for k,v in dei.items():
                #Ignores second object within a tag. Good exmaple can be seen in FB 2019 10k
                dei[k] = v[0]["value"]
            self.dei = dei


    def compare_financials(self, PY_jsbron, us_gaap=False, ifrs=False, ticker=None):
        """Compare a current year JSBRON object with a PY object to identify all matching values with the same tags. Results in a Dictionary with two root values.

            PY_jsbron(jsbron obj): Prior Year financials.
            us_gaap(bool): If US GAAP related financials exists in the instance.
            ifrs(bool): If IFRS related financials exists in the instance.
            ticker(str): The ticker if self.dei is empty.
        """

        #need to compare us_gaap (could also be IFRS for foreign entity)
        #need to compare dei ticker name namespace

        if self.dei:
            ticker = self.dei["TradingSymbol"]

        if not self.instance or not PY_jsbron.instance:
            print("An instance of either JSBRON Objects are missing")
            return

        search_dict = {}
        PY_dict = {}
        if us_gaap:
            search_dict.update(self.instance["xbrli"]["xbrl"]["us_gaap"])
            PY_dict.update(self.instance["xbrli"]["xbrl"]["us_gaap"])
        if ifrs:
            search_dict.update(self.instance["xbrli"]["xbrl"]["ifrs"])
            PY_dict.update(self.instance["xbrli"]["xbrl"]["ifrs"])
        if ticker:
            search_dict.update(self.instance["xbrli"]["xbrl"][ticker])
            PY_dict.update(self.instance["xbrli"]["xbrl"][ticker])
        result = {"tied":{}, "errors":{}}
        #each key will be associated a list of values
        for key, values in search_dict.items():
            for value in values:
                match = False
                PY_values = PY_dict[key]
                possibilities = []
                for PY_value in PY_values:
                    if value["context"] == PY_value["context"] and value['value'] == PY_value['value']:
                        match = True
                    elif value['context'] == PY_value['context']:
                        possibilities.append(PY_value)
                if match:
                    result["tied"].update(value)
                else:
                    possibilities = {"possibilities": possibilities}
                    value.update(possibilities)
                    result["errors"].update(value)

        return result
            
            
    @staticmethod
    def convert_to_text(xml_file, schema=False):
        if schema:
            tree = xmlschema.XMLResource(xml_file)
            string = tree.tostring(indent='  ', spaces_for_tab=2)
        else:
            tree = et.parse(xml_file)
            string = et.tostring(tree, encoding='utf-8').decode('utf-8')
        return string


    def convert_XML(self, instance=None, schema=None, calculation=None, definition=None, label=None, presentation=None, delimiter="\t"):
        """Used to store pieces of xml as a jsbron obj.

            Attr:
                instance(str): XML file location for the instance.
                schema(str): XML file location for the taxonomy schema.
                calculation(str): XML file location for the taxonomy calculations.
                definition(str): XML file location for the taxonomy definition.
                label(str): XML file location for the taxonomy label.
                presentation(str): XML file location for the taxonomy presentation.
                delimiters
        """

        if instance:
            result = self.parse_XML(self.convert_to_text(instance),delimiter)
            self.instance = result
        if schema:
            result = self.parse_XML(self.convert_to_text(schema, schema=True),delimiter)
            self.taxonomy_schema = result
        if calculation:
            result = self.parse_XML(self.convert_to_text(calculation),delimiter)
            self.taxonomy_calculation = result
        if definition:
            result = self.parse_XML(self.convert_to_text(definition),delimiter)
            self.taxonomy_definition = result
        if label:
            result = self.parse_XML(self.convert_to_text(label),delimiter)
            self.taxonomy_label = result
        if presentation:
            result = self.parse_XML(self.convert_to_text(presentation),delimiter)
            self.taxonomy_presentation = result


    @staticmethod
    def parse_XML(string, delimiter="\t"):

        location = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}, 13:{}, 14:{}, 15:{}, 16:{}, 17:{}, 18:{}, 19:{}}
        loc_ref = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}, 13:{}, 14:{}, 15:{}, 16:{}, 17:{}, 18:{}, 19:{}}

        tag_spacing = []
        prop_spacing = 0

        def clean_dict(tab_current, tag_spacing, loc_ref, jsbron_dict, decrease=False):
            new_spacing = []
            for n in range(tab_current):
                new_spacing.append(tag_spacing[n])
            dict_pos = sum(new_spacing)

            for k, v in jsbron_dict.items():
                if int(k) >= dict_pos:
                    jsbron_dict[k] = dict()
            
            temp = jsbron_dict[dict_pos-1]
            
            name = loc_ref[dict_pos-1]['name']
            obj_pos = loc_ref[dict_pos-1]['obj_pos']
            jsbron_dict[dict_pos] = temp[name][obj_pos]

            for k,v in loc_ref.items():
                if int(k) >= dict_pos:
                    loc_ref[k] = dict()

            return (new_spacing,jsbron_dict)


        def construct(text, namespace=False, tag=False, value=False, prop_ns=False, prop_tag=False, prop_val=False):
            """Use this to build generate the next structure of the dict.

                Attr:
                    text(str): Word that was parsed in the XML file.
                    others(bool): Used to determine what kind of structure to build with the text.

            """
            text = text[:-1]
            wrapper = ""
            if namespace:
                # Spit out dict.
                wrapper = ({ text: {}}, {'class':'namespace'})
            elif tag:
                # Spit out tuple.
                wrapper = ({ text: []}, {'class':'tag'})
            elif value:
                # Spit out dict.
                wrapper = ({'value': text}, None)
            elif prop_ns:
                # Spit out tuple.
                wrapper = ({ text: {}}, None)
            elif prop_tag:
                # Spit out dict.
                wrapper = ({ text: ""}, None)
            elif prop_val:
                # Spit out str.
                wrapper = (text, None)
            else:
                print("critical error need to pick one.")
            return wrapper


        text = ""
        temp_prop_value = ""

        tab_current = 0
        obj_pos = 0
        
        new_line = False
        inside_tag = False
        inside_tag_name = False
        inside_tag_properties = False
        inside_tag_properties_value = False

        inside_comment = False
        inside_value = False
        inside_closing_tag = False
        
        for char in string:
            text += char

            #Check to see if there is a new line.
            if text == "\n":
                new_line = True
                inside_value = False
                prop_spacing = 0
                tab_current = 0
                text = ""
                continue

            #Check for spacing.
            if new_line:
                if text == delimiter or text == '\t':
                    tab_current += 1
                    text = ""
                    continue

            #Check to see if the tag is a comment.
            if text == "!--" and inside_tag:
                inside_tag = False
                inside_tag_name = False
                inside_comment = True
                continue

            if text == "?" and inside_tag:
                inside_tag = False
                inside_tag_name = False
                inside_comment = True
                continue

            #Check to see if this def is part of a new line. Need to change 0 requirement soon.
            if char == "<" and new_line and tab_current is not 0:
                new_line = False
                if tab_current < len(tag_spacing):
                    tag_spacing, location = clean_dict(tab_current, tag_spacing, loc_ref, location)
                elif tab_current > len(tag_spacing):
                    tag_spacing, location = clean_dict(tab_current, tag_spacing, loc_ref, location, decrease=True)
           
            #Check to see if contents outside of a tag were important. Need to figure out how to do this efficiently.
            if char == "<" and inside_value:
                piece1, piece2 = construct(text, value=True)
                position = sum(tag_spacing)
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)

                inside_value = False
                inside_closing_tag = True
                text = ""
                continue

            #Check to see if there is an item coming up.
            if char == "<" and not inside_tag:
                inside_tag = True
                inside_tag_name = True
                text = ""
                continue
            
            #Check to see if the item is closing to post tag if abrupt.
            if char == ">" and inside_tag_name:
                piece1, piece2 = construct(text, tag=True)
                position = sum(tag_spacing)
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)
                location[position + 1] = location[position][text[:-1]]
                obj_pos = len(location[position + 1])
                location[position + 1].append({})
                location[position + 1] = location[position][text[:-1]][obj_pos]

                loc_ref[position] = {"name": str(text[:-1]), "obj_pos": int(obj_pos)}

                if tag_spacing[tab_current]:
                    tag_spacing[tab_current] = 2
                else:
                    tag_spacing.append(1)

                inside_tag = False
                inside_tag_name = False
                inside_tag_properties = False
                inside_tag_properties_value = False
                inside_value = True
                text = ""
                continue

            #Check to see if  the item has closed.
            if char == ">" and inside_tag:
                inside_tag = False
                inside_tag_name = False
                inside_tag_properties = False
                inside_tag_properties_value = False
                inside_value = True
                text = ""
                continue

            #Check to see when the comment ends. Could fail need to adjust to vire last 3 chars.
            if char == ">" and inside_comment:
                inside_comment = False
                text = ""
                continue

            #Check to see when the end tag is done.
            if char == ">" and inside_closing_tag:
                inside_closing_tag = False
                text = ""
                continue

            
            if char == "/" and inside_tag_name:
                inside_tag = False
                inside_tag_name = False
                inside_tag_properties = False
                inside_tag_properties_value = False
                inside_closing_tag = True
                text = ""
                continue

            #Check to see if the text should be a tag namespace.
            if char == ":" and inside_tag_name:
                piece1,piece2 = construct(text, namespace=True)
                position = sum(tag_spacing)
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)
                location[position + 1] = location[position][text[:-1]]
                tag_spacing.append(1)
                text = ""
                continue

            #Check to see if there is a separator right after the tag name. Will work if there are random spaces inside def.
            if char == " " and inside_tag_name:
                piece1, piece2 = construct(text, tag=True)
                position = sum(tag_spacing)
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)
                location[position + 1] = location[position][text[:-1]]
                obj_pos = len(location[position + 1])
                location[position + 1].append({})
                location[position + 1] = location[position][text[:-1]][obj_pos]
                loc_ref[position] = {"name": str(text[:-1]), "obj_pos": int(obj_pos)}
                
                if tag_spacing[tab_current]:
                    tag_spacing[tab_current] = 2
                else:
                    tag_spacing.append(1)

                inside_tag_name = False
                inside_tag_properties = True
                text = ""
                continue

            #Ignore spaces in between or after tag properties.
            #@@@@@@@@@@@@@WILL FAIL IF THERE ARE SPACES inside str properties
            if char == " " and inside_tag_properties:
                prop_spacing = 0
                text = ""
                continue

            #Check to see if the text should be a tag property ns.
            if char == ":" and inside_tag_properties and not inside_tag_properties_value:
                piece1, piece2 = construct(text, prop_ns=True)
                position = sum(tag_spacing) + prop_spacing
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)
                location[position + 1] = location[position][text[:-1]]
                prop_spacing += 1

                text = ""
                continue
            
            #Check to see if the tag is finished but do not trigger value. 
            if char == "=" and inside_tag_properties:
                piece1, piece2 = construct(text, prop_tag=True)
                position = sum(tag_spacing) + prop_spacing
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position].update(piece1)
                temp_prop_value = str(text[:-1])
                text = ""
                continue

            #Check to see if tag starts.
            if char == '"' and inside_tag_properties and not inside_tag_properties_value:
                inside_tag_properties_value = True
                text = ""
                continue

            if char == '"' and inside_tag_properties and inside_tag_properties_value:
                piece1, piece2 = construct(text, prop_val=True)
                position = sum(tag_spacing) + prop_spacing
                if text[:-1] in location[position].keys():
                    pass
                else:
                    location[position][temp_prop_value] = piece1
                
                inside_tag_properties_value = False
                temp_prop_value = ""
                text = ""
                continue

        return location[0]