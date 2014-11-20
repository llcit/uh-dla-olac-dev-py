# mixins.py
from django.contrib.contenttypes.models import ContentType

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
        try:
            context['repository'] = Repository.objects.all()[0]
        except:
            context['repository'] = None
        return context

class MapCollectionDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MapCollectionDataMixin, self).get_context_data(**kwargs)
        return context

class MapDataMixin(object):
    """
    Populates additional lists for google map display and browsing.
    May not require a queryset of Record objects. TODO: need to check this for dynamic list building.
    Requires a selector value.
    A selector string  -- map_cache_selector -- can be one of the following:
        plots: will retrieve RepositoryCache.mapped_data_list (all unique map locations in repository)
        collection_plots: will retrieve RepositoryCache.mapped_collection_data_list (map locations grouped by collection)
    """

    def get_context_data(self, **kwargs):
        context = super(MapDataMixin, self).get_context_data(**kwargs)

        repo_cache = RepositoryCache.objects.get()

        try:
            obj = self.get_object()
            obj_type = ContentType.objects.get_for_model(obj).name
        except:
            obj = None
            obj_type = ''

        if obj_type == 'record':
            plot = obj.get_map_plot()
            if not plot:
                context['mapped_plots'] = []
            else:
                plot = [plot._asdict()]
                context['mapped_plots'] = unicode( json.dumps(plot) )        
        elif obj_type == 'collection':
            plots = [p._asdict() for p in obj.list_map_plots()]
            context['mapped_plots'] = unicode(json.dumps(plots))
        else:
            context['mapped_plots'] = unicode(repo_cache.mapped_data_list)
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