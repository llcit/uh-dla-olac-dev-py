# olac_test.py
# from .olac import OLACClient
# from .models import *
from lxml import etree
# import urllib2

# xmlfilepath = 'http://localhost:8000/static/test/sample.xml'
#xmlfilepath = 'http://www.language-archives.org/OLAC/1.1/static-repository.xml'
xmlfilepath = 'http://scholarspace.manoa.hawaii.edu/Kaipuleohone.xml' # sample-olac-static-repo.xml

mprefix = 'olac'
namespaces = {
	'oai': 'http://www.openarchives.org/OAI/2.0/', 
	'olac': 'http://www.language-archives.org/OLAC/1.1/',
	'dcterms': 'http://purl.org/dc/terms/',
	'dc': 'http://purl.org/dc/elements/1.1/',
	'repository': 'http://www.openarchives.org/OAI/2.0/static-repository',
	'olac-archive': 'http://www.language-archives.org/OLAC/1.1/olac-archive',
    'oai-identifier': 'http://www.openarchives.org/OAI/2.0/oai-identifier',
	}

print 'xmlfilepath --> ', xmlfilepath
print 'mprefix --> ', mprefix
print 'namespaces --> ', namespaces

# The lxml way. Seems to be more robust.
tree = etree.parse(xmlfilepath)
repository = tree.getroot()

		# req = urllib2.Request(xmlfilepath)
		# response = urllib2.urlopen(req)
		# text = response.read()
		# OLD and not robust
		# xml = text.encode('ascii', 'replace')
		# xml = unicode(xml, 'UTF-8', 'replace')   	 
		# xml = xml.replace(chr(12), '?')
		# xml = xml.encode('UTF-8')


		# repository = etree.XML(xml) # Repository root element = 'Repository'
		# evaluator = etree.XPathEvaluator(repository, namespaces=namespaces)
		# identify = evaluator('//repository:Identify')
		# listmetadataformats = evaluator('//repository:ListMetadataFormats')
		# listrecords = evaluator('//repository:ListRecords')



# NOTE: this grabs the record elements from tree:
# records = evaluator('//oai:record')



# print '---------HEADER---------\n'
# r = records[0]
# h = r[0]
# i = 0
# for e in h:
# 	print '%s - %s\n--> %s\n-->%s\n\n'% (i, e.tag, e.text, e.attrib)
# 	i+=1

# print '\n\n---------METADATA SINGLE---------\n'
# r = records[267]
# m = r[1][0]
# for e in m:
# 	print '%s\n--> %s\n-->%s\n\n'% (e.tag, e.text, e.attrib)

# print '\n\n---------METADATA FULL---------\n'
# i = 0
# for r in records:
# 	m = r[1][0]
# 	for e in m:
# 		print '%s - %s --> %s\n----> %s'% (i, e.tag, e.text, e.attrib)
# 	i += 1	




# result = []



# for record_node in records:
# 	record_evaluator = etree.XPathEvaluator(record_node, 
#                                         namespaces=namespaces)
# 	e = record_evaluator.evaluate
# 	# find header node
# 	header_node = e('oai:header')[0]
# 	# create header
# 	header = header_node
# 	# find metadata node
# 	metadata_list = e('oai:metadata')
# 	if metadata_list:
# 	    metadata = metadata_list[0]
# 	    # create metadata
# 	    # metadata = metadata_registry.readMetadata(metadata_prefix, metadata_node)
# 	else:
# 	    metadata = None
# 	# XXX TODO: about, should be third element of tuple
# 	result.append((header, metadata, None))


# etree.tostring(tree, pretty_print=True)

