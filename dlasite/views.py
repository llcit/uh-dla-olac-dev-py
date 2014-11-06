from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q, Count
from collections import Counter, namedtuple
import datetime, json, operator

from olacharvests.models import Repository, Collection, Record, MetadataElement
from .mixins import RecordSearchMixin, MapDataMixin
from .models import RepositoryCache
from .forms import CreateRepositoryForm, HarvestRepositoryForm

class HomeView(MapDataMixin, TemplateView):
    template_name = 'home.html'
    queryset = None

    def get_context_data(self, **kwargs):
        # mapped_records = []

        # Query and variables for the needed MetadataElments
        metadata = MetadataElement.objects.all()

        # Create dictionary with language frequency counts using Counter
        language_frequencies = Counter()
        for metaelement in metadata.filter(element_type='language'):
            language_frequencies.update(json.loads(metaelement.element_data))

        # Create dictionary with contributor frequency counts using Counter
        contributor_frequencies = Counter()
        for metaelement in metadata.filter(element_type='contributor'):
            contributor_frequencies.update(
                json.loads(metaelement.element_data))

        # mapped_plots = set()    # unique coords in mapped records
        # mapped_languages = set()  # unique languages in mapped records

        self.queryset = Record.objects.filter(data__element_type='coverage')

        # Only retrieve metadata items that have data values set for coverage
        # for metaelement in metadata.filter(element_type='coverage').exclude(element_data=[]):
        # mapped_plots.add( make_map_plot(metaelement.element_data) )
        #     record_dict = metaelement.record.as_dict()

        #     mapped_languages |= set(record_dict['language'])
        #     mapped_records.append(record_dict)

        # mapped_plots=make_json_map_plots(mapped_plots)

        ######################## Preparing context to render in template ######
        context = super(HomeView, self).get_context_data(**kwargs)
        context['collections'] = Collection.objects.all().order_by('name')
        context['languages'] = sorted(
            language_frequencies.iteritems(), key=operator.itemgetter(1), reverse=True)
        context['contributors'] = sorted(
            contributor_frequencies.iteritems(), key=operator.itemgetter(1), reverse=True)
        # context['mapped_records'] = sorted(
        #     mapped_records, key=operator.itemgetter('collection'))
        # context['mapped_plots'] = unicode(mapped_plots)
        # context['mapped_languages'] = sorted(mapped_languages)

        return context

class RepositoryView(DetailView):
    model = Repository
    template_name = 'olac_repository.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        context['info'] = self.get_object().as_dict()
        return context

class RepositoryListManageView(CreateView):
    model = Repository
    template_name = 'olac_repository_manage.html'
    form_class = CreateRepositoryForm

    def get_context_data(self, **kwargs):
        context = super(RepositoryListManageView, self).get_context_data(**kwargs)
        context['existing_repositories'] = Repository.objects.all()
        return context

class RepositoryHarvestUpdateView(UpdateView):
    model = Repository
    template_name = 'olac_harvest.html'
    form_class = HarvestRepositoryForm
    
    def get_initial(self):
        """
        Sets the Repository to update the last_harvest field to current day.
        """
        initial = self.initial.copy()
        initial['last_harvest'] = datetime.date.today()
        return initial


class CollectionListView(ListView):
    model = Collection
    template_name = 'collection_list.html'



class CollectionView(MapDataMixin, DetailView):
    model = Collection
    template_name = 'collection_view.html'
    queryset = None

    def get_context_data(self, **kwargs):
        self.queryset = self.get_object().list_records()
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['items'] = self.queryset
        context['size'] = len(self.queryset)
        return context


class ItemView(DetailView):
    model = Record
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context['item_data'] = self.get_object().as_dict()
        return context


class LanguageView(MapDataMixin, ListView):
    model = Record
    template_name = 'collection_view.html'

    def get_context_data(self, **kwargs):
        query = self.kwargs['query']
        self.queryset = Record.objects.filter(data__element_type='language').filter(
            data__element_data__icontains=query)

        context = super(LanguageView, self).get_context_data(**kwargs)
        context['items'] = self.queryset
        context['size'] = len(self.queryset)
        context['object'] = query + ' language'
        return context


class ContributorView(MapDataMixin, ListView):
    model = Record
    template_name = 'collection_view.html'

    def get_context_data(self, **kwargs):
        query = self.kwargs['query']
        self.queryset = []
        if len(query.split('-')) != 1:
            firstQuery = query.split('-')[0]
            lastQuery = query.split('-')[1]
            q = MetadataElement.objects.filter(element_type='contributor').filter(
                Q(element_data__icontains=firstQuery) & Q(element_data__icontains=lastQuery))

        else:
            q = MetadataElement.objects.filter(
                element_type='contributor').filter(element_data__icontains=query)

        for i in q:
            self.queryset.append(i.record)

        context = super(ContributorView, self).get_context_data(**kwargs)
        context['items'] = self.queryset
        context['size'] = len(self.queryset)
        context['object'] = query
        return context


class SearchView(ListView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        # arrays to hold values
        self.items = []

        # Grab POST values from the search query
        self.query = self.request.POST.get('query')
        self.key = self.request.POST.get('key')

        self.queryset = MetadataElement.objects.filter(
            element_type=self.query).filter(element_data__icontains=self.key)

        for element in MetadataElement.objects.filter(element_type=self.query).filter(element_data__icontains=self.key):
            self.items.append(element.record)

        return super(SearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['items'] = self.items
        context['len'] = len(self.items)
        context['query'] = self.query
        context['key'] = self.key
        return context


class SearchPage(RecordSearchMixin, ListView):
    model = Record
    template_name = 'searchtest.html'







