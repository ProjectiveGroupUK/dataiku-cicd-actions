import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]

client = dataikuapi.DSSClient(host,apiKey )
test_project = client.get_project(project)

test_project.Git.pull() #needs testing

scenario = test_project.get_scenario('TEST')

scenario.run_and_wait()
