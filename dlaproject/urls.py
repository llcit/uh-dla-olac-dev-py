from django.conf.urls import patterns, include, url
from django.contrib import admin

from dlasite.views import (
    HomeView,
    CollectionListView,
    CollectionView,
    CollectionsUpdateView,
    ItemView,
    LanguageView,
    ContributorView,
    SearchView,
    SearchPage,
    RepositoryView,
    RepositoryCreateView,
    RepositoryResetView,
    RepositoryHarvestUpdateView
)

# Experimenting with faceting
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


sqs = SearchQuerySet().facet('e_type')

urlpatterns = patterns('',
    url(r'^search/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=SearchQuerySet().facet('e_type')), name='haystack_search'),

    # url(r'^search/$', include('haystack.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^repository/info/(?P<slug>[-\w]+)/$', RepositoryView.as_view(), name='olac_repository'),
    url(r'^repository/add/$', RepositoryCreateView.as_view(), name='add_repository'),
    url(r'^repository/delete/$', RepositoryResetView.as_view(), name='delete_repository'),
    url(r'^repository/harvest/(?P<slug>[-\w]+)/$', RepositoryHarvestUpdateView.as_view(), name='harvest_repository'),

    url(r'^collections/update/$', CollectionsUpdateView.as_view(), name='collections_update'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection_list'),
    url(r'^collection/(?P<slug>[-\w]+)/$', CollectionView.as_view(), name='collection'),

    url(r'^item/(?P<pk>\w+)$', ItemView.as_view(), name='item'),

    url(r'^language/(?P<query>\w+)$', LanguageView.as_view(), name='language'),

    url(r'^contributor/(?P<query>[-\w]+)$', ContributorView.as_view(), name='contributor'),

    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^searchtest/$', SearchPage.as_view(), name='searchtest'),

    url(r'^admin/', include(admin.site.urls)),
)
