# dlasite/forms.py
from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib import messages

import json

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from olacharvests.olac import OLACClient
from olacharvests.models import Repository, Collection, Record, MetadataElement

class CreateRepositoryForm(ModelForm):

    def clean(self):
        cleaned_data = super(CreateRepositoryForm, self).clean()
        try:

            client = OLACClient(cleaned_data.get('base_url'))    
            repository_info = client.identify()
            info = []
            for i in repository_info:
                if i.fieldname == 'name':
                    cleaned_data['name'] = i.data
                
                d = {}
                d[i.fieldname] = i.data
                info.append(d)

            cleaned_data['info'] = json.dumps(info)
            
        except:
            raise ValidationError('Repository base url is invalid.')

        return cleaned_data

    def save(self):
        repository = super(CreateRepositoryForm, self).save(commit=False)
        repository.name = self.cleaned_data.get('name')
        repository.base_url = self.cleaned_data.get('base_url')
        repository.info_list = self.cleaned_data.get('info')
        
        # repository.archive_url = self.cleaned_data.get('archive_url')
        # repository.participants = list(self.cleaned_data.get('participant'))
        # repository.institution = self.cleaned_data.get('institution')
        # repository.institution_url = self.cleaned_data.get('institution_url')
        # repository.short_location = self.cleaned_data.get('short_location')
        # repository.location = self.cleaned_data.get('location')
        # repository.synopsis = self.cleaned_data.get('synopsis')
        # repository.access = self.cleaned_data.get('access')
        # repository.submission_policy = self.cleaned_data.get('submission_policy')
        repository.save()
        
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
