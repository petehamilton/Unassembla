#!/usr/bin/env python
# encoding: utf-8
"""
unassembla.py

Created by Peter Hamilton on 2011-04-20.
Copyright (c) 2011 Inspired Pixel. All rights reserved.
"""

import sys
import os
from xml.etree import ElementTree as ET
from schema_mappers import TicketSchemaMapper, MilestoneSchemaMapper, CommentSchemaMapper
from curl_helper import CURLHelper, U, A

class Unassembla:
	
	ticket_map = {}
	def copyTicket(self, ticket_id):
		c = CURLHelper()
		print 'Starting Ticket Import'
		ticket = c.parseXML(c.getTicket(ticket_id))
		mapper = TicketSchemaMapper(ticket)
		new_ticket = c.parseXML(c.createTicket(mapper.get_xml()))
		print '###Imported ' + mapper.assembla_dict['summary']
		try:
			print '###Starting Comments Import'
			for comment in ticket.comments.comment:
				mapper = CommentSchemaMapper(comment)
				c.updateTicket(new_ticket.number,mapper.get_xml())
			print '###Finished Comments Import'
		except:	
			print '###No Comments Found'
			pass
		print 'Finished Ticket Import'

	def copyTickets(self):
		c = CURLHelper()
		print 'Starting Ticket Import'
		ts = c.getTickets()
		print ts
		tickets = c.parseXML(ts)
		for ticket in tickets.ticket[:5]:
			mapper = TicketSchemaMapper(ticket)
			new_ticket = c.parseXML(c.createTicket(mapper.get_xml()))
			print '###Importing "' + mapper.assembla_dict['summary'] +'"'
			try:
				print '###Starting Comments Import'
				for comment in ticket.comments.comment:
					mapper = CommentSchemaMapper(comment)
					c.updateTicket(new_ticket.number,mapper.get_xml())
				print '###Finished Comments Import'
			except:
				print '###No Comments Found'
				pass
			ticket_map[ticket.id] = new_ticket.id
		print 'Finished Ticket Import'

	def copyMilestones(self):
		c = CURLHelper()
		print 'Starting Milestone Import'
		milestones = c.parseXML(c.getMilestones())
		try:
			for milestone in milestones.milestone:
				mapper = MilestoneSchemaMapper(milestone)
				c.createMilestone(mapper.get_xml())
				print '###Imported ' + mapper.assembla_dict['title']
		except TypeError:
			print '### No Milestones Found'
		print 'Finished Milestone Import'


def main():
	u = Unassembla()
	u.copyTickets()


if __name__ == '__main__':
	main()