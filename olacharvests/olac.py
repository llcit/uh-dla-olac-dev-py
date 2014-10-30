# OLACClient.py
from lxml import etree
from collections import namedtuple
import codecs
import json
import urllib2

OlacRecord = namedtuple('OlacRecord', ['header', 'metadata'])
OlacMetadataItem = namedtuple('OlacMetadataItem', 'fieldname data')

olac_archive_reader = {
    'name': '//repository:repositoryName',
    'base_url': '//repository:baseURL',
    'archive_url': '//olac-archive:archiveURL',
    'participant': '//olac-archive:participant',
    'institution': '//olac-archive:institution',
    'institution_url': '//olac-archive:institutionURL',
    'short_location': '//olac-archive:shortLocation',
    'location': '//olac-archive:location',
    'synopsis': '//olac-archive:synopsis',
    'access': '//olac-archive:access',
    'submission_policy': '//olac-archive:archivalSubmissionPolicy',
    'current_as_of': '//olac-archive:olac-archive'
}

olac_dc_reader = {
    'identifier': './/dc:identifier',
    'title': './/dc:title',
    'date': './/dc:date',
    'contributor': './/dc:contributor',
    'tableOfContents': './/dcterms:tableOfContents',
    'description': './/dc:description',
    'language': './/dc:language',
    'spatial': './/dcterms:spatial',
    'bibliographicCitation': './/dcterms:bibliographicCitation',
    'coverage': './/dc:coverage',
    'subject': './/dc:subject',
    'content': './/dc:content',
    'format': './/dc:format',
    'type': './/dc:type',
}

meta_type_map = {
    'olac:discourse-type': 'discourse-type',
    'olac:language': 'language',
    'olac:linguistic-field': 'linguistic-field',
    'olac:linguistic-type': 'linguistic-type',
    'olac:role': 'role',
    'dcterms:DCMIType': 'dcmi',
    'dcterms:URI': 'uri',
    'dcterms:ISO3166': 'iso'
}

namespaces = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'olac': 'http://www.language-archives.org/OLAC/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'repository': 'http://www.openarchives.org/OAI/2.0/static-repository',
    'olac-archive': 'http://www.language-archives.org/OLAC/1.1/olac-archive',
    'oai-identifier': 'http://www.openarchives.org/OAI/2.0/oai-identifier',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}


class OLACClient(object):

    """
    A loose implementation of client OAI protocol.
    Designed to parse and load an OLAC 'static repository' xml document.
    E.g., http://www.language-archives.org/OLAC/1.1/static-repository.xml
    """

    def __init__(self, xmlfilepath):
        """
        xmlfilepath: a local file or url of an OLAC static repository.
        """
        self.root = self.build_tree_root(xmlfilepath)

    def identify(self):
        evaluator = etree.XPathEvaluator(self.root, namespaces=namespaces)

        repository_info = [] # list of metadatitem named tuples
        for fieldname, xpath in olac_archive_reader.items():
            for node in evaluator(xpath):
                if fieldname == 'participant':
                    data = '%s (%s) %s'% (node.get('name'), node.get('role'), node.get('email'))
                elif fieldname == 'current_as_of':
                    data = node.get('currentAsOf')
                else:
                    data = node.text

                repository_info.append(OlacMetadataItem(fieldname, data))
        
        return repository_info

    def list_metatdata_formats(self):
        evaluator = etree.XPathEvaluator(self.root, namespaces=namespaces)
        listmetadataformats = evaluator('//repository:ListMetadataFormats')
        return listmetadataformats

    def list_records(self):
        evaluator = etree.XPathEvaluator(self.root, namespaces=namespaces)
        records = evaluator('//oai:record')

        record_list = []
        for record_node in records:
            # create evaluator from single record
            record_evaluator = etree.XPathEvaluator(
                record_node, namespaces=namespaces)
            
            header = self.build_header(
                record_evaluator('./oai:header')[0])  # get the header node
            
            # metadata items are nested in <olac> so we can use the // for direct access.
            metadata = self.build_metadata(record_evaluator('.//olac:olac')[0])
            record_list.append(OlacRecord(header, metadata))

        return record_list

    def build_tree_root(self, xmlfilepath):
        # with codecs.open(xmlfilepath, 'r', 'utf-8') as xmlfile:
        #     text = xmlfile.read()

        request = urllib2.Request(xmlfilepath)
        response = urllib2.urlopen(request)
        text = response.read()
        
        xml = text.encode('ascii', 'replace')
        xml = unicode(xml, 'UTF-8', 'replace')
        xml = xml.replace(chr(12), '?')
        xml = xml.encode('UTF-8')
        return etree.XML(xml)

    def build_header(self, element):
        hdr_evaluator = etree.XPathEvaluator(element, namespaces=namespaces)
        identifier = hdr_evaluator('.//oai:identifier')
        datestamp = hdr_evaluator('.//oai:datestamp')
        setspec = hdr_evaluator('.//oai:setSpec')

        header = {}
        try:
            header[self.strip_namespace_string(identifier[0].tag)] = identifier[
                0].text
            header[self.strip_namespace_string(datestamp[0].tag)] = datestamp[
                0].text
            header[self.strip_namespace_string(setspec[0].tag)] = setspec[
                0].text
        except:
            pass

        return header

    def build_metadata(self, element):
        print '\n-------------------------------\n'
        meta_evaluator = etree.XPathEvaluator(
            element, namespaces=namespaces)  # Get the metadata tree
        metadata = []
        for fieldname, xpath in olac_dc_reader.items():
            # Process each metadata child element matching xpath
            for e in meta_evaluator(xpath):
                metadata.append(self.build_olac_metadata(e))

        return metadata

    def build_olac_metadata(self, element):
        tag = self.strip_namespace_string(element.tag)
        text = element.text

        dctype = element.get(
            '{http://www.w3.org/2001/XMLSchema-instance}type') or ''
        olaccode = element.get(
            '{http://www.language-archives.org/OLAC/1.1/}code') or ''
        # attributes = {}
        # for key, value in element.attrib.items():
        #     attributes[self.strip_namespace_string(key)] = value

        try:
            tag = '%s.%s' % (tag, meta_type_map[dctype])
            # Add code as value for element or append to tag when node text exists.
            # Not sure if this is standard but if text does not exist, the
            # element will have no value.
            if not text:
                text = olaccode
            else:
                tag = '%s.%s' % (tag, olaccode)
        except:
            pass

        return OlacMetadataItem(tag, text)

    def tostring(self, record):
        print '\n-------HEADER-------'
        for i, j in record.header.items():
            print '%s --> %s' % (i, j)
        print '-------METADATA-------'
        for item in record.metadata:
            print '%s:\t%s' % (item.fieldname, item.data)
        return None

    def strip_namespace_string(self, ns_str):
        s = ns_str
        try:
            if s[0] == '{':
                ns_str = s[1:].split('}')[1]
        except:
            pass

        return ns_str

# metadata dictionary sample:
# {tag: (text, attrib)}
