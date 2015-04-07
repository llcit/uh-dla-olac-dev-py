# Setups for interactive mode.
from haystack.query import SearchQuerySet

query = 'mel'
sr = SearchQuerySet().filter(e_type='language.language').filter(e_data=query)