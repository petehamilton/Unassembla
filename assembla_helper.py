import pycurl
from xml.etree import ElementTree as ET
import StringIO

import sys
sys.path.append('python-rest-client')
from restful_lib import Connection

class AssemblaHelper:
	
	assembla_space = ''
	assembla_username = ''
	assembla_password = ''
	
	RC = None
	
	def __init__(self, assembla_space, assembla_username, assembla_password):
		self.assembla_space = assembla_space
		self.assembla_username = assembla_username
		self.assembla_password = assembla_password
		self.RC = Connection("http://www.assembla.com/spaces/"+assembla_space, username=assembla_username, password=assembla_password)

	def getUsers(self,byID=False):
		response = self.RC.request_get('/users')
		users = {}
		for user_element in ET.XML(response['body']):
			user = {}
			for attr in user_element:
				user[attr.tag] = attr.text
			if byID:
				users[user['id']]=user['login_name']
			else:
				users[user['login_name']]=user['id']
		return users
	
	"""
	<milestones type="array">
	  <milestone>
	    <completed-date type="date" nil="true"></completed-date>
	    <created-at type="datetime">2010-07-22T14:04:11+03:00</created-at>
	    <created-by>bgnP_qA1Gr2QjIaaaHk9wZ</created-by>
	    <description>Hello world description</description>
	    <due-date type="date" nil="true"></due-date>
	    <id type="integer">15</id>
	    <is-completed type="boolean">false</is-completed>
	    <release-level type="integer">2</release-level>
	    <release-notes>This release will contain something cool</release-notes>
	    <space-id>at6CkKLwSr34lqacjKAZfO</space-id>
	    <title>My release</title>
	    <updated-at type="datetime">2010-07-23T14:56:03+03:00</updated-at>
	    <updated-by>bgnP_qA1Gr2QjIaaaHk9wZ</updated-by>
	    <user-id></user-id>
	    <pretty-release-level>Beta</pretty-release-level>
	    <documents type="array">
	      <document>
	        <filesize type="integer">139856</filesize>
	        <name>BDD_Intro.pdf</name>
	        <url>http://www.assembla.com/spaces/sap_releases/documents/afJu4MMUyr350kacjKAZfO/download/File1.pdf</url>
	      </document>
	      <document>
	        <filesize type="integer">131988</filesize>
	        <name>CodeConventions.pdf</name>
	        <url>http://www.assembla.com/spaces/sap_releases/documents/ah6L28MUyr350kacjKAZfO/download/File2.pdf</url>
	      </document>
	    </documents>
	  </milestone>
	</milestones>
	"""
	
	def getMilestones(self,byID=False):
		response = self.RC.request_get('/milestones')
		milestones = {}
		return self.parseMilestones(response['body'], byID)
	
	def parseMilestones(self,milestones_xml, byID=False):
		milestones = {}
		for milestone_element in ET.XML(milestones_xml):
			milestone = {}
			for attr in milestone_element:
				milestone[attr.tag] = attr.text
			if byID:
				milestones[milestone['id']]=milestone['title']
			else:
				milestones[milestone['title']]=milestone['id']
		return milestones
	
	def parseMilestone(self,milestone_xml):
		milestone = {}
		for attr in ET.XML(milestone_xml):
			milestone[attr.tag] = attr.text
		return milestone

	def createMilestone(self, args):
		xml = '<milestone>'
		for k,v in args.items():
			xml += '<'+k+'>'+v+'</'+k+'>'
		xml += '</milestone>'
		response = self.RC.request_post('/milestones',body=xml)
		return self.parseMilestone(response['body'])
		

	def parseTicketXML(self, xml):
		"""
		'number':0,
		'summary':'',
		'reporter-id':0,
		'priority':0,
		'status':'',
		#Optionals
		'description':'',
		'user-comment':'',
		'assigned-to-id':'',
		'milestone-id':'',
		'component-id':'',
		'user-comment':'',
		'created-on':'',
		'updated-at':'',
		'acts-as-user-id':'',
		'skip-alerts':False,
		'working-hours':0
		"""
		
		ticket_xml = ET.XML(xml)
		ticket = {}
		for e in ticket_xml:
			ticket[e.tag] = e.text
		return ticket

	def createTicketXML(self, assembla_ticket):
		ticket = ET.Element("ticket")
		for k, v in assembla_ticket.items():
			xml_attribute = ET.Element(k)
			xml_attribute.text = v
			ticket.append(xml_attribute)
		return ET.tostring(ticket)

	def saveTicketXML(self, assembla_ticket_xml):	
		response = self.RC.request_post('/tickets',body=assembla_ticket_xml)
		return response['body']

	def updateTicketXML(self, ticketID, assembla_ticket_xml):
		response = self.RC.request_put('tickets/154',body = assembla_ticket_xml)
		return response['body']