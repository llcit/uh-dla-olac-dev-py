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
            olac_client = OLACUtil(cleaned_data.get('base_url'))
            repo_meta = olac_client.get_repository()
            repo_name = [x for x in repo_meta if x.fieldname == 'name']
            cleaned_data['repo_name'] = repo_name[0].data
            cleaned_data['repo_meta'] = repo_meta
        except:
            raise ValidationError('Repository base url is invalid.')

        return cleaned_data

    def save(self):
        # Create the repository and assign the metadatarchive elements
        repository = super(CreateRepositoryForm, self).save(commit=False)
        repository.name = self.cleaned_data['repo_name']
        repository.save()

        for i in self.cleaned_data['repo_meta']:
            repository.set_info_item(i)

        return repository

    class Meta:
        model = Repository
        fields = ['base_url']


class HarvestRepositoryForm(ModelForm):

    def clean(self):
        cleaned_data = super(HarvestRepositoryForm, self).clean()
        try:
            olac_client = OLACUtil(cleaned_data.get('base_url'))
            olac_client.harvest_records()
        except ValidationError:
            raise ValidationError(str( ('Repository at %s is invalid.')% cleaned_data.get('base_url') ))

        return cleaned_data

    class Meta:
        model = Repository
        fields = ['base_url', 'last_harvest']
        widgets = {
            'base_url': forms.HiddenInput(), 'last_harvest': forms.HiddenInput()}
