import lxml.etree as et

class JSBON():
    def __init__(self):
        self.instance = {}
        self.taxonomy_calc = {}
        self.taxonomy_def = {}
        self.taxonomy_lab = {}
        self.taxonomy_pres = {}
    

    def create_JSBON(element=None):
        temp = {}

        tree = et.parse(element)
        root = tree.getroot()
        name = 'us-gaap'
        elements = tree.xpath('/xbrli:xbrl/{}:*'.format(name), namespaces=root.nsmap)

        for element in elements:
            element_tag = remove_namespace(element.tag,name,root.nsmap)
            temp.setdefault(element_tag,[])
            temp[element_tag].append(create_dict(element))

        return temp    

    def convert_to_JSBON(self, xml_file):
        temp = {}

        tree = et.parse(xml_file)
        string = et.tostring(tree, encoding='utf-8').decode('utf-8')
        return string


    def parse_XML(self, xml_string):
        """Used to parse through XML and write a JSBON obj.

            Attr:
                xml_string(str): XML file location.
        """

        location = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}, 13:{}, 14:{}, 15:{}, 16:{}, 17:{}, 18:{}, 19:{}}
        loc_ref = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}, 13:{}, 14:{}, 15:{}, 16:{}, 17:{}, 18:{}, 19:{}}

        tag_spacing = []
        prop_spacing = 0

        def clean_dict(tab_current, tag_spacing, loc_ref, jsbon_dict, decrease=False):
            new_spacing = []
            for n in range(tab_current):
                new_spacing.append(tag_spacing[n])
            dict_pos = sum(new_spacing)

            for k,v in jsbon_dict.items():
                if int(k) >= dict_pos:
                    jsbon_dict[k] = dict()
            
            temp = jsbon_dict[dict_pos-1]
            
            name = loc_ref[dict_pos-1]['name']
            obj_pos = loc_ref[dict_pos-1]['obj_pos']
            jsbon_dict[dict_pos] = temp[name][obj_pos]

            for k,v in loc_ref.items():
                if int(k) >= dict_pos:
                    loc_ref[k] = dict()

            return (new_spacing,jsbon_dict)


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
        
        
        def determine_location(tag_spacing, tab_current, namespace=False, tag=False):
            """Used to find the current location in the dict to place the generated structure.

                Attr:
                    tag_spacing(int): The amount of tab delimiters in the last line.
                    tab_previos(int): The amount of tab delimiters in the current line.
            """
            global location, current_location
            
            addition = 0

            if tag:
                addition = 1

            position = tab_current + addition
            return position

        tree = et.parse(xml_string)
        string = et.tostring(tree, encoding='utf-8').decode('utf-8')

        text = ""
        temp_prop_value = ""

        tab_previous = 0
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
                tab_previous = int(tab_current)
                prop_spacing = 0
                tab_current = 0
                text = ""
                continue

            #Check to see if new item is a child or in line.
            if text == "\t":
                tab_current += 1
                text = ""
                continue

            #Check to see if the tag is a comment.
            if text == "!--" and inside_tag:
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
        
        self.instance = location[0]