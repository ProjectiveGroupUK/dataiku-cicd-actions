#import dataikuapi
#import sys
#import time

#host = sys.argv[1]
#apiKey = sys.argv[2]
#project = sys.argv[3]

#client = dataikuapi.DSSClient(host,apiKey)
#test_project = client.get_project(project)

#branch_to_pull = 'scenarios'
#project_git_handle = test_project.get_project_git()

#status = project_git_handle.get_status()
#print(status)

# Switch to the appropriate branch
#project_git_handle.checkout(branch_name=branch_to_pull)

# Fetch updates from the remote repository
#project_git_handle.fetch()

# Pull changes from the remote Git repository
#project_git_handle.pull(branch_name=branch_to_pull)

#status = project_git_handle.get_status()
#print(status)

#time.sleep(5)
