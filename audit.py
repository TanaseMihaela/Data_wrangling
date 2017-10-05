import os
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
import sys
import codecs
from collections import defaultdict
import os

mapXML='bucharest_romania.osm'     # import Bucharest osm from OpenStreetMap

#AUDIT TAGS

tags={}
def count_tags(filename):
    '''Count tags'''
    for event,element in ET.iterparse(filename):
        if element.tag in tags.keys():
            tags[element.tag]+=1
        else:
            tags[element.tag]=1
    return tags     
count_tags=count_tags(mapXML)
print '-----COUNT TAGS:-----'
if __name__ == "__main__":
    pprint.pprint(count_tags)

#AUDIT USERS
def get_user(element):
    '''Get user uid'''
    if element.get('uid'):
        uid = element.attrib["uid"]
        return uid
    else:
        return None

def users_count(filename):
    '''save unique users in set 'users' '''
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element):
            users.add(get_user(element))
    return len(users)
print '-----COUNT UNIQUE USERS:-----'  
if __name__ == "__main__":
    print users_count(mapXML)

#AUDIT PROBLEMCHARS
# Check the "k" value for each "<tag>" and see if there are any problems
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower_colon.search(element.attrib['k']):
            keys["lower_colon"] += 1
        elif lower.search(element.attrib['k']):
            keys["lower"] += 1
        elif problemchars.search(element.attrib['k']):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    return keys

def process_problems(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys
print '-----COUNT PROBLEMCHARS:-----'  
if __name__ == "__main__":
    print process_problems(mapXML)

#AUDIT STREET TYPE NAMES

def streets_count(file_name):
    '''Count total number of streets; is a street if the tag attribute is "addr:street" '''
    steet_count = 0                                      
    for event, elem in ET.iterparse(file_name, events=("start",)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == "addr:street":     
                    steet_count += 1
    return steet_count
if __name__ == "__main__":
    print 'STRET COUNTS:' streets_count (mapXML)

  


# STREETS TYPES AND COUNTS FOR EACH TYPE
street_type_re=re.compile(r'^\S+\.?',re.IGNORECASE) #regular expression to extract first word before '.'
street_types=defaultdict(int)                       #create dictionary  with default value of int 0                   

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type]+=1
        
def print_sorted_dict(d):                           
    '''sort dictionary by street names'''
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 
        
def is_street_name(elem):                          
    '''find tag with attribute for street       '''
    return (elem.tag=="tag") and (elem.attrib['k'] == "addr:street")
    
def audit_street( ):                                
    '''populate dictionary street_types with street abbreviation as keys and counts as values'''
    for event, elem in ET.iterparse(mapXML):        
        if (elem.tag=="tag") and (elem.attrib['k'] == "addr:street"):
            audit_street_type(street_types, elem.attrib['v'])
    print print_sorted_dict (street_types)

print '----AUDIT STREETS----'
if __name__ == "__main__":
    print audit_street()
    


#AUDIT MOBILE SHOPS (Orange,Vodafone,Telekom)
def is_shop(elem):
    return (elem.attrib['k'] == "shop")    

def is_shop_name(elem):
    return (elem.attrib['k'] == "name")


# TOTAL NUMBER OF MOBILE SHOPS
def mobile_shops_count(filename):
    ''' if value of attribute "shop" is "mobile_phone", return value of attribute "name" saved in variable curr_name '''
    ''' Eg:<tag k="name" v="Germanos Baneasa"/>'''
    '''    <tag k="shop" v="mobile_phone"/> '''
    shops_count = 0
    for event, elem in ET.iterparse(filename, events=("start",)):
        curr_name=None
        curent_shop=None
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_shop_name(tag):
                    curr_name=tag.attrib['v']       
                if is_shop(tag):
                    curr_shop=tag.attrib['v']
                    if curr_shop=='mobile_phone':
                        shops_count += 1
    return shops_count
print '-----TOTAL NUMBERS OF MOBILE SHOPS IN BUCHAREST:-----'
if __name__ == "__main__":
    print mobile_shops_count (mapXML)


def audit_shops(filename):   
    '''create dictionary with mobile shop name as key and count as value'''
    data=defaultdict(int)     
    for event, elem in ET.iterparse(filename, events=("start",)):
        curr_name=None
        curent_shop=None
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_shop_name(tag):
                    curr_name=tag.attrib['v']       
                if is_shop(tag):
                    curr_shop=tag.attrib['v']
                    if curr_shop=='mobile_phone':
                        data[curr_name]+=1             
    return data
print '-----AUDIT MOBILE SHOPS----' 
if __name__ == "__main__":
    print audit_shops(mapXML)   


#AUDIT POSTAL CODES
def audit_zipcode(invalid_zipcodes, zipcode): 
    '''Zip codes should have 5 or 6 digits in Bucharest'''
    '''search for zipcodes which doesn't contain digits and the lenght is not 5 or 6'''
    '''save the results in invalid_zipcodes'''
    if not zipcode.isdigit():                 
        invalid_zipcodes[code].add(zipcode)
    elif len(zipcode)<5 or len(zipcode)>6:
        invalid_zipcodes[code].add(zipcode)

        
def is_zipcode(elem):
    return (elem.attrib['k'] == "postal_code")

def audit_zip(filename):                     
    '''iterate over  xml and find the invalid zipcodes'''
    invalid_zipcodes = defaultdict(set)            
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])

    return invalid_zipcodes
print '-----AUDIT POSTAL CODES-----'
if __name__ == "__main__":
    print audit_zip(mapXML)

#No mistakes in postal code? Let's list them and check manually if they are formatted correctly


data=set()
def list_postal(filename):
    '''List postal codes'''
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    data.add(tag.attrib['v'])
    return sorted(data)
print '-----LIST POSTAL CODES-----'
if __name__ == "__main__":
    print list_postal(mapXML)                    
#All values listed contain 5-6 digits    



#AUDIT STREET NUMBERS
def audit_housenumber(invalid_housenumber, housenumber):
    '''save in invalid_housenumber the housenumber which don't contain only digits'''
    if not (housenumber).isdigit():
        invalid_housenumber.add(housenumber)

def is_housenumber(elem):
    return (elem.attrib['k'] == "addr:housenumber")      

def audit_house_number(filename):                    
    '''list invalid numbers; street numbers are extracted from the  value of attribute "addr:housenumber" '''
    invalid_housenumber = set()                       
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_housenumber(tag):
                    audit_housenumber(invalid_housenumber,tag.attrib['v'])
    return invalid_housenumber
print '-----AUDIT HOUSENUMBERS-----'
if __name__ == "__main__":
    print audit_house_number(mapXML)