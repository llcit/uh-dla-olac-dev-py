# olac_util.py
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from collections import Counter, namedtuple
import json

from olacharvests.models import Repository, Collection, Record, MetadataElement, Plot
from olacharvests.olac import OLACClient, OlacMetadataItem

from .models import RepositoryCache

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

    def update_repository_cache(self):
        # metadata = MetadataElement.objects.all()
        # languages = metadata.filter(element_type='subject.language')
        # language_freq = Counter()
        # language_freq.update([x.element_data for x in languages])
        repo_cache = RepositoryCache.objects.all()[0]
        site = DlaSiteUtil()
        repo_cache.mapped_data_list = site.make_map_plots(Record.objects.all())
        repo_cache.mapped_collection_data_list = json.dumps(
            site.make_map_plot_collections()
            )
        repo_cache.save()

        pass

    def update_record_metadata(self, record, node):
        # Clear existing metadata for this record.
        record.data.all().delete()

        # Replenish metadata element data for the record from xml harvest
        # NOTE: reads off olac.OlacMetadataItem namedtuples
        for m in node.metadata:
            record.set_metadata_item(m)

        return

    def harvest_records(self):
        index = 0
        length = 0
        if self.client:
            records = self.get_record_list()
            length = len(records)
            
            for node in records:
                # DEBUGGING -> print '%s/%s' % (index+1, length)

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

                    datestr = unicode(node.header['datestamp'])
                    # if record.make_update(datestr):
                    record.datestamp = datestr
                    record.set_spec = collection
                    record.save()
                    self.update_record_metadata(record, node)
                    index = index + 1

                except Record.DoesNotExist:
                    record = Record(identifier=node.header['identifier'])
                    record.datestamp = unicode(node.header['datestamp'])
                    record.set_spec = collection
                    record.save()
                    self.update_record_metadata(record, node)
                    print 'new record added!'
                    index = index + 1
                
                except KeyError:
                    raise KeyError(str( ('Record node [%s] does not have an identifier key. Please validate xml at %s')% (
                        index, self.client.root)))
    

        else:
            raise Exception('Please instantiate a OLACUtil client first.')
        
        return '%s/%s records updated.' % (index, length)

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

class DlaSiteUtil(object):
    def __init__(self):
        pass

    def make_map_lists(self, queryset):
        mapped_plots = set()
        mapped_languages = set()
        mapped_records = []
        mapped_collections = []

        for record in queryset: 
            mapped_data = [json.loads(i.element_data) for i in record.get_metadata_item('spatial')]
            
            [ mapped_plots.add(Plot(i['east'], i['north'])) for i in mapped_data ]    
            mapped_languages |= set([i.element_data for i in record.get_metadata_item('subject.language')])   
            
            mapped_records.append(record.as_dict())
                    
        mapped_plots = self.make_json_map_plots(mapped_plots)

        maplists = {}
        maplists['mapped_records'] = sorted(mapped_records)
        maplists['mapped_languages'] = sorted(mapped_languages)
        maplists['mapped_plots']= mapped_plots

        return maplists

    def make_map_plots(self, queryset):
        mapped_plots = set()
        for record in queryset: 
            mapped_plots.add(record.get_map_plot())

        return self.make_json_map_plots(list(mapped_plots))

    def make_map_plot_collections(self):
        """
        Returns a tuple ([name, site url, [languages] ], [Plots])
        """
        mapped_collections = [i for i in Collection.objects.all() if i.list_map_plots()]

        # Very elaborate list comprehension...
        mapped_collections = [
            {
                'name':        unicode(i), 
                'site_url':     i.get_absolute_url(), 
                'languages':    i.list_languages(),
                'map_plots':    [j._asdict() for j in i.list_map_plots()]
            }         
            for i in mapped_collections
        ]
        return mapped_collections


    def make_json_map_plots(self, plots):
        """
        Create a dictionary for each in the Plot list then encode as json string.
        """
        try:
            plots = [ plot._asdict() for plot in plots ]
            return json.dumps( plots ) # jsonify for google maps js client (DOM).
        except:
            return []



        
