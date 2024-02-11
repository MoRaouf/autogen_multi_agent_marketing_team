import os
import json
from  datetime import datetime
import openai
import autogen
import requests
from typing import Optional, Union, Type, List

# Content Team
from PIL import Image
from io import BytesIO
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials


# Market Research Team
from SeoKeywordResearch import SeoKeywordResearch
from bs4 import BeautifulSoup

# LangChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate

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
# Contetnt Team Functions
#==============================================================================

# --------------------------- Head of Content ---------------------------
class ContentTeamToolInput(BaseModel):
    instructions: str = Field(description = "Detailed instructions for the Content Team to accomplish the required tasks")

class ContentTeamTool(BaseTool):
    name = "content_team"
    description = "A function used to access the Content Team & assign them relevant tasks"
    args_schema: Type[BaseModel] = ContentTeamToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, instructions: str):
        
        from agents import Content_Creator, Editor, Designer, Email_Marketer, Content_Assistant, llm_config

        groupchat = autogen.GroupChat(
            agents=[Content_Creator, Editor, Designer, Email_Marketer, Content_Assistant],
            messages=[],
            max_round=10
            )
        manager = autogen.GroupChatManager(groupchat=groupchat, 
                                           name = "Content_Team_Chat_Manager",
                                           llm_config=llm_config)

        Content_Assistant.initiate_chat(
            manager, 
            message=instructions)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f"chat_history/Content_Team_chat_{timestamp}.json", "w") as json_file:
            json.dump(groupchat.messages, json_file, indent=2)


# --------------------------- Content Creator ---------------------------
class SaveContentToolInput(BaseModel):
    content: str = Field(description = "Generated content to be saved")

class SaveContentTool(BaseTool):
    name = "save_content"
    description = "A function to save the generated content in a text file"
    args_schema: Type[BaseModel] = SaveContentToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, content: str):

        # Get the current timestamp in a specific format (e.g., YYYYMMDDHHMMSS)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'teams/Content_Team/Content_Creator/content_{timestamp}.txt', 'w') as file:
            file.write(content)

        # Return the content to be passed to next agent
        return content


# --------------------------- Designer ---------------------------
class CreateImageToolInput(BaseModel):
    prompt: str = Field(description = "The input prompt to generate the image")
    n: int = Field(description="The number of images to generate. Default to 1.")
    size: str = Field(description="The size of the image. Default to 1024x1024.")

class CreateImageTool(BaseTool):
    name = "create_image"
    description = "A function used to generate images & poster designs"
    args_schema: Type[BaseModel] = CreateImageToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, prompt: str, n: int = 1, size: str = "1024x1024") -> str:
        
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size
            )
        image_url = response['data'][0]['url']

        response = requests.get(image_url)

        if response.status_code == 200:

            image_data = response.content
            image = Image.open(BytesIO(image_data))

            # Get the current timestamp in a specific format (e.g., YYYYMMDDHHMMSS)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_path = f'Content_Team/Designer/image_{timestamp}.jpg'
            image.save(image_path)

        else:
            print("Failed to download the image. Status code:", response.status_code)

# --------------------------- Email Marketer ---------------------------
# If modifying these SCOPES, delete the file token.json
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/gmail.compose",
            # "https://www.googleapis.com/auth/gmail.send",
            ],
    client_secrets_file="utils/google_credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
tools = GmailToolkit(api_resource=api_resource).get_tools()

# Get GmailSendMessage tool
CreateDraftTool = tools[0]
SendEmailTool = tools[1]

# from utils.agent_utils import generate_oai_func
# from pprint import pprint
# pprint(generate_oai_func(SendEmailTool))


# --------------------------- Content Team Functions ---------------------------
content_team_functions = {"Content_Creator": [SaveContentTool()],
                          "Designer": [CreateImageTool()],
                          "Email_Marketer":[CreateDraftTool,SendEmailTool],
                          }


#==============================================================================
# Market Research Team Functions
#==============================================================================

# --------------------------- Head of Market Research ---------------------------
class MarketResearchTeamToolInput(BaseModel):
    instructions: str = Field(description = "Detailed instructions for the Market Research Team to accomplish the required tasks")

class MarketResearchTeamTool(BaseTool):
    name = "market_research_team"
    description = "A function used to access the Market Research Team & assign them relevant tasks"
    args_schema: Type[BaseModel] = MarketResearchTeamToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, instructions: str):
        
        from agents import Market_Researcher, SEO_Specialist, Data_Analyst, Research_Assistant, llm_config
        from utils.agent_functions import (
            ContentTeamTool,
            MarketResearchTeamTool,
            SaveContentTool,
            CreateImageTool,
            SendEmailTool,
            WebSearchTool,
            ScrapeTool,
            KeywordResearchTool
        )

        groupchat = autogen.GroupChat(
            agents=[Market_Researcher, SEO_Specialist, Data_Analyst, Research_Assistant],
            messages=[],
            max_round=10
            )
        manager = autogen.GroupChatManager(groupchat=groupchat, 
                                           name = "Market_Research_Team_Chat_Manager",
                                           llm_config=llm_config)

        Research_Assistant.initiate_chat(
            manager, 
            message=instructions)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f"chat_history/Market_Research_Team_chat_{timestamp}.json", "w") as json_file:
            json.dump(groupchat.messages, json_file, indent=2)

# --------------------------- Market Researcher ---------------------------
class WebSearchToolInput(BaseModel):
    query: str = Field(description = "Query to search for on Google")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "A function used to search for a query on Google"
    args_schema: Type[BaseModel] = WebSearchToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, query: str, num_results:int=3):
        url = "https://google.serper.dev/search"

        payload = json.dumps({
            "q": query,
            "num":num_results,
        })
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = response.json()
        links_list = [item["link"] for item in json_response["organic"]]

        return links_list


# ------------------------ Summary -------------------------
def summary(text):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=3000, chunk_overlap=300)
    docs = text_splitter.create_documents([text])
    map_prompt = """
    Write a short summary of the following text for a research purpose:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text"])
    
    combine_prompt = """
    Write a detailed summary of the following text with main key ideas & keywords:
    "{text}"
    SUMMARY:
    """
    combine_prompt_template = PromptTemplate(
        template=combine_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=combine_prompt_template,
        verbose=True
    )

    output = summary_chain.run(docs)

    return output

# ------------------------ Scrape -------------------------

class ScrapeToolInput(BaseModel):
    urls: List[str] = Field(description = "List of websites URLs to scrape for data")

class ScrapeTool(BaseTool):
    name = "scrape"
    description = "A function to scrape websites for data"
    args_schema: Type[BaseModel] = ScrapeToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, urls: List[str]):
        scraped_data = []
        for url in urls:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check the response status code
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()

                output = summary(text)
                scraped_data.append(output)

                # if len(text) > 6000:
                #     # output = summary(text)  # You need to define the 'summary' function
                #     output = summary(text[:6000])
                #     scraped_data.append(output)
                    
                # else:
                #     scraped_data.append(text)
            else:
                print(f"HTTP request failed with status code {response.status_code}")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'teams/Market_Research_Team/Market_Researcher/scrape_{timestamp}.json', "w") as json_file:
            json.dump(scraped_data, json_file, indent=2)

        return scraped_data

# ------------------------ Search & Scrape -------------------------

class SearchScrapeToolInput(BaseModel):
    query: str = Field(description = "Query to search for on Google")

class SearchScrapeTool(BaseTool):
    name = "search_scrape"
    description = "A function used to search for a query on Google, get the top 3 results and scrape the websites for data"
    args_schema: Type[BaseModel] = SearchScrapeToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, query: str, num_results:int=3):

        # ==========================  search  =========================
        url = "https://google.serper.dev/search"

        payload = json.dumps({
            "q": query,
            "num":num_results,
        })
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = response.json()
        urls_list = [item["link"] for item in json_response["organic"]]

        # ==========================  scrape  =========================
        scraped_data = []
        for url in urls_list:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check the response status code
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()

                output = summary(text)
                scraped_data.append(output)

            else:
                print(f"HTTP request failed with status code {response.status_code}")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'teams/Market_Research_Team/Market_Researcher/search_scrape_{timestamp}.json', "w") as json_file:
            json.dump(scraped_data, json_file, indent=2)

        formatted_output = ""
        for i, data in enumerate(scraped_data):
            website_header = f"Website {i+1} summary:\n"
            formatted_output+= website_header + data + "\n\n"

        return formatted_output


# --------------------------- SEO Specialist ---------------------------
class KeywordResearchToolInput(BaseModel):
    keywords: List[str] = Field(description = "List of Keywords to search for SEO Optimization")
    # domain: "str" = Field(description = "Google domain. Default to 'google.com'.")
    # country: "str" = Field(description = "Country of the keywords search . Default to 'us'.")
    # language: "str" = Field(description = "Language of the search. Default to 'en'.")

class KeywordResearchTool(BaseTool):
    name = "keyword_research"
    description = "A function used to search for SEO Optimization related keywords"
    args_schema: Type[BaseModel] = KeywordResearchToolInput
    required_args: List = [field for field in args_schema.__annotations__.keys()]

    def _run(self, keywords: List[str]) -> str:
        
        final_results = []

        for kw in keywords:
            keyword_research = SeoKeywordResearch(
            query=kw,
            api_key=os.getenv('SERPAPI_API_KEY'),
            lang='en',
            country='ae',
            domain='google.com'
            )

            auto_complete_results = keyword_research.get_auto_complete()
            related_searches_results = keyword_research.get_related_searches()
            related_questions_results = keyword_research.get_related_questions()

            full_results_text = f"""
            Autocomplete results for "{kw}":
            {auto_complete_results}

            Related searches results for "{kw}":
            {related_searches_results}

            Related questions results for "{kw}":
            {related_questions_results}
            """

            final_results.append(full_results_text)

            data = {
              'auto_complete': auto_complete_results,
              'related_searches': related_searches_results,
              'related_questions': related_questions_results
            }

            # Get the current timestamp in a specific format (e.g., YYYYMMDDHHMMSS)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            with open(f'teams/Market_Research_Team/SEO_Specialist/keywrods_{timestamp}.json', 'w') as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)

        return final_results


# --------------------------- Market Research Functions ---------------------------
market_research_team_functions = {"Market_Researcher": [SearchScrapeTool()],
                                  "SEO_Specialist": [KeywordResearchTool(),],
                                  }

#==============================================================================
# Management Functions
#==============================================================================
management_functions = {"Content_Team":[ContentTeamTool()],
                        "Market_Research_Team":[MarketResearchTeamTool()],
                        }



# print(tools)
# from pprint import pprint
# from utils.agent_utils import get_oai_func_name
# function_map_1={
#         get_oai_func_name(tool):tool._run for _role, tools in market_research_team_functions.items() for tool in tools
#     }

# def ff():
#     pass

# function_map_2={
#         WebSearchTool().name: WebSearchTool()._run()
#     }



# pprint(function_map_1)
# print("\n\n")
# pprint(function_map_2)