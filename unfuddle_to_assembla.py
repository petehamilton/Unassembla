import pycurl
import StringIO
from xml.etree import ElementTree as ET
from unfuddle_helper import UnfuddleHelper
from assembla_helper import AssemblaHelper
import sys
sys.path.append('python-rest-client')
from restful_lib import Connection

from settings import *

UH = UnfuddleHelper(unfuddle_subdomain,unfuddle_project_id,unfuddle_username,unfuddle_password)
AH = AssemblaHelper(assembla_space,assembla_username,assembla_password)
ARC = Connection("http://www.assembla.com/spaces/"+assembla_space, username=assembla_username, password=assembla_password)
URC = Connection("http://"+unfuddle_subdomain+".unfuddle.com/api/v1/projects/"+unfuddle_project_id, username=unfuddle_username, password=unfuddle_password)


ticket_map = {}

class UnfuddleToAssembla:
	
	def main(self):
		uts = UH.getTickets()
		print uts
		# for t in uts:
		# 	ARC.request_delete('tickets/'+t['number'])
		# 	print "Copying ticket #" + t['number']
		# 	self.convertAndSave(t)

	def convertAndSave(self,unfuddle_ticket):
		assembla_ticket = {}
		assembla_ticket['number'] = unfuddle_ticket['number']
		assembla_ticket['summary'] = unfuddle_ticket['summary']
		assembla_ticket['created-on'] = unfuddle_ticket['created-at']
		assembla_ticket['updated-at'] = unfuddle_ticket['updated-at']

		#Priority is inverse for assembla
		assembla_ticket['priority'] = str(6 - int(unfuddle_ticket['priority']))

		assembla_ticket['status'] = unfuddle_ticket['status']
		
		#Map across
		assembla_ticket['acts-as-user-id'] = self.mapUser(unfuddle_ticket['reporter-id'])
		assembla_ticket['assigned-to-id'] = self.mapUser(unfuddle_ticket['assignee-id'])
		
		#Create/link with milestones
		if unfuddle_ticket['milestone-id']:
			assembla_ticket['milestone-id'] = self.copyMilestone(unfuddle_ticket['milestone-id'])
		
		#If component exists, map, otherwise blank
		assembla_ticket['component-id'] = None
		
		#Optionals
		assembla_ticket['description'] = unfuddle_ticket['description']
		# assembla_ticket['skip-alerts'] = None
		# assembla_ticket['working-hours'] = None
		
		xml = AH.createTicketXML(assembla_ticket)
		new_ticket = AH.saveTicketXML(xml)
		new_ticket = AH.parseTicketXML(new_ticket)
		
		
		#Add any associated comments
		assembla_ticket = {}
		try:
			for comment in unfuddle_ticket['comments']:
				assembla_ticket['user-comment'] = comment['body']
				assembla_ticket['updated-at'] = comment['updated-at']
				assembla_ticket['acts-as-user-id'] = self.mapUser(unfuddle_ticket['reporter-id'])
				xml = AH.createTicketXML(assembla_ticket)
				print "updating"
				AH.updateTicketXML(new_ticket['id'],xml)
			#Add resolution as a comment
			assembla_ticket['user-comment'] = unfuddle_ticket['resolution-description']
			assembla_ticket['updated-at'] = unfuddle_ticket['updated_at']
			assembla_ticket['acts-as-user-id'] = None
			assembla_ticket['status'] = unfuddle_ticket['resolution']		
		except: #keyerror?
			pass
		ticket_map[unfuddle_ticket['id']] = new_ticket['id']

	def mapUser(self, unfuddle_user_id):
		assembla_users = AH.getUsers()
		unfuddle_users = UH.getUsers(True)
		try:
			return assembla_users[user_map[unfuddle_users[unfuddle_user_id]]]
		except: #Most likely key error
			return None

	def copyMilestone(self, milestoneID):
		assembla_milestones = AH.getMilestones()
		unfuddle_milestones = UH.getMilestones(True)
		try:
			return assembla_milestones[unfuddle_milestones[milestoneID]]
		except: #Milestone doesn't exist
			unfuddle_milestone = UH.getMilestone(milestoneID)
			assembla_milestone['title'] = unfuddle_milestone['title']
			assembla_milestone['description'] = unfuddle_milestone['description']
			assembla_milestone['created-at'] = unfuddle_milestone['created-at']
			assembla_milestone['updated-at'] = unfuddle_milestone['updated-at']
			assembla_milestone['due-date'] = unfuddle_milestone['due-on']
			assembla_milestone['completed'] = unfuddle_milestone['completed']
			assembla_milestone['user-id'] = self.mapUser(unfuddle_milestone['person-responsible'])
			m = AH.createMilestone(assembla_milestone)
			return m['id']

