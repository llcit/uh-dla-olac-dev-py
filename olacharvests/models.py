from django.db import models
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from collections import OrderedDict
from django.utils.text import slugify

import json
import operator


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
        self.slug = slugify(self.name)
        super(Repository, self).save(*args, **kwargs)
    
    def list_collections(self):
        return self.collection_set.all()

    def get_info_item(self, info_type):
        return self.archive_data.all(element_type=info_type)

    def set_info_item(self, metadata_element):
        element = ArchiveMetadataElement(
            repository = self,
            element_type = metadata_element.fieldname,
            element_data = metadata_element.data
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
    name = models.CharField(max_length=256, null=True, blank=True)
    repository = models.ForeignKey(Repository, null=True, blank=True)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.slug = slugify(self.id)
        else:
            self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def count_records(self):
        return self.record_set.all().count()

    def list_records(self):
        return self.record_set.all()

    def __unicode__(self):
        if not self.name:
            return (self.identifier)
        return (self.name)

    def get_absolute_url(self):
        return reverse('collection', args=[str(self.slug)])


class Record(TimeStampedModel):

    """
    OLAC conception of an ITEM. Mainly populated with the header element 
    of the metadata standard.
    """
    identifier = models.CharField(max_length=256, unique=True)
    datestamp = models.CharField(max_length=48)
    set_spec = models.ForeignKey(Collection, null=True, blank=True)

    def remove_data(self):
        MetadataElement.objects.filter(record=self).delete()
        return

    def set_metadata_item(self, metadata_element):
        element = MetadataElement(
            record = self,
            element_type = metadata_element.fieldname,
            element_data = metadata_element.data
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

    """Sort record dictionary by key"""

    def sort_metadata_dict(self, record_dict):
        return OrderedDict(sorted(record_dict.items(), key=lambda t: t[0]))

    def as_dict(self):
        record_dict = {}
        elements = self.data.all().order_by('element_type')
        for e in elements:
            data = e.element_data
            if e.element_type == 'spatial':
                data = json.loads(data)
                try:
                    record_dict['east'] = data['east']
                    record_dict['north'] = data['north']
                except:
                    record_dict['east'] = []
                    record_dict['north'] = []
            else:
                record_dict[e.element_type] = data
        # record_dict['collection'] = self.set_spec
        record_dict['site_url'] = [self.get_absolute_url()]
        # return self.sort_metadata_dict(record_dict)
        return record_dict

    """Function to get the coordinates of the element to plot in map """

    def get_coordinates(self, json_position):
        coords = {
            "lat": json_position[0],
            "lng": json_position[1]
        }
        print coords
        return coords

    def __unicode__(self):
        title = self.get_metadata_item('title')[0].element_data
        return '%s - %s' % (self.set_spec, title)

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
    repository = models.ForeignKey(Repository, null=True, related_name='archive_data')
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(default='')

    def __unicode__(self):
        return u'%s:%s' % (self.element_type, self.element_data)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

