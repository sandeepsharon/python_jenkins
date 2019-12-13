import jenkins
import xmltodict
import json


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

	server.delete_job(name)
#	jobs = server.get_jobs()
#	print jobs
#	my_job = server.get_job_config('test')
#	print my_job
main()
