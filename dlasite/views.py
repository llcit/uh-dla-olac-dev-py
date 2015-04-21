import datetime
import json
import operator
from collections import Counter, namedtuple

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q, Count
from django.conf import settings

from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm
from haystack.generic_views import SearchView, FacetedSearchView

from olacharvests.models import Repository, Collection, Record, MetadataElement, ArchiveMetadataElement, ISOLanguageNameIndex
from .mixins import RecordSearchMixin, MapDataMixin, RepositoryInfoMixin
from .models import RepositoryCache
from .forms import CreateRepositoryForm, HarvestRepositoryForm, CollectionsUpdateForm


class HomeView(MapDataMixin, RepositoryInfoMixin, SearchView):
    template_name = 'home.html'


    def get_context_data(self, **kwargs):
        # Map mixin needs queryset variable set.

        context = super(HomeView, self).get_context_data(**kwargs)
        # repo_cache = RepositoryCache.objects.all()[0]

        language_codes = MetadataElement.objects.filter(element_type__contains='subject.language').values(
            'element_data').annotate(hits=Count('element_data')).order_by('-hits')
        for i in language_codes:
            i['print_name'] = SearchQuerySet().filter(code=i['element_data'])

        context['languages'] = language_codes

        context['contributors'] = MetadataElement.objects.filter(element_type__contains='contributor').values(
            'element_data').annotate(hits=Count('element_data')).order_by('-hits')

        # Create collections list
        collections = [(i, i.count_records()) for i in Collection.objects.all()]
        context['collections'] = sorted(
            collections, key=operator.itemgetter(1), reverse=True)
        return context


class RepositoryView(RepositoryInfoMixin, DetailView):
    model = Repository
    template_name = 'olac_repository.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        context['info'] = self.get_object().as_dict()
        return context


class RepositoryCreateView(CreateView):
    model = Repository
    template_name = 'olac_repository_manage.html'
    form_class = CreateRepositoryForm

    def get_context_data(self, **kwargs):
        context = super(RepositoryCreateView, self).get_context_data(**kwargs)
        context['existing_repositories'] = Repository.objects.all()
        return context


class RepositoryResetView(TemplateView):
    template_name = 'olac_repository_manage.html'

    def dispatch(self, request, *args, **kwargs):

        MetadataElement.objects.all().delete()
        ArchiveMetadataElement.objects.all().delete()
        Record.objects.all().delete()
        Collection.objects.all().delete()
        RepositoryCache.objects.all().delete()
        Repository.objects.all().delete()

        return redirect('add_repository')


class RepositoryHarvestUpdateView(RepositoryInfoMixin, UpdateView):
    model = Repository
    template_name = 'olac_harvest.html'
    form_class = HarvestRepositoryForm

    def get_initial(self):
        """
        The form performs the harvest.
        The harvest date is initialized here to current day.
        """
        initial = self.initial.copy()
        initial['last_harvest'] = datetime.date.today()
        return initial


class CollectionListView(RepositoryInfoMixin, ListView):
    model = Collection
    template_name = 'collection_list.html'


class CollectionView(MapDataMixin, RepositoryInfoMixin, DetailView):
    model = Collection
    context_object_name = 'collection_obj'
    template_name = 'collection_view.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        curr_collection = self.get_object()
        records_queryset = curr_collection.record_set.all()

        """ Building collection and record presentation data here rather than in template."""
        collection_dict = curr_collection.as_dict()
        for k, v in collection_dict.items():
            try:
                collection_dict[k] = ', '.join(v)
            except:
                collection_dict[k] = v[0]
                pass
        collection_languages = curr_collection.list_subject_languages_as_tuples()
        records = []
        page = 0
        pager = []
        for record in records_queryset:
            data = record.data  # using related manager (related_name)
            r = {}  # custom dictionary for the template
            r['page'] = len(pager) + 1

            r['title'] = data.filter(element_type='title').get().element_data   # i.object.get_title()
            r['url'] = record.get_absolute_url()
            r['languages'] = record.list_subject_languages_as_tuples()
            r['description'] = [j.element_data for j in data.filter(element_type='description')]   # i.object.get_metadata_item('description')[0].element_data
            records.append(r)
            page = page + 1
            if page % 10 == 0:
                pager.append(len(pager) + 1)

        if page % 10 > 0:
            pager.append(len(pager) + 1)

        context['collection_info'] = collection_dict
        context['records'] = records
        context['pager'] = pager
        context['collection_languages'] = collection_languages
        context['size'] = records_queryset.count()
        return context


class CollectionsUpdateView(RepositoryInfoMixin, UpdateView):
    model = Repository
    template_name = 'collection_update.html'
    form_class = CollectionsUpdateForm
    success_url = reverse_lazy('collection_list')

    def get_object(self, queryset=None):
        try:
            return Repository.objects.all().get()
        except Repository.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CollectionsUpdateView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.all()
        return context


class ItemView(MapDataMixin, RepositoryInfoMixin, DetailView):
    model = Record
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)

        d = self.get_object().set_spec.as_dict()
        for k, v in d.items():
            try:
                d[k] = ', '.join(v)
            except:
                d[k] = v[0]
                pass

        context['collection_info'] = d

        item_info = self.get_object().as_dict()

        for i, v in enumerate(item_info['tableOfContents']):
            filename = item_info['tableOfContents'][i]
            rooturl = item_info['identifier_uri_'][0].replace('hdl.handle.net', settings.BITSTREAM_ROOT)
            item_info['tableOfContents'][i] = '<a href="' + rooturl + '/' + filename + '">' + filename + '</a>'

        context['item_data'] = item_info
        return context


class LanguageView(MapDataMixin, RepositoryInfoMixin, ListView):
    model = Record
    template_name = 'item_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(LanguageView, self).get_context_data(**kwargs)
        query = self.kwargs['query']

        try:
            self.queryset = SearchQuerySet().filter(
                e_type='subject.language').filter(e_data=query).facet('e_type')
        except Exception as e:
            print e

        language_name = ISOLanguageNameIndex.objects.filter(code=query)
        if language_name:
            language_name = language_name[0].print_name

        records = []
        collection_filters = set()
        page = 0
        pager = []
        """ Building presentation data here rather than in template. Iterating over MetadataElement in search results."""
        for i in self.queryset:
            r = {}
            r['page'] = len(pager) + 1
            r['element_type'] = i.e_type
            r['collection'] = i.coll
            collection_filters.add(r['collection'])
            r['title'] = i.object.record.get_title()
            r['url'] = i.object.record.get_absolute_url()
            r['languages'] = i.object.record.list_subject_languages_as_tuples()
            r['description'] = i.object.record.get_metadata_item(
                'description')[0].element_data
            records.append(r)
            page = page + 1
            if page % 10 == 0:
                pager.append(len(pager) + 1)

        if page % 10 > 0:
            pager.append(len(pager) + 1)

        context['records'] = records
        context['pager'] = pager
        context['collection_filters'] = list(collection_filters)
        context['size'] = self.queryset.count()
        context['facets'] = self.queryset.facet_counts()['fields']['e_type']
        context['page_title'] = language_name + ' (' + query + ') ' + ' language'
        return context


class ContributorView(MapDataMixin, RepositoryInfoMixin, ListView):
    model = Record
    template_name = 'item_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorView, self).get_context_data(**kwargs)
        query = self.kwargs['query']
        query = query.replace('-', ' ')  # unslugify
        self.queryset = SearchQuerySet().filter(e_type__startswith='contributor').filter(e_data=query).facet('e_type')

        records = []
        page = 0
        pager = []
        """ Building presentation data here rather than in template. Iterating over MetadataElement in search results."""
        for i in self.queryset:
            r = {}
            r['page'] = len(pager) + 1
            r['element_type'] = i.e_type

            r['title'] = i.object.record.get_title()
            r['url'] = i.object.record.get_absolute_url()
            r['languages'] = i.object.record.list_subject_languages_as_tuples()
            r['description'] = i.object.record.get_metadata_item(
                'description')[0].element_data
            records.append(r)
            page = page + 1
            if page % 10 == 0:
                pager.append(len(pager) + 1)

        if page % 10 > 0:
            pager.append(len(pager) + 1)

        context['records'] = records
        context['pager'] = pager
        context['size'] = self.queryset.count()
        context['facets'] = self.queryset.facet_counts()['fields']['e_type']
        context['page_title'] = query
        return context

# FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=SearchQuerySet().facet('e_type'))
sqs = SearchQuerySet().facet('collection').facet('record').facet('e_type')

class SearchHaystackView(FacetedSearchView):
    template_name = 'search/search.html'
    # form_class = FacetedSearchForm
    # queryset = sqs
    # results = None

    # def get_queryset(self):
    #     queryset = super(SearchHaystackView, self).get_queryset()

    #     self.results = queryset
    #     print 'FACETS:', queryset.facet_counts()['fields']['collection']
    #     return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchHaystackView, self).get_context_data(*args, **kwargs)
    #     print 'CONTEXT:', context['object_list']
    #     return context



class SearchView(RepositoryInfoMixin, ListView):
    pass
#     template_name = 'search.html'

#     def post(self, request, *args, **kwargs):
# arrays to hold values
#         self.items = []

# Grab POST values from the search query
#         self.query = self.request.POST.get('query')
#         self.key = self.request.POST.get('key')

#         self.queryset = MetadataElement.objects.filter(
#             element_type=self.query).filter(element_data__icontains=self.key)

#         for element in MetadataElement.objects.filter(element_type=self.query).filter(element_data__icontains=self.key):
#             self.items.append(element.record)

#         return super(SearchView, self).get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(SearchView, self).get_context_data(**kwargs)
#         context['items'] = self.items
#         context['len'] = len(self.items)
#         context['query'] = self.query
#         context['key'] = self.key
#         return context


class SearchPage(RecordSearchMixin, ListView):
    pass
#     model = Record
#     template_name = 'searchtest.html'
