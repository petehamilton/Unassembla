import pycurl
from xml.etree import ElementTree as ET
import StringIO

import sys
sys.path.append('python-rest-client')
from restful_lib import Connection

class UnfuddleHelper:
	
	unfuddle_subdomain = ''
	unfuddle_project_id = ''
	unfuddle_username = ''
	unfuddle_password = ''
	
	RC = None
	
	def __init__(self, unfuddle_subdomain, unfuddle_project_id, unfuddle_username, unfuddle_password):
		self.unfuddle_subdomain = unfuddle_subdomain
		self.unfuddle_project_id = unfuddle_project_id
		self.unfuddle_username = unfuddle_username
		self.unfuddle_password = unfuddle_password
		self.RC = Connection("http://"+unfuddle_subdomain+".unfuddle.com/api/v1/projects/"+unfuddle_project_id, username=unfuddle_username, password=unfuddle_password)
	
	def getUsers(self, byID=False):
		response = self.RC.request_get('/people')
		users = {}
		for user_element in ET.XML(response['body']):
			user = {}
			for attr in user_element:
				user[attr.tag] = attr.text
			if byID:
				users[user['id']]=user['username']
			else:
				users[user['username']]=user['id']
			
		return users

	"""
	<milestone>
	  <archived type="boolean"> [true, false] </archived>
	  <completed type="boolean"> [true, false] </completed>
	  <created-at type="datetime"> </created-at>
	  <description> </description>
	  <due-on type="date"> </due-on>
	  <due-on-formatted> </due-on-formatted>
	  <id type="integer"> </id>
	  <person-responsible-id type="integer"> </person-responsible-id>
	  <project-id type="integer"> </project-id>
	  <title> </title>
	  <updated-at type="datetime"> </updated-at>
	</milestone>
	"""

	def getMilestones(self,byID=False):
		response = self.RC.request_get('/milestones')
		milestones = {}
		for milestone_element in ET.XML(response['body']):
			milestone = {}
			for attr in milestone_element:
				milestone[attr.tag] = attr.text
			if byID:
				milestones[milestone['id']]=milestone['title']
			else:
				milestones[milestone['title']]=milestone['id']
		return milestones

	def getMilestone(self,id):
		
		response = self.RC.request_get('/milestones/'+id)
		milestone = {}
		milestone = {}
		for attr in ET.XML(response['body']):
			milestone[attr.tag] = attr.text
		return milestone

	def getComponents(self,byID=False):
		response = self.RC.request_get('/components')
		components = {}
		for component_element in ET.XML(response['body']):
			component = {}
			for attr in component_element:
				component[attr.tag] = attr.text
			if byID:
				components[component['id']]=component['title']
			else:
				components[component['title']]=component['id']
		return components

	def getComponent(self,id):
		response = self.RC.request_get('/components/'+id)
		component = {}
		component = {}
		for attr in ET.XML(response['body']):
			component[attr.tag] = attr.text
		return milestones
	
	"""
	<ticket>
	  <assignee-id type="integer"> </assignee-id>
	  <component-id type="integer"> </component-id>
	  <created-at type="datetime"> </created-at>
	  <description> </description>
	  <description-format> [markdown, textile, plain] </description-format>
	  <description-formatted> <!-- only available if formatted=true --> </description-formatted>
	  <due-on type="date"> </due-on>
	  <due-on-formatted> </due-on-formatted>
	  <field1-value-id="integer"> </field1-value-id>
	  <field2-value-id="integer"> </field2-value-id>
	  <field3-value-id="integer"> </field3-value-id>
	  <hours-estimate-current type="float"> </hours-estimate-current>
	  <hours-estimate-initial type="float"> </hours-estimate-initial>
	  <id type="integer"> </id>
	  <milestone-id type="integer"> </milestone-id>
	  <number type="integer"> </number>
	  <priority> [1, 2, 3, 4, 5] </priority>
	  <project-id type="integer"> </project-id>
	  <reporter-id type="integer"> </reporter-id>
	  <resolution> [fixed, works_for_me, postponed, duplicate, will_not_fix, invalid] </resolution>
	  <resolution-description> </resolution-description>
	  <resolution-description-format> [markdown, textile, plain] </resolution-description-format>
	  <resolution-description-formatted> <!-- only available if formatted=true --> </resolution-description-formatted>
	  <severity-id type="integer"> </severity-id>
	  <status> [new, unaccepted, reassigned, reopened, accepted, resolved, closed] </status>
	  <summary> </summary>
	  <updated-at type="datetime"> </updated-at>
	  <version-id type="integer"> </version-id>

	  <!--
	  The following are not actual ticket attributes, but when creating or updating
	  a ticket, including any of these three attributes instead of the corresponding
	  <fieldN-value-id> attributes will allow you to create a new value for
	  the ticekt field if that field is of the "text" disposition.
	  -->
	  <field1-value> </field1-value>
	  <field2-value> </field2-value>
	  <field3-value> </field3-value>

	  <comments type="array"><!-- only available for GET requests if comments=true -->
	    <comment></comment>
	    ...
	  </comments>

	  <attachments type="array"><!-- only available for GET requests if attachments=true -->
	    <attachment>...</attachment>
	    ...
	  </attachments>
	</ticket>
	"""
	#Returns XML for an unfuddle ticket
	def getTicketXML(self, num, comments=True, attachments=False):
			url = "/tickets/by_number/"+str(num)
			if comments and attachments:
				url += "?comments=true&attachments=true"
			elif comments:
				url += "?comments=true"
			elif attachments:
				url += "?attachments=true"
			response = self.RC.request_get(url)
			return response['body']

	#Returns all unfuddle tickets in XML form
	def getTicketsXML(self, comments=True, attachments=False):
		url = "/tickets"
		if comments and attachments:
			url += "?comments=true&attachments=true"
		elif comments:
			url += "?comments=true"
		elif attachments:
			url += "?attachments=true"
		response = self.RC.request_get(url)
		return response['body']
	
	#Returns a dictionary of ticket attribute names and values
	def parseTicketXML(self, ticket_xml):
		"""
		'version-id':'',
		'component-id':'',
		'number':'',
		'reporter-id':'',
		'hours-estimate-initial':'',
		'id':'',
		'hours-estimate-current':'',
		'severity-id':'',
		'updated-at':'',
		'field2-value-id':'',
		'priority':'',
		'status':'',
		'description-format':'',
		'description':'',
		'field1-value-id':'',
		'field3-value-id':'',
		'milestone-id':'',
		'resolution-description':'',
		'due-on':'',
		'created-at':'',
		'summary':'',
		'resolution-description-format':'',
		'resolution':'',
		'project-id':'',
		'assignee-id':'',
		"""
		
		ticket = {}
		for e in ticket_xml:
			if e.tag=='comments':
				comments = []
				for comment in e:
					comments.append(self.parseCommentXML(comment))
					ticket['comments'] = comments
			else:
				ticket[e.tag] = e.text
		return ticket
	
	#Returns a dictionary of a ticket comment attribute names and values
	def parseCommentXML(self, comment_xml):
		"""
		'author-id':'',
		'body':'',
		'body-format':'',
		'created-at':'',
		'id':'',
		'parent-id':'',
		'parent-type':'',
		'updated-at':'',
		"""
		comment = {}
		for e in comment_xml:
			comment[e.tag] = e.text
		return comment
	
	#Gets unfuddle tickets in a list of ticket dictionaries
	def getTickets(self):
		tickets_xml = ET.XML(self.getTicketsXML())
		tickets = []
		for ticket_xml in tickets_xml:
			tickets.append(self.parseTicketXML(ticket_xml))
		return tickets
	
	#Gets an unfuddle ticket dictionary
	def getTicket(self, num):
		ticket_xml = ET.XML(self.getTicketXML(num))
		return self.parseTicketXML(ticket_xml)