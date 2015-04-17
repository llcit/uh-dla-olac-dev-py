# search_indexes.py
""" See http://django-haystack.readthedocs.org/en/latest/tutorial.html for more
	information about this setup.

    Haystack management commands (e.g., python manage.py <command>:
        clear_index
        haystack_info
        rebuild_index
        update_index


"""
from haystack import indexes

from olacharvests.models import Record, MetadataElement, ISOLanguageNameIndex

class LanguageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    code = indexes.CharField(model_attr='code')
    print_name = indexes.CharField(model_attr='print_name')

    def get_model(self):
        return ISOLanguageNameIndex

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class RecordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    collection = indexes.CharField(model_attr='set_spec')

    def get_model(self):
        return Record

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class MetadataElementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    coll = indexes.CharField(model_attr='record__set_spec__name')
    record = indexes.CharField(model_attr='record')
    e_type = indexes.CharField(model_attr='element_type', faceted=True)
    e_data = indexes.CharField(model_attr='element_data', null=True)

    def get_model(self):
        return MetadataElement

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()