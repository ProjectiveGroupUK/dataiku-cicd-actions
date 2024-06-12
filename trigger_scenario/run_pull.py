import dataikuapi
import logging
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]

client = dataikuapi.DSSClient(host,apiKey)
test_project = client.get_project(project)

branch_to_pull = 'scenarios'

# Switch to the appropriate branch
try:
    logging.info(f"Switching to branch {branch_to_pull}...")
    project.git_checkout(branch_to_pull)
    logging.info(f"Successfully switched to branch {branch_to_pull}.")
except Exception as e:
    logging.error(f"Error switching to branch {branch_to_pull}: {e}")
    raise

# Pull changes from the remote Git repository
try:
    logging.info(f"Pulling changes from Git branch {branch_to_pull}...")
    project.git_pull()
    logging.info(f"Successfully pulled changes from Git branch {branch_to_pull}.")
except Exception as e:
    logging.error(f"Error pulling changes from Git branch {branch_to_pull}: {e}")
    raise
