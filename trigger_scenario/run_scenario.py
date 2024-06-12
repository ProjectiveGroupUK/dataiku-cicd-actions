
import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]

client = dataikuapi.DSSClient(host,apiKey )
test_project = client.get_project(project)

## Extra step that first pulls the remote changes into the dataiku project's local repository on DSS
## For Demo purposes make sure you first switch the DSS project to the 'scenarios' branch (I think)
# project_git = dataikuapi.dss.project.DSSProjectGit(client, project)
# branch_name = 'scenarios'
# project_git.pull(branch_name)

## Step that calls the scenario to rebuild the flow, run DQ checks, create and deploy a new bundle if the checks succeed
scenario = test_project.get_scenario('TEST')
scenario.run_and_wait()
