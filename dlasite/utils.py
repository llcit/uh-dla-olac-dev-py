# olac_util.py
# from olacharvests.models import Repository, Collection, Record, MetadataElement
from olacharvests.olac import OLACClient
import json

"""
from dlasite.utils import OLACUtil
from olacharvests.olac import *
from olacharvests.models import *
util = OLACUtil('http://localhost:8000/static/test/Kaipuleohone.xml')
repo = util.get_repository()
jrepo = util.get_repository_asdict()
"""


class OLACUtil(object):

    """
    This is a utility class:
    * designed to provide independent procedures for harvesting OLAC repositories.
    * used by django specific views as well as other modules independent of django context.
    * E.g, crontab scripts for automated/scheduled harvests.
    * makes connections to repository base_urls
    * pulls and parses xml (utilizing olac module)
    * writes to db tables
    """

    def __init__(self, xmlfilepath):
        """
        xmlfilepath: a local file or url of an OLAC static repository.
        """

        self.client = OLACClient(xmlfilepath)

    def get_repository(self):
        repository_info = self.client.identify()
        return repository_info

    def get_repository_asdict(self):
        repository_info = self.client.identify()
        info_dict = []
        for i in repository_info:
            d = {}
            d[i.fieldname] = i.data
            info_dict.append(d)
        return info_dict

    def get_record_list(self):
        records_list = self.client.list_records()
        return records_list
        
