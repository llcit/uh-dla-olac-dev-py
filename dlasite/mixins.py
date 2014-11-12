# mixins.py
import json

from olacharvests.models import MetadataElement, Record, Collection,  Plot

"""NOTE TO self
List comprehensions are great:
Count all the languages in the metadata:
tally = Counter()
tally.update(i.element_data for i in MetadataElement.objects.filter(element_type='subject.language'))

See changes below for examples of list comprehensions.
"""



class MapDataMixin(object):
    """
    Populates additional lists for google map display and browsing.
    Requires a queryset of Record objects. 
    """

    def get_context_data(self, **kwargs):
        context = super(MapDataMixin, self).get_context_data(**kwargs)
        maplists = self.make_map_lists(self.queryset)

        context['mapped_records'] = maplists['mapped_records']
        context['mapped_languages'] = maplists['mapped_languages']
        context['mapped_plots']= maplists['mapped_plots']
        context['mapped_collections'] = maplists['mapped_collections']
        
        return context

    def make_map_lists(self, queryset):
        mapped_plots = set()
        mapped_languages = set()
        mapped_records = []
        mapped_collections = []

        for record in queryset: 
            mapped_data = [json.loads(i.element_data) for i in record.get_metadata_item('spatial')]
            
            [ mapped_plots.add(Plot(i['east'], i['north'])) for i in mapped_data ]    
            mapped_languages |= set([i.element_data for i in record.get_metadata_item('subject.language')])   
            
            mapped_records.append(record.as_dict())
                    
        mapped_plots = self.make_json_map_plots(mapped_plots)

        mapped_collections = [i.as_dict() for i in Collection.objects.all()]

        maplists = {}
        maplists['mapped_records'] = sorted(mapped_records)
        maplists['mapped_languages'] = sorted(mapped_languages)
        maplists['mapped_plots']= mapped_plots
        maplists['mapped_collections'] = mapped_collections

        return maplists

        
    def make_map_plot(self, json_position):
        """
        Create a Plot (namedtuple) from a json representation of metaelement coverage data e.g. [u'7.4278', u'134.5495']
        """
        try:
            return Plot(json_position['north'], json_position['east'])
        except:
            return None

    def make_json_map_plots(self, plots):
        """
        Create a dictionary for each Plot then encode as json string.
        """
        try:
            plots = [ plot._asdict() for plot in list(plots) ]
            return json.dumps( plots ) # jsonify for google maps js client (DOM).
        except:
            return []



class RecordSearchMixin(object):

    def get_queryset(self):
        queryset = super(RecordSearchMixin, self).get_queryset()
        queryset = []
        key = self.request.GET.get('key')
        filteropt = self.request.GET.get('filteropts')

        if key:
            q = MetadataElement.objects.filter(element_type=filteropt).filter(element_data__icontains=key)
            for i in q:
                queryset.append(i.record)
            return queryset
        
        return None