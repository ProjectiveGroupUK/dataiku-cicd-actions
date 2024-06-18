import dataikuapi
import radon.raw as cc_raw
import radon.visitors as cc_visitors
import logging


def test_scenario(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    # Check that there is at least one scenario TEST_XXXXX & one TEST_SMOKE
    scenarios = project.list_scenarios()
    test_scenario = False
    smoketest_scenario = False
    for scenario in scenarios:
        if scenario["id"].startswith("TEST"):
            test_scenario = True
            if scenario["id"] == "TEST_SMOKE":
                smoketest_scenario = True
    assert test_scenario, "You need at least one test scenario (name starts with 'TEST_')"
    assert smoketest_scenario, "You need at least one smoke test scenario (name 'TEST_SMOKE')"

    
def test_coding_recipes_complexity(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    recipes = project.list_recipes()
    for recipe in recipes:
        if recipe["type"] == "python":
            print(recipe)
            payload = project.get_recipe(recipe["name"]).get_settings().get_code()
            code_analysis = cc_raw.analyze(payload)
            print(code_analysis)
            assert code_analysis.loc < 100
            assert code_analysis.lloc < 50
            v = cc_visitors.ComplexityVisitor.from_code(payload)
            assert v.complexity < 21, "Code complexity of recipe " + recipe["name"] + " is too complex: " + v.complexity + " > max value (21)"



##NEW unit testing for code environments and scenario reporters


# Test 1: All python recipes have a dedicated code environment
def check_code_recipes_environment(params):
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
        print(f"Recipe settings: {recipe_settings}")
        
        # Accessing the type of the recipe
        recipe_type = recipe_settings.type
        print(f"Recipe type: {recipe_type}")
        
        if 'custom_python' in recipe_type or 'python' in recipe_type:
            env_details = recipe_settings.get_code_env_settings()
            print(f"Environment details: {env_details}")
            
            if 'envMode' not in env_details:
                code_recipes_without_env.append(recipe['name'])
            else:
                env_mode = env_details['envMode']
                print(f"Environment mode: {env_mode}")
                    
                if env_mode != 'EXPLICIT_ENV':
                    code_recipes_without_env.append(recipe['name'])
                elif 'EXPLICIT_ENV' not in env_mode:
                    code_recipes_without_env.append(recipe['name'])
 

    if code_recipes_without_env:
        logging.error(f"Code recipes without a dedicated code environment: {code_recipes_without_env}")
        raise Exception(f"Code recipes without a dedicated code environment: {code_recipes_without_env}")      
    else:
        logging.info("All code recipes have a dedicated code environment.")
        

# Test 2: All scenarios have at least one active reporter
def check_scenarios_active_reporters(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project_obj = client.get_project(params["project"])

    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info("Checking active reporters for all scenarios...")
    scenarios = project_obj.list_scenarios()
    scenarios_without_reporters = []
    
    for scenario in scenarios:
        scenario_obj = project_obj.get_scenario(scenario['id'])
        print(scenario_obj)

        scenario_settings = scenario_obj.get_settings()
        print(f"Scenario settings: {scenario_settings}")

        raw_settings = scenario_settings.get_raw()
        print(f"Raw settings: {raw_settings}")
        
        if 'reporters' not in raw_settings or not raw_settings['reporters']:
            scenarios_without_reporters.append(scenario['id'])
        else:
            active_reporters = [reporter for reporter in raw_settings['reporters'] if reporter.get('active', False)]
            if not active_reporters:
                scenarios_without_reporters.append(scenario['id'])

    
    if scenarios_without_reporters:
        error_message = f"Scenarios without active reporters: {scenarios_without_reporters}"
        logging.error(error_message)
        raise Exception(error_message)
    else:
        logging.info("All scenarios have active reporters.")
        

# Run checks
#check_code_recipes_environment(params)
#check_scenarios_active_reporters(params)
#logging.info("All checks passed successfully.")
