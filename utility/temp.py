    # Namespaces cannot have meta data
    # If child namespace is the same as parent, no need to redeclare
    {
        "xbrli":
        {
            "class": "namespace",
            "xbrl":
            [{
                "class": "tag",
                "meta":{
                    # The root tag will always include an NS_MAP shown below.
                    "xmls":{"amd":"http", "country":"http", "link":"http"},
                }
                "link":{
                    "class": "namespace",
                    "schemaRef":
                    [{
                        "class":"tag"
                        "meta":{
                            "xlink":{
                                "href":"amd.xsd",
                                "type": "simple"
                            }
                        }
                    }],
                    "loc":
                    [{

                    },
                    {

                    }],
                    "footnoteLink":[{
                        "xlink":{
                            "role": "http://www.xbrl.org/2003/role/link",
                            "type": "extended"
                        }
                        "loc":[{

                        }]
                    }]
                
                }
                "amd":
                {
                    "class": "namespace"
                    "AccountsRec":
                    [{
                        "class": "tag",
                        'properties':{
                            "contextRef": {
                                "year": "2027",
                                "quarter": "Q4", 
                                "tags": [("us-gaap","debt")]
                                },
                            "id": "3678678678",
                            "unitRef": "usd",
                        }
                        "namespaces": {None},
                        "value":"678879"
                    },
                    {
                        'tags':{
                            "contextRef": ["FI2017YTD",{"amd":"General"}],
                            "id": "3678678678",
                            "unitRef": "usd",
                        }
                        "namespaces": {None},
                        "value":"678879"
                    }]
                },
                {
                    "us-gaap"
                }
            }],
            "context":[{
                "tags":{
                    "id": ["FI2017YTD"],
                },
                "entity":[{
                    "identifier":[{

                    }]
                }],
                "period":[{
                    #Typical parse would wrap this in a dict
                    "star_date": "2017-01-01",
                    "end_date": "2017-12-30"
                }]
            }],
            "unit":[{

            }]
        }
    }