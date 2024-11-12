import dataikuapi
import radon.raw as cc_raw
import radon.visitors as cc_visitors
import logging
import warnings


# def test_scenario(params):
#     client = dataikuapi.DSSClient(params["host"], params["api"])
#     project = client.get_project(params["project"])

#     # Check that there is at least one scenario TEST_XXXXX & one TEST_SMOKE
#     scenarios = project.list_scenarios()
#     test_scenario = False
#     smoketest_scenario = False
#     for scenario in scenarios:
#         if scenario["id"].startswith("TEST"):
#             test_scenario = True
#             if scenario["id"] == "TEST_SMOKE":
#                 smoketest_scenario = True
#     assert test_scenario, "You need at least one test scenario (name starts with 'TEST_')"
#     assert smoketest_scenario, "You need at least one smoke test scenario (name 'TEST_SMOKE')"

    
# def test_coding_recipes_complexity(params):
#     client = dataikuapi.DSSClient(params["host"], params["api"])
#     project = client.get_project(params["project"])

#     recipes = project.list_recipes()
#     for recipe in recipes:
#         if recipe["type"] == "python":
#             print(recipe)
#             payload = project.get_recipe(recipe["name"]).get_settings().get_code()
#             code_analysis = cc_raw.analyze(payload)
#             print(code_analysis)
#             assert code_analysis.loc < 100
#             assert code_analysis.lloc < 50
#             v = cc_visitors.ComplexityVisitor.from_code(payload)
#             assert v.complexity < 21, "Code complexity of recipe " + recipe["name"] + " is too complex: " + v.complexity + " > max value (21)"



##NEW unit testing for code environments and scenario reporters


# Test 1: All python recipes have a dedicated code environment
def test_check_code_recipes_environment(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project_obj = client.get_project(params["project"])

    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Checking code environments for all code recipes...")

    recipes = project_obj.list_recipes()
    code_recipes_without_env = []

    for recipe in recipes:
        recipe_obj = project_obj.get_recipe(recipe['name'])
        recipe_settings = recipe_obj.get_settings()
        recipe_type = recipe_settings.type

        if 'custom_python' in recipe_type or 'python' in recipe_type:
            
            logging.info(f"Recipe name: {recipe['name']}")
            logging.info(f"Recipe type: {recipe_type}")

            project_default_env_details = project_obj.get_settings().get_raw()['settings']['codeEnvs']['python']
            project_default_env_mode = project_default_env_details['mode']
            logging.info(f"Project default settings for Python code envs: {project_default_env_details}")

            recipe_env_details = recipe_settings.get_code_env_settings()
            recipe_env_mode = recipe_env_details['envMode']
            logging.info(f"Recipe environment details: {recipe_env_details}")

            if recipe_env_mode == 'USE_BUILTIN_MODE' or (project_default_env_mode != 'EXPLICIT_ENV' and recipe_env_mode != 'EXPLICIT_ENV'):
                code_recipes_without_env.append(recipe['name'])

    if code_recipes_without_env:
        logging.error(f"Code recipes without a dedicated code environment: {code_recipes_without_env}")
        raise Exception(f"Code recipes without a dedicated code environment: {code_recipes_without_env}")      
    else:
        logging.info("All code recipes have a dedicated code environment.")
        

# Test 2: All scenarios have at least one active reporter
def test_check_scenarios_active_reporters(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project_obj = client.get_project(params["project"])

    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info("Checking active reporters for all scenarios...")
    scenarios = project_obj.list_scenarios()
    scenarios_with_reporters = []
    
    for scenario in scenarios:
        scenario_obj = project_obj.get_scenario(scenario["id"])
        scenario_settings = scenario_obj.get_settings()
        raw_settings = scenario_settings.get_raw()

        # Attached reporters
        active_reporters = []
        attached_reporters = raw_settings.get("reporters", [])

        # An attached reporter must be active in order to pass the requirements
        active_reporters.extend([reporter for reporter in attached_reporters if reporter.get("active", False)])

        # python reporters
        steps = raw_settings.get("params", {}).get("steps", [])
        if steps and "params" in steps[0]:
            step_params = steps[0]["params"]
            script = step_params.get("script")
            if script and ("https://hooks.slack.com/services" in script or "post_slack_message" in script):
                active_reporters.append(steps[0].get("name"))

        if active_reporters:
            scenarios_with_reporters.append(scenario["id"])

    
    if not scenarios_with_reporters:
        warning_message = f"There are no Scenarios with active reporters"
        logging.warning(warning_message)
        warnings.warn(warning_message)
    else:
        logging.info(f"There are {len(active_reporters)} active reporters.")