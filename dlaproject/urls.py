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

urlpatterns = patterns('',

	url(r'^dla/$', HomeView.as_view(), name='home'),
	
	url(r'^dla/repository/info/(?P<slug>[-\w]+)/$',
	   RepositoryView.as_view(), name='olac_repository'),
	
	url(r'^dla/repository/add/$',
	   RepositoryCreateView.as_view(), name='add_repository'),

	url(r'^dla/repository/delete/$',
	   RepositoryResetView.as_view(), name='delete_repository'),
	
	url(r'^dla/repository/harvest/(?P<slug>[-\w]+)/$',
	   RepositoryHarvestUpdateView.as_view(), name='harvest_repository'),

	url(r'^dla/collections/update/$', CollectionsUpdateView.as_view(),
	   name='collections_update'),
	
	
	url(r'^dla/collections/$', CollectionListView.as_view(), name='collection_list'),
	



	url(r'^dla/collection/(?P<slug>[-\w]+)/$',
	   CollectionView.as_view(), name='collection'),
	url(r'^dla/item/(?P<pk>\w+)$',
	   ItemView.as_view(), name='item'),
	url(r'^dla/language/(?P<query>\w+)$',
	   LanguageView.as_view(), name='language'),
	url(r'^dla/dla/contributor/(?P<query>[-\w]+)$',
	   ContributorView.as_view(), name='contributor'),
	url(r'^dla/search/$', SearchView.as_view(), name='search'),
	url(r'^dla/searchtest/$', SearchPage.as_view(),
	   name='searchtest'),


	url(r'^dla/admin/', include(admin.site.urls)),
)
