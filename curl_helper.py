#!/usr/bin/env python
# encoding: utf-8
"""
curl_helper.py

Created by Peter Hamilton on 2011-04-20.
Copyright (c) 2011 Inspired Pixel. All rights reserved.
"""

import sys
import os
from settings import *
sys.path.append('python-rest-client')
from restful_lib import Connection
from xml_to_obj import xml2obj
from xml.etree import ElementTree as ET

U = 'unfuddle'
A = 'assembla'

class CURLHelper:
	UCurl = Connection("http://"+unfuddle_subdomain+".unfuddle.com/api/v1/projects/"+unfuddle_project_id, username=unfuddle_username, password=unfuddle_password)
	ACurl = Connection("http://www.assembla.com/spaces/"+assembla_space, username=assembla_username, password=assembla_password)
	
	def getTickets(self, system=U):
		SCurl = None
		if system == U:
			SCurl = self.UCurl
			url = "/tickets?comments=true&attachments=true"
		else:	
			url = "/tickets"
			SCurl = self.ACurl
		response = SCurl.request_get(url)
		return str(response['body'])

	def getTicket(self, ticket_id, system=U):
		SCurl = None
		if system == U:
			SCurl = self.UCurl
			url = "/tickets/by_number/"+str(ticket_id)+"?comments=true&attachments=true"
		else:	
			url = "/tickets/by_number/"+str(ticket_id)
			SCurl = self.ACurl
		response = SCurl.request_get(url)
		return str(response['body'])

	def createTicket(self, xml):
		SCurl = self.ACurl
		url = "/tickets"
		response = SCurl.request_post(url,body=xml)
		return str(response['body'])

	def updateTicket(self, ticket_number, xml):
		SCurl = self.ACurl
		url = "/tickets/"+str(ticket_number)
		response = SCurl.request_put(url,body=xml)
		return str(response['body'])

	def getUsers(self, system=U):
		SCurl = None
		if system == U:
			SCurl = self.UCurl
			url = "/people"
		else:	
			url = "/users"
			SCurl = self.ACurl
		response = SCurl.request_get(url)
		return str(response['body'])

	def getMilestones(self, system=U):
		SCurl = None
		if system == U:
			SCurl = self.UCurl
			url = "/milestones"
		else:	
			url = "/milestones"
			SCurl = self.ACurl
		response = SCurl.request_get(url)
		return str(response['body'])

	def getMilestone(self, milestone_id, system=U):
		SCurl = None
		if system == U:
			SCurl = self.UCurl
			url = "/milestones/" + str(milestone_id)
		else:	
			url = "/milestones/" + str(milestone_id)
			SCurl = self.ACurl
		response = SCurl.request_get(url)
		return str(response['body'])
	
	def createMilestone(self, xml):
		SCurl = self.ACurl
		url = "/milestones"
		response = SCurl.request_post(url,body=xml)
		return str(response['body'])


	def getComments(self):
		SCurl = self.UCurl
		response = SCurl.request_get("/tickets/comments")
		return str(response['body'])

	def parseXML(self, xml_schema):
		return xml2obj(xml_schema)
		
	def parseDict(self, assembla_dict, wrapper_tag):
		root = ET.Element(wrapper_tag)
		for k, v in assembla_dict.items():
			xml_attribute = ET.Element(k.replace('_','-'))
			xml_attribute.text = v
			root.append(xml_attribute)
		return ET.tostring(root)