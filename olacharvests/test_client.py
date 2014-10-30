# test_client.py
from olac import OLACClient
from lxml import etree
import json


xmlfile =  'http://localhost:8000/static/test/Kaipuleohone.xml'  
# 'sample-olac-static-repo.xml' 'sample-olac-kaipuleohone.xml' 
# 'http://scholarspace.manoa.hawaii.edu/Kaipuleohone.xml'
# 'http://localhost:8000/static/test/Kaipuleohone.xml'

client = OLACClient(xmlfile)
x = client.identify()
y = []

for i in x:
	d = {}
	d[i.fieldname] = i.data
	y.append(d)

for i in y:
	print i






# r = client.list_records()
# records = client.list_records()
# for i in records:
#     client.tostring(i)
