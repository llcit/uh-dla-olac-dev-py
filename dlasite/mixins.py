# mixins.py
from olacharvests.models import MetadataElement
from .utils import DlaSiteUtil
from .models import RepositoryCache
import json

"""NOTE TO self
List comprehensions are great:
Count all the languages in the metadata:
tally = Counter()
tally.update(i.element_data for i in MetadataElement.objects.filter(element_type='subject.language'))

See changes below for examples of list comprehensions.
"""



class MapDataMixin(object):
    """
    Populates additional lists for google map display and browsing.
    Requires a queryset of Record objects. 
    """

    def get_context_data(self, **kwargs):
        context = super(MapDataMixin, self).get_context_data(**kwargs)
        site = DlaSiteUtil()
        # maplists = site.make_map_lists(self.queryset)

        # context['mapped_records'] = maplists['mapped_records']
        # context['mapped_languages'] = maplists['mapped_languages']
        # context['mapped_plots']= maplists['mapped_plots']
        # context['mapped_collections'] = maplists['mapped_collections']
        repo_cache = RepositoryCache.objects.get()
        context['mapped_plots']= repo_cache.mapped_data_list
        context['mapped_collections'] = json.loads(repo_cache.mapped_collection_data_list)
        
        print 'MapDataMixin done.', repo_cache.mapped_collection_data_list
        return context

class RecordSearchMixin(object):

    def get_queryset(self):
        queryset = super(RecordSearchMixin, self).get_queryset()
        queryset = []
        key = self.request.GET.get('key')
        filteropt = self.request.GET.get('filteropts')

        if key:
            q = MetadataElement.objects.filter(element_type=filteropt).filter(element_data__icontains=key)
            for i in q:
                queryset.append(i.record)
            return queryset
        
        return None