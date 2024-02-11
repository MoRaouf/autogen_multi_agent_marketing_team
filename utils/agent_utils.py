
import autogen


#==============================================================================
# Helper Tools
#==============================================================================

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    file_location=".",
)

llm_config = {
    # "seed": 42,
    "use_cache": False,  
    "temperature": 0,
    "config_list": config_list,
    "request_timeout": 120,
}

# Define a function to generate OpenAI Function from a LangChain tool
def generate_oai_func(tool):

    if hasattr(tool, "required_args"):
        # Define the function schema based on the tool's args_schema
        function_schema = {
            "name": tool.name.lower().replace (' ', '_'),
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [*tool.required_args],
            },
        }
        
    else:
        # Define the function schema based on the tool's args_schema
        function_schema = {
            "name": tool.name.lower().replace (' ', '_'),
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }

    if tool.args is not None:
      function_schema["parameters"]["properties"] = tool.args

    return function_schema



def get_oai_func_name(tool):
    return tool.name