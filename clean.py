import os
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
import sys
import codecs
from collections import defaultdict
import os
from audit import is_street_name,street_type_re,audit_shops,audit_house_number
mapXML='bucharest_romania.osm'     # import Bucharest osm from OpenStreetMap

#CLEAN STREETS  
expected = ["Aleea", "Calea", "Bulevardul", "Drumul", "Intrarea", "Pia?a", "?oseaua", "Strada","Splaiul","Prelungirea"] #most common street types in Bucharest
  

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit(filename):
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(mapXML, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

st_types = audit(mapXML)

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

if __name__ == '__main__':    
    MyPrettyPrinter().pprint(dict(st_types))
    
                       
# Mapping correct street type
mapping_street = {"sos": u"?oseaua",
           "Spaiul.": "Splaiul",
           "Str.":"Strada",
           "Piata":u"Pia?a",
           "Dr.":"Drumul",
           "Drum":"Drumul",
           "drumul":"Drumul",
           "Bulevbardul":"Bulevardul",
           "B-dul":"Bulevardul",
           "strada":"Strada",
           "Soseaua":u"?oseaua",
           "Spaiul":"Splaiul",
           "strada":"Strada",
           "Sf.":"Sfantul",
           "pictor":"Pictor",
           "Campia":u"Campia"       
          }

def update_street(name, mapping_street):
    m = street_type_re.search(name)
    better_name = name
    # condition: if the street name does have a last word
    if m:
        # check if the street type is a key in your mapping dictionary:
        if m.group() in mapping_street.keys():
            better_street_type = mapping_street[m.group()]
            better_name = street_type_re.sub(better_street_type, name)
        return better_name
   

print '----CLEAN STREETS-----'
for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_street(name, mapping_street)
            print name, "=>", better_name


#CLEAN MOBILE SHOPS   
expected = ["Vodafone", "Orange", "Telekom"]
                         
#correct shop names
mapping_shop = {"Arsis Vodafone": "Vodafone",
           "Cosmote / Romtelecom": "Telekom",
           "Interniti, Cosmote": "Telekom",
           "Cosmote": "Telekom",
           "Interniti, Cosmote ": "Telekom",
           "Germanos":"Telekom",
           u"Germanos Baneasa":"Telekom",
           "Germanos Promenada":"Telekom",
           "Ilex Vodafone":"Vodafone",
           "Orange Shop":"Orange",
           "Orange Store":"Orange",
           "Orange Titan":"Orange",
           "Telekom Titan":"Telekom",
           "Vodafone"+' "ILEX"':"Vodafone",
           "Vodafone Arsis":"Vodafone",
           "Vodafone Titan":"Vodafone",
           "Vodafone Vasile Milea":"Vodafone"
          }

def update_mobile_shop(name, mapping_shop):    
    '''update shop names with mapping_shop dict values'''
    for key,value in mapping_shop.items():
        if name==key:
            name=value
        else:
            continue
    return name

print '----CLEAN MOBILE SHOPS NAME-----'
for name in  audit_shops(mapXML):
    better_name = update_mobile_shop(name, mapping_shop)
    print name, "=>", better_name            
    

#CLEAN HOUSENUMBER
mapping_housenumber = { "B-dul. Iuliu Maniu, nr.79, Sector 6": "79", #dict for corrections on housenumber
            "185Miniprix": "185",
            "Bl. 43": "No_number",
            "Bl. 50": "No_number",
            "Bl. 37": "No_number",  
            "Bl. 38": "No_number",           
            "106R.  Can Pack": "106R",
            "Bl. PM91":"No_number",
            "Sos. Pipera-Tunari, nr.1C, Sector 2":"1C",
            "Brasov":"No_number",
            "F.N.":"No_number",
            "37/I":"37I",
            "31B+C":"31B,C",
            "Bl. 5":"No_number",
            "Bl. 4":"No_number", 
            "Bl. 7":"No_number",
            "Bl. 1":"No_number", 
            "Bl. 3":"No_number",
            "Bl. M15":"No_number", 
            "37/J":"37J",                       
            "486Petrom":"486",
            "4, Ap.2, Sector 5":"4",
            "bl. 1":"No_number",
            "bl. 2":"No_number", 
            "Bl. P2":"No_number",
            "1A villa 40":"No_number",
            "Bloc F5":"No_number",
            "Bloc C5":"No_number",
            "Soseaua Virtutii":"No_number",
            "Nr. 232":"232", 
            "Bl. 12":"No_number", 
            "nr.130":"130",
            "1A (fost 14)":"1A",
            "Camin 4":"No_number",
            "86     Bl 86A":"86",
            "nr. 12":"12",
            "km9+100":"No_number",
            "Scara C":"No_number",
            "Bl 303":"No_number",
            "a1 Et4 Sc.a":"A1",
            "Padurea Baneasa":"No_number",
            "5 ,bl.C 72":"5",
            "Bl. C3":"No_number", 
            "Bl. C2":"No_number", 
            "Bl. C1":"No_number",                       
            "fn":"No_number",
            "BL.P 20":"No_number",
            "Bl.1":"No_number",  
            "Bl. A5":"No_number"           
     }


remove_whitespaces = re.compile(r'\s+')   #regular expression to remove whitespaces

def update_number(number, mapping_housenumber):
    number=number.encode('utf-8')
    for key,value in mapping_housenumber.items(): #update housenumbers with values from mapping
        if number==key:
            number=value
    number=re.sub(remove_whitespaces, '',number)  #remove whitespaces and convert the housenumber to uppercases
    number=str.upper(number)
    return  number

print '----CLEAN HOUSENUMBERS-----'
for number in  audit_house_number(mapXML):
    better_number = update_number(number, mapping_housenumber)
    print number, "=>", better_number    