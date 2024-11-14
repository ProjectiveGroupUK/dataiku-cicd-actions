import dataikuapi
import logging


def test_run_scenario(params, scenario_id):
    logging.info("*************************")
    logging.info("Executing scenario ", scenario_id)
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])
    scenario_result = project.get_scenario(scenario_id).run_and_wait()
    # scenario_result = project.get_scenario(scenario_id).get_last_runs(limit=1)[0]
    logging.info("Scenario info: ", scenario_result.get_info())
    logging.info("Scenario duration: ", scenario_result.get_duration())
    logging.info(scenario_result.get_details()["scenarioRun"]["result"])
    logging.info(scenario_result.get_details()["scenarioRun"]["result"]["outcome"])
    assert scenario_result.get_details()["scenarioRun"]["result"]["outcome"] == "SUCCESS"
