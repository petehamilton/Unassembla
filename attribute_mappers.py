#!/usr/bin/env python
# encoding: utf-8
"""
attribute_mappers.py

Created by Peter Hamilton on 2011-04-20.
Copyright (c) 2011 Inspired Pixel. All rights reserved.
"""

from curl_helper import *

class AttributeMapper(object):
	unfuddle_attribute = ''
	assembla_attribute = ''
	
	def __init__(self, unfuddle_attribute, assembla_attribute):
		self.unfuddle_attribute = unfuddle_attribute.replace('-','_')
		self.assembla_attribute = assembla_attribute.replace('-','_')
	def map(self):
		pass

class DirectMapper(AttributeMapper):
	def map(self, model):
		return {self.assembla_attribute:unicode(getattr(model,self.unfuddle_attribute))}

class StatusMapper(AttributeMapper):
	def map(self, model):
		return {self.assembla_attribute:unicode(getattr(model,self.unfuddle_attribute))}

class PriorityMapper(AttributeMapper):
	def map(self, model):
		return {self.assembla_attribute:unicode(6 - int(getattr(model,self.unfuddle_attribute)))}

class UserMapper(AttributeMapper):
	def map(self, model):
		c = CURLHelper()
		unfuddle_users = c.parseXML(c.getUsers())
		assembla_users = c.parseXML(c.getUsers(A))
		for unfuddle_user in unfuddle_users.person:
			if str(unfuddle_user.id) == str(getattr(model,self.unfuddle_attribute)):
				for assembla_user in assembla_users.user:
					if assembla_user.login_name == user_map[unfuddle_user.username]:
						return {self.assembla_attribute:assembla_user.id}
		return {self.assembla_attribute:None}

class MilestoneMapper(AttributeMapper):
	def map(self, model):
		c = CURLHelper()
		unfuddle_milestones = c.parseXML(c.getMilestones())
		assembla_milestones = c.parseXML(c.getMilestones(A))
		for unfuddle_milestone in unfuddle_milestones.milestone:
			if str(unfuddle_milestone.id) == str(getattr(model,self.unfuddle_attribute)):
				for assembla_milestone in assembla_milestones.milestone:
					if assembla_milestone.title == str(unfuddle_milestone.title):
						return {self.assembla_attribute:assembla_milestone.id}
		return {self.assembla_attribute:None}