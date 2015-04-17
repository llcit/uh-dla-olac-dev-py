# mixins.py
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from olacharvests.models import Collection, Repository, MetadataElement, Plot
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
        context = super(
            MapCollectionDataMixin, self).get_context_data(**kwargs)
        return context


class MapDataMixin(object):

    """
    Populates up to two lists for google map display and browsing.

    mapped_collections: is used primarily in the context of home where all collections are mapped and filtered.
        Contains 0 or more:
        collection id (key), collection name, collection url, and list of plots associated with the collection

    mapped_plots: is a json list ultimately used by map js code to plot coordinates on displayed google map.
        Contains a json representation of the Plot namedtuple:
        E.g., {'east': val, 'north': val}
    """

    def get_context_data(self, **kwargs):
        context = super(MapDataMixin, self).get_context_data(**kwargs)

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
                context['mapped_plots'] = unicode(json.dumps(plot))
        elif obj_type == 'collection':
            plots = [p._asdict() for p in obj.list_map_plots()]
            context['mapped_plots'] = unicode(json.dumps(plots))
        else:
            context['mapped_plots'] = []
            plot_list = []
            plotted_collections = MetadataElement.objects.filter(element_type='spatial').values(
                'record__set_spec', 'element_data', 'record__set_spec__name').annotate(
                collection_locations=Count('record__set_spec'))
            colls = {}
            for collection in plotted_collections:
                coll_key = collection['record__set_spec']
                coll_nam = collection['record__set_spec__name']
                coll_plot = collection['element_data']

                try:
                    colls[coll_key]
                except:  # create the dict key
                    colls[coll_key] = {}
                    colls[coll_key]['plots'] = []

                js = json.loads(coll_plot)
                plot = Plot(js['east'], js['north'])
                plot_list.append(plot._asdict())
                colls[coll_key]['plots'].append(plot)

                try:
                    colls[coll_key]['name']
                except:
                    colls[coll_key]['name'] = coll_nam

                try:
                    colls[coll_key]['url'] = Collection.objects.get(
                        pk=coll_key).get_absolute_url()
                except:
                    colls[coll_key]['url'] = ''

            context['mapped_plots'] = unicode(json.dumps(plot_list))
            context['mapped_collections'] = colls
        return context

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
"""


class RecordSearchMixin(object):

    def get_queryset(self):
        queryset = super(RecordSearchMixin, self).get_queryset()
        queryset = []
        key = self.request.GET.get('key')
        filteropt = self.request.GET.get('filteropts')

        if key:
            q = MetadataElement.objects.filter(
                element_type=filteropt).filter(element_data__icontains=key)
            for i in q:
                queryset.append(i.record)
            return queryset

        return None
