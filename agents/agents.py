import os
import autogen
import openai
from utils.agent_functions import content_team_functions, market_research_team_functions, management_functions
from utils.agent_utils import generate_oai_func, get_oai_func_name, llm_config
from agents.UserProxyMarketingAgent import UserProxyMarketingAgent
from agents.Orchestrator import Orchestrator
# from UserProxyMarketingAgent import UserProxyMarketingAgent
# from Orchestrator import Orchestrator

from dotenv import load_dotenv
load_dotenv()


#==============================================================================
# Configuration list + LLM Configuration
#==============================================================================

openai.api_key = os.getenv("OPENAI_API_KEY")
llm_config = llm_config

#==============================================================================
# Management Team
#==============================================================================

management_llm_config = llm_config.copy()

Chief_Marketing_Officer = autogen.AssistantAgent(
    name="Chief_Marketing_Officer",
    llm_config=management_llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message="""You are the Chief Marketing Officer (CMO) of the Marketing Department at our retail company. In your leadership role, you oversee the entire marketing department. As the CMO, you provide strategic direction to all teams within the department, ensuring that they work cohesively to achieve marketing objectives. You have an assistant called 'Chief Marketing Officer Assistant' that can help you execute functions & get the human input of the company's CEO.

    Here is the hierarchy of the teams you lead:

    - Content Team:
        - Content Creator: Creates engaging written content.
        - Editor: Reviews and enhances written content quality.
        - Designer: Creates visually appealing posters and images.
        - Email Marketer: Manages email newsletters featuring recent blogs.

    - Market Research Team:
        - Researcher: Conducts web research and data scraping.
        - SEO Specialist: Optimizes content for SEO.
        - Data Analyst: Analyzes researched data for strategic decision-making.

    Please give very detailed instructions to your teams whenever you ask them to accomplish any task or group of tasks, & specify which team members will be involved in which tasks.

    Reply "TERMINATE" in the end when everything is done.
    """)


# Chief_Marketing_Officer_Assistant = autogen.UserProxyAgent(
#    name="Chief_Marketing_Officer_Assistant",
#    system_message="A Human Assistant for the Chief Marketing officer.",
#    llm_config=management_llm_config,
#    code_execution_config=False,
#    human_input_mode = "ALWAYS"
# )

Chief_Marketing_Officer_Assistant = UserProxyMarketingAgent(
   name="Chief_Marketing_Officer_Assistant",
   system_message="A Human Assistant for the Chief Marketing officer.",
   llm_config=management_llm_config,
   code_execution_config=False,
   human_input_mode = "ALWAYS",
#    function_map={
#         get_oai_func_name(tool):tool._run for _role, tools in management_functions.items() for tool in tools
#     }
)

#==============================================================================
# Content Team
#==============================================================================

# --------------------------- Head of Content ---------------------------

head_of_content_llm_config = llm_config.copy()
# head_of_content_llm_config["functions"] = [generate_oai_func(func) for func in content_team_functions["Head_of_Content"]]

Head_of_Content = autogen.AssistantAgent(
   name="Head_of_Content",
   system_message="""You are the Head of Content (HOC) in the Content Team of the Marketing Department. Your leadership role involves managing the Content Team and ensuring that the content created aligns with the overall marketing strategy. However, before proceeding with content creation, it is essential to coordinate with the CMO to prioritize tasks. Chat with him directly without sending or receiving any emails from him.

    Your team include: 
    - Content Creator: Creates engaging written content.
    - Editor: Reviews and enhances written content quality.
    - Designer: Creates visually appealing posters and images.
    - Email Marketer: Manages email newsletters featuring recent blogs.

    Please give very detailed instructions to your team whenever you ask them to accomplish any task or group of tasks, & specify which team members will be involved in which tasks. 

    Reply "TERMINATE" in the end when everything is done or when there is no need to communicate with the CMO & the HOMR.
    """,
   llm_config=head_of_content_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- Content Creator ---------------------------

content_creator_llm_config = llm_config.copy()
content_creator_llm_config["functions"] = [generate_oai_func(func) for func in content_team_functions["Content_Creator"]]

Content_Creator = autogen.AssistantAgent(
   name="Content_Creator",
   system_message="""You are the Content Creator in the Content Team of the Marketing Department. Your primary responsibility is to create high-quality written content, such as blogs, articles, and social media posts, based on the marketing strategy and objectives. Collaborate with the Editor, Designer, and Email Marketer to ensure content meets quality standards.

    You have access to the following function, which allows you to save the content you created into a text file. 
    Function: `save_content`

    Make sure to save every final version of the content you create into a new text file.

    Reply "TERMINATE" in the end when everything is done.
    """,
   llm_config=content_creator_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- Editor ---------------------------

editor_llm_config = llm_config.copy()

Editor = autogen.AssistantAgent(
   name="Editor",
   system_message="""You are the Editor in the Content Team of the Marketing Department. Your role is to review and edit written content, including blogs, articles, and social media posts, to ensure accuracy, clarity, and consistency.

    Reply "TERMINATE" in the end when everything is done.
    """,
   llm_config=editor_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- Designer ---------------------------

designer_llm_config = llm_config.copy()
designer_llm_config["functions"] = [generate_oai_func(func) for func in content_team_functions["Designer"]]

Designer = autogen.AssistantAgent(
   name="Designer",
   system_message="""You are the Designer in the Content Team of the Marketing Department. Your primary responsibility is to create visually appealing posters for social media posts and images for articles and blogs. Your designs should align with the marketing strategy and branding guidelines.

    Collaborate with the Content Team to ensure that your designs complement the written content. Generated images && posters can have a size of 256x256, 512x512, or 1024x1024 pixels. Choose the proper size of the image based on the type of written content..

    You have access to the following function, which allows you to design an appealing image or poster. 
    Function: `create_image`

    Reply "TERMINATE" in the end when everything is done.
    """,
    llm_config=designer_llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    )

# --------------------------- Email Marketer ---------------------------

email_marketer_llm_config = llm_config.copy()
email_marketer_llm_config["functions"] = [generate_oai_func(func) for func in content_team_functions["Email_Marketer"]]

Email_Marketer = autogen.AssistantAgent(
   name="Email_Marketer",
   system_message="""You are the Email Marketer in the Content Team of the Marketing Department. Your role involves managing and sending email newsletters featuring recent blogs and content.

    You have access to the following function, which allows you to write a draft email & send it to recipient's email. 
    Function: `create_gmail_draft`
    
    Always create a draft email of the generated content by the Content Creator at his email address 'm.raouf.ai@gmail.com'.

    Reply "TERMINATE" in the end when everything is done.
    """,
   llm_config=email_marketer_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- Content Assistant ---------------------------

# content_assistant_llm_config = llm_config.copy()

Content_Assistant = autogen.UserProxyAgent(
    name="Content_Assistant",
    system_message='''Assistant for the Content team to do function calling.''',
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    # llm_config=content_assistant_llm_config,
    code_execution_config=False,
    human_input_mode = "NEVER",
    max_consecutive_auto_reply=10,
    function_map={
        get_oai_func_name(tool):tool._run for _role, tools in content_team_functions.items() for tool in tools
    }
)


#==============================================================================
# Market Research Team
#==============================================================================

# --------------------------- Head of Market Research ---------------------------

head_of_market_research_llm_config = llm_config.copy()
# head_of_market_research_llm_config["functions"] = [generate_oai_func(func) for func in market_research_team_functions["Head_of_Market_Research"]]

Head_of_Market_Research = autogen.AssistantAgent(
   name="Head_of_Market_Research",
   system_message="""You are the Head of Market Research (HOMR) in the Market Research Team of the Marketing Department. 
    You return the results of the SEO Specialist & send instructions to the Content team utilizing the results of the keywords needed to create an optimized content for SEO.
    
    Reply "TERMINATE" in the end when everything is done..
    """,
   llm_config=head_of_market_research_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- Market Researcher: Search & Scrape---------------------------

market_researcher_llm_config = llm_config.copy()
market_researcher_llm_config["functions"] = [generate_oai_func(func) for func in market_research_team_functions["Market_Researcher"]]

Market_Researcher = autogen.AssistantAgent(
   name="Market_Researcher",
   system_message="""You are the Market Researcher Researcher in the Market Research Team of the Marketing Department. Your primary responsibility is to search the web and scrape relevant data to provide valuable insights for SEO Specialist.

    You have access to the following functions to do web research & scraping. 
    Functions: 
    `search_scrape`: A fucntion to do web search & scraping to get websites data.

    Reply "TERMINATE" in the end when you finish.
    """,
   llm_config=market_researcher_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
   function_map={
       get_oai_func_name(tool):tool._run for tool in market_research_team_functions["Market_Researcher"]
       }
)

# --------------------------- Market Researcher 2: Scrape ---------------------------

# market_researcher_llm_config = llm_config.copy()
# market_researcher_llm_config["functions"] = [generate_oai_func(func) for func in market_research_team_functions["Market_Researcher_2"]]

# Market_Researcher_2 = autogen.AssistantAgent(
#    name="Market_Researcher_2",
#    system_message="""You are the Market Researcher Researcher in the Market Research Team of the Marketing Department. Your primary responsibility is to scrape websites fro relevant data to provide valuable insights for SEO Specialist. 

#     You have access to the following functions to do web research & scraping. 
#     Functions: 
#     `scrape`: A fucntion to do web scraping & get website data.

#     Reply "TERMINATE" in the end when you finish.
#     """,
#    llm_config=market_researcher_llm_config,
#    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
#    function_map={
#        get_oai_func_name(tool):tool._run for tool in market_research_team_functions["Market_Researcher_2"]
#        }
# )

# --------------------------- SEO Assistant ---------------------------

seo_specialist_llm_config = llm_config.copy()
# seo_specialist_llm_config["functions"] = [generate_oai_func(func) for func in market_research_team_functions["SEO_Specialist"]]

SEO_Assistant = autogen.AssistantAgent(
   name="SEO_Assistant",
   system_message="""You are the SEO Assistant in the Market Research Team of the Marketing Department. Your role involves finding relevant keywords from researchered websites summaries to help SEO Specialiast in optimizing the content for SEO.

    You only return a list of the most relevant keywords from the summaries to help SEO Specialist in using these keywords to do further SEO Optimization research.

    Reply "TERMINATE" in the end when everything is done.
    """,
   llm_config=seo_specialist_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

# --------------------------- SEO Specialist ---------------------------

seo_specialist_llm_config = llm_config.copy()
seo_specialist_llm_config["functions"] = [generate_oai_func(func) for func in market_research_team_functions["SEO_Specialist"]]

SEO_Specialist = autogen.AssistantAgent(
   name="SEO_Specialist",
   system_message="""You are the SEO Specialist in the Market Research Team of the Marketing Department. Your role involves optimizing content for SEO to improve search engine rankings and visibility. Collaborate with the Researcher to gather keyword data and work closely with the Content Team to implement SEO best practices.

    You have access to the following function, which allows you to research keywords for SEO optimization. 
    Function: `keyword_research`

    Reply "TERMINATE" in the end when everything is done.
    """,
   llm_config=seo_specialist_llm_config,
   is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
   function_map={
       get_oai_func_name(tool):tool._run for tool in market_research_team_functions["SEO_Specialist"]
       }
)

# --------------------------- Research Assistant ---------------------------

# research_assistant_llm_config = llm_config.copy()

# Research_Assistant = autogen.UserProxyAgent(
#     name="Research_Assistant",
#     system_message='''Assistant for the Market Research team to do function calling.''',
#     is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
#     # llm_config=research_assistant_llm_config,
#     code_execution_config={"work_dir": "coding"},
#     human_input_mode = "NEVER",
#     max_consecutive_auto_reply=10,
#     function_map={
#         get_oai_func_name(tool):tool._run for _role, tools in market_research_team_functions.items() for tool in tools
#     }
# )

#==============================================================================
# Chat Orchestrators
#==============================================================================

# Content Team Sequential Chat
Content_Team_Orchestrator = Orchestrator(name= "Content_Team_Orchestrator", agents=[Chief_Marketing_Officer_Assistant,
                                                                                    Content_Creator,
                                                                                    Editor,
                                                                                    Content_Assistant, # AssistantAgent to save content
                                                                                    Email_Marketer,
                                                                                    Designer,
                                                                                    ])

# Market Research Team Sequential Chat
Market_Research_Team_Orchestrator = Orchestrator(name= "Market_Research_Team_Orchestrator", agents=[Chief_Marketing_Officer_Assistant,
                                                                                                    Market_Researcher,
                                                                                                    SEO_Assistant,
                                                                                                    SEO_Specialist,
                                                                                                    Head_of_Market_Research,
                                                                                                    ])

# Research & Content Teams Sequential Chat
Research_Content_Orchestrator = Orchestrator(name= "Research_Content_Orchestrator", agents=[Chief_Marketing_Officer_Assistant,
                                                                                            Market_Researcher,
                                                                                            SEO_Assistant,
                                                                                            SEO_Specialist,
                                                                                            Head_of_Market_Research,
                                                                                            Content_Creator,
                                                                                            Editor,
                                                                                            Email_Marketer,
                                                                                            Designer,
                                                                                            ])

# LlaVa Team normal Chat (UserProxy "ALWAYS" input + Assistant "LlaVa"). Check if I need to add the Designer.
