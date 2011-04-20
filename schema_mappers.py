#!/usr/bin/env python
# encoding: utf-8
"""
schema_mappers.py

Created by Peter Hamilton on 2011-04-20.
Copyright (c) 2011 Inspired Pixel. All rights reserved.
"""

from attribute_mappers import DirectMapper, PriorityMapper, StatusMapper, UserMapper, MilestoneMapper
from curl_helper import *

class SchemaMapper(object):
	unfuddle_model = None
	assembla_dict = {}
	mappers = []
	
	def __init__(self, model):
		self.unfuddle_model = model
		self.map()
	
	def map(self):
		for mapper in self.mappers:
			self.assembla_dict.update(mapper.map(self.unfuddle_model))
	
	def get_xml(self, wrapper_tag):
		c = CURLHelper()
		return c.parseDict(self.assembla_dict, wrapper_tag)

class TicketSchemaMapper(SchemaMapper):
	mappers = [
	DirectMapper('number','number'),
	DirectMapper('summary','summary'),
	DirectMapper('created-at','created-on'),
	DirectMapper('updated-at','updated-at'),
	PriorityMapper('priority','priority'),
	StatusMapper('status','status'),
	DirectMapper('description','description'),
	UserMapper('assignee-id','assigned-to-id'),
	MilestoneMapper('milestone-id','milestone-id'),
	# ComponentMapper('milestone-id','milestone-id'),
	UserMapper('reporter-id','acts-as-user-id'),
	]

	def get_xml(self):
		return super(TicketSchemaMapper, self).get_xml('ticket')

class MilestoneSchemaMapper(SchemaMapper):
	mappers = [
	DirectMapper('completed','is-completed'),
	DirectMapper('created-at','created-at'),
	DirectMapper('description','description'),
	DirectMapper('due-on','due-date'),
	UserMapper('person-responsible-id','user-id'),
	DirectMapper('title','title'),
	]

	def get_xml(self):
		return super(MilestoneSchemaMapper, self).get_xml('milestone')

class CommentSchemaMapper(SchemaMapper):
	mappers = [
	DirectMapper('body','user-comment'),
	DirectMapper('updated_at','updated_at'),
	UserMapper('reporter-id','acts-as-user-id'),
	]

	def get_xml(self):
		return super(CommentSchemaMapper, self).get_xml('ticket')