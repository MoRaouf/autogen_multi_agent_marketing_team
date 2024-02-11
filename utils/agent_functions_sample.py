from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from typing import Optional, Union, Type, List
from utils.agent_functions import content_team_functions

import os
import autogen
import openai
from dotenv import load_dotenv
load_dotenv()

#==============================================================================
# Tools Template
#==============================================================================

# class CustomToolInput(BaseModel):
#     arg1: float = Field(description = "")

# class CustomTool(BaseTool):
#     name = ""
#     description = ""
#     args_schema: Type[BaseModel] = CustomToolInput
#     required_args: List = [field for field in args_schema.__annotations__.keys()]

#     def _run(self, arg1: float):
#         return "Write your fucntion logic here"


#==============================================================================
# OpenAI Function Template
#==============================================================================

# [
#     {
#       "name": "get_current_weather",
#       "description": "Get the current weather in a given location",
#       "parameters": {
#         "type": "object",
#         "properties": {
#           "location": {
#             "type": "string",
#             "description": "The city and state, e.g. San Francisco, CA"
#           },
#           "unit": {
#             "type": "string",
#             "enum": ["celsius", "fahrenheit"]
#           }
#         },
#         "required": ["location"]
#       }
#     }
# ]


openai.api_key = os.getenv("OPENAI_API_KEY")
config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    file_location=".",
)

class CircumferenceToolInput(BaseModel):
    radius: float = Field(description = "Radius of the Circle")

class CircumferenceTool(BaseTool):
    name = "circumference_calculator"
    description = "Use this tool when you need to calculate a circumference using the radius of a circle"
    args_schema: Type[BaseModel] = CircumferenceToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, radius: float):
        return "Write your fucntion logic here"

# Define a function to generate OpenAI Function from a LangChain tool
def generate_oai_func(tool):
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

    if tool.args is not None:
      function_schema["parameters"]["properties"] = tool.args

    return function_schema


# Construct the llm_config
llm_config = {
  #Generate functions config for the Tool
  "functions":[generate_oai_func(func) for func in content_team_functions["Head_of_Content"]],
  "config_list": config_list,  # Assuming you have this defined elsewhere
  "seed": 42,  
  "temperature": 0,
  "request_timeout": 120,
}