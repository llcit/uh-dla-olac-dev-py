# dlasite/forms.py
from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib import messages

import json

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from olacharvests.olac import OLACClient
from olacharvests.models import Repository, Collection, Record, MetadataElement

from .utils import OLACUtil

class CreateRepositoryForm(ModelForm):

    def clean(self):
        cleaned_data = super(CreateRepositoryForm, self).clean()
        try:
            self.olac_client = OLACUtil(cleaned_data.get('base_url'))
            self.repo_data = self.olac_client.get_repository()
            self.record_list = self.olac_client.get_record_list()         
        except:
            raise ValidationError('Repository base url is invalid.')

        return cleaned_data

    def save(self):
        # Create the repository
        try: 
            repository = super(CreateRepositoryForm, self).save(commit=False)
            repository.base_url = self.cleaned_data.get('base_url')     
            repository.save()
        except:
            print 'Exception'

        for i in self.repo_data:
            if i.fieldname == 'name':
                repository.name = i.data
                repository.save()
            
            repository.set_info_item(i)

        # Add the records 
        
        for i in self.record_list:
            # Create a collection on the fly
            try:
                collection = Collection.objects.get(identifier=i.header['setSpec'])
            except:
                collection = Collection(identifier=i.header['setSpec'])
                collection.save()

            record = Record(
                identifier = i.header['identifier'],
                datestamp = i.header['datestamp'],
                set_spec = collection
                )

            record.save()
            
            print 'Storing metadata....'
            for j in i.metadata:
                record.set_metadata_item(j)

        return repository

    class Meta:
        model = Repository
        fields = ['base_url']


# class CreateCommunityForm(ModelForm):

#     def __init__(self, *args, **kwargs):
#         try:
#             repo = kwargs.pop('repo')
#             communities = kwargs.pop('community_list')
#         except:
#             pass

#         super(CreateCommunityForm, self).__init__(*args, **kwargs)

#         self.fields['identifier'] = forms.CharField(
#             widget=forms.Select(choices=communities))
#         self.fields['identifier'].label = 'Select Community Collection From ' + \
#             repo.name + ':'
#         self.fields['repository'].initial = repo
#         self.fields['repository'].empty_label = None
#         self.fields['repository'].label = repo.name

#     class Meta:
#         model = Community
#         fields = ['identifier', 'name', 'repository']
#         widgets = {'name':
#                    forms.HiddenInput(), 'repository': forms.HiddenInput()}


# class CreateCollectionForm(ModelForm):

#     def __init__(self, *args, **kwargs):

#         try:
#             community = kwargs.pop('community')
#             collections = kwargs.pop('collections_list')
#         except:
#             pass

#         super(CreateCollectionForm, self).__init__(*args, **kwargs)

#         self.fields['identifier'] = forms.CharField(
#             widget=forms.Select(choices=collections))
#         self.fields['identifier'].label = 'Select Collection From ' + \
#             community.name + ':'
#         self.fields['community'].initial = community
#         self.fields['community'].label = community.name

#     class Meta:
#         model = Collection
#         fields = ['identifier', 'name', 'community']
#         widgets = {'name':
#                    forms.HiddenInput(), 'community': forms.HiddenInput()}
