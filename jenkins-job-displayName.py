import jenkins
import xml.etree.ElementTree as ET
import xmltodict
import json

def convert_xml_file_to_str():
	tree = ET.parse('/root/job2.xml')
	root = tree.getroot()
        return ET.tostring(root, encoding='utf8', method='xml').decode()

def main():

	with open('/root/job2.xml') as fd:
       	 doc = xmltodict.parse(fd.read())
	str = json.dumps(doc)
	dict = json.loads(str)
	name = dict.get("flow-definition").get("displayName")
	server = jenkins.Jenkins('http://192.168.1.224:8080', username='root', password='polus123')
	user = server.get_whoami()
	version = server.get_version()
	print('Hello %s from Jenkins %s' % (user['fullName'], version))
	config = convert_xml_file_to_str()

	server.create_job(name,config)
#	jobs = server.get_jobs()
#	print jobs
#	my_job = server.get_job_config('test')
#	print my_job
main()
