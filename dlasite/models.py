from django.db import models

from model_utils.models import TimeStampedModel

from olacharvests.models import Repository

class RepositoryCache(models.Model):
	"""
	Harvester populates these lists at each harvest.
	language_list: dictionary {language: frequency}
	contributor_list: : dictionary {contributor: frequency}
	mapped_data_list: dictionary {geopoint: [collection list]}
	"""
	repository = models.ForeignKey(Repository, unique=True, blank=True)
	language_list = models.TextField(blank=True)
	contributor_list = models.TextField(blank=True)
	mapped_data_list = models.TextField(blank=True)



