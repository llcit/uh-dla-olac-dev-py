# mixins.py
from olacharvests.models import Repository, MetadataElement
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



class RepositoryInfoMixin(object):
    """
    Simply populates a template variable with the one and only Repository object. 
    """

    def get_context_data(self, **kwargs):
        context = super(RepositoryInfoMixin, self).get_context_data(**kwargs)
        context['repository'] = Repository.objects.all()[0]
        return context

class MapCollectionDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MapCollectionDataMixin, self).get_context_data(**kwargs)
        return context

class MapDataMixin(object):
    """
    Populates additional lists for google map display and browsing.
    May not require a queryset of Record objects. TODO: need to check this for dynamic list building.
    """

    def get_context_data(self, **kwargs):
        context = super(MapDataMixin, self).get_context_data(**kwargs)
        repo_cache = RepositoryCache.objects.get()
        context['mapped_plots']= unicode(repo_cache.mapped_data_list)
        context['mapped_collections'] = json.loads(repo_cache.mapped_collection_data_list)
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