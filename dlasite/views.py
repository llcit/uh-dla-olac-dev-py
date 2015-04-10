from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q, Count
from collections import Counter, namedtuple
import datetime, json, operator

from haystack.query import SearchQuerySet

from olacharvests.models import Repository, Collection, Record, MetadataElement, ArchiveMetadataElement
from .mixins import RecordSearchMixin, MapDataMixin, RepositoryInfoMixin
from .models import RepositoryCache
from .forms import CreateRepositoryForm, HarvestRepositoryForm, CollectionsUpdateForm


class HomeView(MapDataMixin, RepositoryInfoMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Map mixin needs queryset variable set.

        context = super(HomeView, self).get_context_data(**kwargs)
        repo_cache = RepositoryCache.objects.all()[0]

        # languages = json.loads(repo_cache.language_list)
        # context['languages'] = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)

        # Create language list using haystack.
        langs = SearchQuerySet().filter(e_type='subject.language').facet('e_data')
        context['languages'] = langs.facet_counts()['fields']['e_data']


        # contributors = json.loads(repo_cache.contributor_list)
        # context['contributors'] = sorted(contributors.items(), key=operator.itemgetter(1), reverse=True)

        contribs = SearchQuerySet().filter(e_type__contains='contributor').facet('e_data')
        context['contributors'] = contribs.facet_counts()['fields']['e_data']


        # Create collections list
        collections = [(i, i.count_records()) for i in Collection.objects.all()]
        context['collections'] = sorted(collections, key=operator.itemgetter(1), reverse=True)
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

        self.queryset = SearchQuerySet().filter(collection=curr_collection.name)

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
        for i in self.queryset:
            r = {}
            r['page'] = len(pager)+1
            r['title'] = i.object.get_title()
            r['url'] = i.object.get_absolute_url()
            r['languages'] = i.object.list_subject_languages_as_tuples()
            r['description'] = i.object.get_metadata_item('description')[0].element_data
            records.append(r)
            page = page + 1
            if page % 10 == 0:
                pager.append(len(pager)+1)

        if page % 10 > 0:
            pager.append(len(pager)+1)

        context['collection_info'] = collection_dict
        context['records'] = records
        context['pager'] = pager
        context['collection_languages'] = collection_languages
        context['size'] = self.queryset.count()
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
        context['item_data'] = self.get_object().as_dict()
        return context


class LanguageView(MapDataMixin, RepositoryInfoMixin, ListView):
    model = Record
    template_name = 'item_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(LanguageView, self).get_context_data(**kwargs)
        query = self.kwargs['query']

        self.queryset = SearchQuerySet().filter(e_type='language.language').filter(e_data=query)

        context['records'] = self.queryset
        context['size'] = self.queryset.count()
        context['object'] = query + ' language'
        return context


class ContributorView(MapDataMixin, RepositoryInfoMixin, ListView):
    model = Record
    template_name = 'item_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorView, self).get_context_data(**kwargs)
        query = self.kwargs['query']
        self.queryset = SearchQuerySet().filter(e_data=query)

        context['records'] = self.queryset
        context['size'] = self.queryset.count()
        context['object'] = query
        return context


class SearchView(RepositoryInfoMixin, ListView):
    pass
#     template_name = 'search.html'

#     def post(self, request, *args, **kwargs):
#         # arrays to hold values
#         self.items = []

#         # Grab POST values from the search query
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







