import json, operator, datetime

from django.db import models
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from collections import OrderedDict
from django.utils.text import slugify
from collections import namedtuple

from haystack.query import SearchQuerySet

""" A namedtuple to handle unique points to plot """
Plot = namedtuple('Plot', ['east', 'north'])

""" A namedtuple to handle language codes and indexed name. """
Language = namedtuple('Language', ['code', 'name'])

class Repository(TimeStampedModel):

    """
    An OLAC static repository. This kind of repository collapses
    the distinction made by OAI repositories. The OLAC concept of
    repository correlates with the OAI Set (Community/Collection).
    The xml root element name is Repository.

    The properties of this class are mostly assigned from the <IDENTIFY>
    element tree.

    See: http://www.language-archives.org/OLAC/1.1/static-repository.xml
    and /docs/sample-olac-static-repo.xml
    """
    name = models.CharField(max_length=512, unique=True, blank=True)
    base_url = models.CharField(max_length=1024, unique=True)
    last_harvest = models.DateField(null=True)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(unicode(self.name))
        else:
            self.slug = slugify(unicode(self.id))
        super(Repository, self).save(*args, **kwargs)

    def list_collections(self):
        return self.collection_set.all()

    def get_info_item(self, info_type):
        return self.archive_data.all(element_type=info_type)

    def set_info_item(self, metadata_element):
        element = ArchiveMetadataElement(
            repository=self,
            element_type=metadata_element.fieldname,
            element_data=metadata_element.data
        )
        element.save()
        return element

    def as_dict(self):
        info = self.archive_data.all().order_by('element_type')
        info_list = []
        for i in info:
            d = {}
            d[i.element_type] = i.element_data
            info_list.append(d)
        return info_list

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('olac_repository', args=[str(self.slug)])


class Collection(TimeStampedModel):

    """
    Models the OAI standard conception of a SET. OLAC does not
    distinguish sets and supersets. Collection instances are populated
    using the OAI-PMH standard (pyoai module needed for this)
    """

    identifier = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    repository = models.ForeignKey(Repository, null=True, blank=True)
    slug = models.SlugField(max_length=512, null=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(unicode(self.name))
        else:
            self.slug = slugify(unicode(self.id))
        super(Collection, self).save(*args, **kwargs)

    def count_records(self):
        return self.record_set.all().count()

    def list_records(self):
        return self.record_set.all()

    def list_map_plots(self):
        """ Returns a list of Plot tuples pruned from records in a collection. """
        plots = set()
        for record in self.list_records():
            p = record.get_map_plot()
            if p:
                plots.add(p)
        return list(plots)

    def list_languages(self):
        """ Returns a list of languages pruned from records in this collection. """
        languages = set()

        for record in self.list_records():
            [languages.add(i) for i in record.list_languages()]

        return list(languages)

    def list_subject_languages_as_tuples(self):
        """ Returns a list of subject.language tuples (code, print_name) pruned from records in this collection."""

        languages = set()
        for record in self.list_records():
            [languages.add(i) for i in record.list_languages()]

        language_list = []
        for i in list(languages):
            for j in SearchQuerySet().filter(code=i):
                language_list.append(Language(j.code, j.print_name))
        return language_list

    def as_dict(self):
        """ Returns a dictionary representation of the collection data as k,v = {type: data list}"""
        collection_dict = {}
        collection_dict['identifier'] = [self.identifier]
        collection_dict['name'] = [self.name]
        collection_dict['repository'] = [self.repository]
        collection_dict['site_url'] = [self.get_absolute_url()]
        collection_dict['num_records'] = [self.count_records()]
        collection_dict['map_plots'] = self.list_map_plots()
        collection_dict['languages'] = self.list_languages()
        return collection_dict

    def __unicode__(self):
        if not self.name:
            return (self.identifier)
        return (self.name)

    def get_absolute_url(self):
        return reverse('collection', args=[self.slug])


class Record(TimeStampedModel):

    """
    OLAC conception of an ITEM. Mainly populated with the header element
    of the metadata standard.
    """
    identifier = models.CharField(max_length=256, unique=True)
    datestamp = models.CharField(max_length=48)
    set_spec = models.ForeignKey(Collection, null=True, blank=True)

    def get_title(self):
        try:
            title = self.data.filter(element_type='title')[0].element_data
        except:
            title = ''
        return title

    def remove_data(self):
        MetadataElement.objects.filter(record=self).delete()
        return

    def set_metadata_item(self, metadata_element):
        element = MetadataElement(
            record=self,
            element_type=metadata_element.fieldname,
            element_data=metadata_element.data
        )

        element.save()
        return element

    def get_metadata_item(self, e_type):
        return self.data.filter(element_type=e_type)

    def metadata_items(self):
        return self.data.all()

    def metadata_items_json(self):
        json_metadata = {}
        for e in self.metadata_items():
            jsonobj = json.loads(e.element_data)
            if jsonobj:
                json_metadata[e.element_type] = jsonobj
            else:
                json_metadata[e.element_type] = ['']

        return json_metadata

    def sort_metadata_dict(self, record_dict):
        """Sort record dictionary by key"""
        return OrderedDict(sorted(record_dict.items(), key=lambda t: t[0]))

    def as_dict(self):
        """ Returns a dictionary of the record data as k,v = {element type: element data list}"""
        record_dict = {}

        record_dict['collection'] = [self.set_spec]
        record_dict['site_url'] = [self.get_absolute_url()]
        record_dict['datestamp'] = [self.datestamp]

        elements = self.data.all().order_by('element_type')
        for e in elements:
            etype = e.element_type.replace('.', '_')
            edata = e.element_data
            if etype == 'spatial':
                edata = json.loads(edata)
            try:
                record_dict[etype].append(edata)
            except KeyError:  # no key yet, make one and assign a new data list
                record_dict[etype] = [edata]

        return record_dict

    def get_map_plot(self):
        """ Returns a Plot namedtuple object or None if no map data assigned to this record """
        map_data = self.get_metadata_item('spatial')
        if not map_data:
            return None
        plot = json.loads(map_data[0].element_data)
        return Plot(plot['east'], plot['north'])

    def list_languages(self):
        """ Returns a list of languages listed in this record """
        languages = set()
        [languages.add(i.element_data) for i in self.get_metadata_item('subject.language')]
        return list(languages)

    def list_subject_languages_as_tuples(self):
        """ Returns a list of subject.language tuples (code, print_name) listed in this record."""
        languages = set()
        [languages.add(i.element_data) for i in self.get_metadata_item('subject.language')]
        language_list = []
        for i in list(languages):
            for j in SearchQuerySet().filter(code=i):
                language_list.append(Language(j.code, j.print_name))
        return language_list

    def make_update(self, datestamp_str):
        newdate = datetime.datetime.strptime(datestamp_str, '%Y-%m-%d').date()
        curdate = datetime.datetime.strptime(self.datestamp, '%Y-%m-%d').date()
        return newdate > curdate

    def __unicode__(self):
        title = self.get_metadata_item('title')[0].element_data
        return '%s' % (title)

    def get_absolute_url(self):
        return reverse('item', args=[str(self.id)])


class MetadataElement(models.Model):

    """A tuple containing an element_type (dublin core) and its data"""
    record = models.ForeignKey(Record, null=True, related_name='data')
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(null=True, default='')

    def __unicode__(self):
        return u'%s:%s' % (self.element_type, self.element_data)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])


class ArchiveMetadataElement(models.Model):

    """
    A archive informationtuple containing an
    element_type (dublin core/olac) and its data
    """
    repository = models.ForeignKey(
        Repository, null=True, related_name='archive_data')
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(default='')

    def __unicode__(self):
        return u'%s:%s' % (self.element_type, self.element_data)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

class ISOLanguageNameIndex(models.Model):
    """
    Models the ISO 693-3 Language Names Index
    http://www-01.sil.org/iso639-3/download.asp
    CREATE TABLE [ISO_639-3_Names] (
         Id             char(3)     NOT NULL,  -- The three-letter 639-3 identifier
         Print_Name     varchar(75) NOT NULL,  -- One of the names associated with this identifier
         Inverted_Name  varchar(75) NOT NULL)  -- The inverted form of this Print_Name form
    """

    code = models.CharField(max_length=3)
    print_name = models.CharField(max_length=75)
    inverted_name = models.CharField(max_length=75, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.print_name)


