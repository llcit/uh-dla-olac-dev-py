# olac_util.py
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from collections import Counter, namedtuple
import json

from olacharvests.models import Repository, Collection, Record, MetadataElement
from olacharvests.olac import OLACClient, OlacMetadataItem

from .models import RepositoryCache

"""

from collections import *
from dlasite.models import *
from olacharvests.models import *
metadata = MetadataElement.objects.all()
languages = metadata.filter(element_type='subject.language')
lf = Counter()
lf.update([x.element_data for x in languages])

contributors = metadata.filter(element_type__startswith='contributor.')
cf = Counter()
cf.update([x.element_data for x in contributors])

mapped_data = metadata.filter(element_type='spatial')
points = Counter


from dlasite.utils import OLACUtil
from olacharvests.olac import *
util = OLACUtil('http://localhost:8000/static/test/Kaipuleohone.xml')
repo = util.get_repository()
jrepo = util.get_repository_asdict()
"""


class OLACUtil(object):

    """
    This is a utility class:
    * designed to provide independent procedures for harvesting OLAC repositories.
    * used by django specific views as well as other modules independent of django context.
    * E.g, crontab scripts for automated/scheduled harvests.
    * makes connections to repository base_urls
    * pulls and parses xml (utilizing olac module)
    * writes to db tables
    """

    def __init__(self, xmlfilepath):
        """
        xmlfilepath: a local file or url of an OLAC static repository.
        """

        self.client = OLACClient(xmlfilepath)

    def get_repository(self):
        repository_info = self.client.identify()
        return repository_info

    def get_repository_asdict(self):
        repository_info = self.client.identify()
        info_dict = []
        for i in repository_info:
            d = {}
            d[i.fieldname] = i.data
            info_dict.append(d)
        return info_dict

    def get_record_list(self):
        records_list = self.client.list_records()
        return records_list

    def create_repository(self):
        pass

    def update_repository_cache(self, records):
        # metadata = MetadataElement.objects.all()
        # languages = metadata.filter(element_type='subject.language')
        # language_freq = Counter()
        # language_freq.update([x.element_data for x in languages])

        pass

    def harvest_records(self):
        index = 0
        if self.client:
            records = self.get_record_list()
            length = len(records)
            
            for node in records:
                print '%s/%s' % (index+1, length)

                # Get an existing or create a new collection object
                try:
                    collection = Collection.objects.get(
                        identifier=node.header['setSpec'])
                except Collection.DoesNotExist:
                    collection = Collection(identifier=node.header['setSpec'])
                    collection.save()
                except KeyError:
                    collection = None

                # Get an existing or create a new record object
                try:
                    record = Record.objects.get(
                        identifier=node.header['identifier'])
                except Record.DoesNotExist:
                    record = Record(identifier=node.header['identifier'])
                except KeyError:
                    raise KeyError(str( ('Record node [%s] does not have an identifier key. Please validate xml at %s')% (
                        index, cleaned_data.get('base_url')) ))

                record.datestamp = node.header['datestamp'],
                record.set_spec = collection
                record.save()

                
                # Clear existing metadata for this record.
                record.data.all().delete()

                # Replenish metadata element data for the record from xml harvest
                # NOTE: reads off olac.OlacMetadataItem namedtuples
                for m in node.metadata:

                    if m.fieldname == 'spatial':
                        s = m.data.replace(' ', '').split(';')
                        s = [s[i].split('=') for i in range(len(s))]
                        s = {s[0][0]:s[0][1], s[1][0]:s[1][1]}
                        m = OlacMetadataItem(m.fieldname, json.dumps(s))

                    record.set_metadata_item(m)

                index = index + 1

        else:
            raise Exception('Please instantiate a OLACUtil client first.')
        
        return index

class OAIUtil(object):
    """
    Utility class for accessing data usin OAI-PMH. This is here mainly to 
    enrich information related to Collections. The OLAC static repository scheme 
    implemented at Scholarspace does not provide Collection names but does provide
    Collection identifiers of the form: col_nnnnnnn.
    """
    def __init__(self, request_url):
        """
        request_url: base request url for OAI-PMH repository.
        E.g., https://scholarspace.manoa.hawaii.edu/dspace-oai/request
        """
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            self.client = Client(request_url, registry)
        
        except:
            raise ValidationError(str( ('OAI Repository at %s is invalid.')% cleaned_data.get('request_url') ))
        
    def update_oai_collection_info(self):
        # url = 'https://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        try:
            oai_collections = list(self.client.listSets())
            queryset = Collection.objects.all()
            querylist = [x.identifier for x in queryset]
            for i in oai_collections:
                if i[0] in querylist: 
                    col_obj = queryset.get(identifier=i[0])
                    col_obj.name = i[1]
                    col_obj.save()
                    querylist.remove(i[0])            
                if not querylist:
                    break
        except:
            return None

        return queryset
        
