s = MetadataElement.objects.filter(element_type='spatial').values('record__set_spec', 'element_data').annotate(collection_locations=Count('record__set_spec'))

{'element_data': u'{"east": "131.8084", "north": "2.9594"}', 'collection_locations': 35, 'record__set_spec': 73}
{'element_data': u'{"east": "100.315246", "north": "30.939924"}', 'collection_locations': 198, 'record__set_spec': 81}
{'element_data': u'{"east": "-149.4909", "north": "-23.3775"}', 'collection_locations': 1, 'record__set_spec': 84}
{'element_data': u'{"east": "134.5495", "north": "7.4278"}', 'collection_locations': 1, 'record__set_spec': 74}
{'element_data': u'{"east": "131.8084", "north": "2.9594"}', 'collection_locations': 3, 'record__set_spec': 74}
{'element_data': u'{"east": "113.0901109", "north": "3.19057"}', 'collection_locations': 1, 'record__set_spec': 68}
{'element_data': u'{"east": "134.5495", "north": "7.4278"}', 'collection_locations': 31, 'record__set_spec': 73}

s = MetadataElement.objects.filter(element_type='spatial').values('record__set_spec', 'element_data', 'record__set_spec__name').annotate(collection_locations=Count('record__set_spec'))

{'element_data': u'{"east": "131.8084", "north": "2.9594"}', 'collection_locations': 3, 'record__set_spec__name': u'Hatohobei and Sonsorol (restricted access)', 'record__set_spec': 74}
{'element_data': u'{"east": "113.0901109", "north": "3.19057"}', 'collection_locations': 1, 'record__set_spec__name': u'Blust Collection', 'record__set_spec': 68}
{'element_data': u'{"east": "-149.4909", "north": "-23.3775"}', 'collection_locations': 1, 'record__set_spec__name': u'Plants and Animals of the Pacific', 'record__set_spec': 84}
{'element_data': u'{"east": "134.5495", "north": "7.4278"}', 'collection_locations': 31, 'record__set_spec__name': u'Hatohobei and Sonsorol', 'record__set_spec': 73}
{'element_data': u'{"east": "100.315246", "north": "30.939924"}', 'collection_locations': 198, 'record__set_spec__name': u'Nyagrong Minyag Collection', 'record__set_spec': 81}
{'element_data': u'{"east": "134.5495", "north": "7.4278"}', 'collection_locations': 1, 'record__set_spec__name': u'Hatohobei and Sonsorol (restricted access)', 'record__set_spec': 74}
{'element_data': u'{"east": "131.8084", "north": "2.9594"}', 'collection_locations': 35, 'record__set_spec__name': u'Hatohobei and Sonsorol', 'record__set_spec': 73}

colls = {}
for i in s:
    coll_key = i['record__set_spec']
    coll_nam = i['record__set_spec__name']
    coll_plot = i['element_data']
    try:
        colls[coll_key]
    except:
        colls[coll_key] = []
        colls[coll_key]['plots'] = []
    colls[coll_key]['name'] = coll_nam
    colls[coll_key]['plots'].append(coll_plot)





                {% for i in mapped_collections %}
                    <div class="mapped_collection_selector
                        {% for j in i.map_plots %}
                            coord{{ j.north|cut:'.'|slice:":6" }}_{{ j.east|cut:'.'|slice:":6" }}
                        {% endfor %}
                        {% for j in i.languages %}
                            {{ j }}
                        {% endfor %}
                    ">
                        {{ i.name }}
                        <input class="title" type="hidden" name="title" value="{{ i.name }}">
                        <input class="language" type="hidden" name="language" value="
                            {% for j in i.languages %} {{ j }} {% endfor %}
                        ">
                        <input class="latitude" type="hidden" name="latitude" value="
                            {% for j in i.map_plots %} {{ j.north }} {% endfor %}
                        ">
                        <input class="longitude" type="hidden" name="longitude" value="
                            {% for j in i.map_plots %} {{ j.east }} {% endfor %}
                        ">
                        <input class="collection" type="hidden" name="collection" value="{{ i.name }}">

                        <input class="site_url" type="hidden" name="site_url" value="{{ i.site_url }}">
                    </div>
                {% endfor %}