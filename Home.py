import os
import streamlit as st
from datetime import datetime
import json
import autogen
from agents.agents import (
    Chief_Marketing_Officer_Assistant,
    Content_Creator,
    Designer,
    Editor,
    Email_Marketer,
    Market_Researcher_1,
    Market_Researcher_2,
    SEO_Specialist,
    Content_Team_Orchestrator,
    Market_Research_Team_Orchestrator,
    Research_Content_Orchestrator
)


# ----------------------------------------------------------------------------------
# Page Config
st.set_page_config(
    page_title="Multi-agent AI Marketing Team",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Multi-agent AI Marketing Team")
st.write("> Autonomous Marketing department of AI Agents that can accomplish multiple tasks collaboratively with minimal human intervention.")

# ----------------------------------------------------------------------------------
# Sidebar
with st.sidebar:

    st.title("About")
    st.write("\'AI Marketing Team\' is an app that allows you to automate many of the Marketing department daily tasks.")
    st.write('It consists of a hierarchy of agents where they work autonomously and collaboratively to achieve their goals.')
    st.write("This app is built using the powerful capabilities of *[AutoGen](https://github.com/microsoft/autogen)* framework, which allows to create conversable multi-agent systems.")
    st.markdown("---")
    st.write('Made with ❤️ by [Mohammed Raouf](https://github.com/MoRaouf)')

# ----------------------------------------------------------------------------------
# Team Chat
# st.subheader("Read Team Chat", divider='red')
# team_chat_container = st.container()

# ----------------------------------------------------------------------------------
# Chat Input Text
st.subheader("Chat Input", divider='red')
# Sender & Receiver Selection
st.warning("Select the Sender and Recipient before giving instructions.")

col1, col2 = st.columns(2)
with col1:
    sender = st.selectbox("SENDER", ["Chief_Marketing_Officer_Assistant",
                                    #  "Chief_Marketing_Officer",
                                     ])
with col2:
    recipient = st.selectbox("RECIPIENT", ["Content_Team_Orchestrator",
                                            "Market_Research_Team_Orchestrator",
                                            "Research_Content_Orchestrator",
                                            #  "Chief_Marketing_Officer",
                                            #  "Management_Chat_Manager",  
                                            #  "Head_of_Content", 
                                            #  "Head_of_Market_Research",
                                                ])
    
agents_list = [Chief_Marketing_Officer_Assistant,
                Content_Creator,
                Designer,
                Editor,
                Email_Marketer,
                Market_Researcher_1,
                Market_Researcher_2,
                SEO_Specialist,
                Content_Team_Orchestrator,
                Market_Research_Team_Orchestrator,
                Research_Content_Orchestrator
               ]

# Get Sender & Receiver Agents
def get_agent(agent_name):
    for agent in agents_list:
        if agent_name==agent.name:
            return agent
        else:
            continue
        
sender = get_agent(sender)
recipient = get_agent(recipient)

# sender = [agent for agent in agents_list if sender==agent.name]
# receiver = [agent for agent in agents_list if receiver==agent.name]

# ----------------------------------------------------------------------------------

# Initialize session state for app loading
if "load_state" not in st.session_state:
    st.session_state["load_state"] = False

# Start AutoGen logging
# autogen.ChatCompletion.start_logging()

# ----------------------------------------------------------------------------------

input_text_container = st.container()
with input_text_container: 
    empty_instructions = st.empty()
    input_text = st.text_area(":blue[Message to the Receiver :robot_face: :]", height = None, key="input")

# Add the input text to the self.human_sent_queue
Chief_Marketing_Officer_Assistant.human_sent_queue.put(input_text)

# ----------------------------------------------------------------------------------
# col3, col4 = st.columns(2)
# with col3:
# st.info("Send the message to the Receiver.")
if st.button("Send") or st.session_state.load_state:

    # Change app load_state to True
    st.session_state.load_state = True

    #Start the conversation
    recipient.sequential_conversation(prompt=input_text)
    # sender[0].initiate_chat(
    #     recipient[0],
    #     message=input_text,
    #     clear_history=True
    # )


# with col4 or st.session_state.load_state:
#     st.error("Press the button to stop the conversation.")
#     if st.button("Interrupt Chat"):
#         st.stop()

# ----------------------------------------------------------------------------------
# Team Chat
st.subheader("Read Team Chat", divider='red')
team_chat_container = st.container()

with team_chat_container:
    # Show the chat messages
    with st.expander("**:green[Read Detailed Team Chat]**"):
        for msg in recipient.messages:
            st.write(msg)
        
    with st.expander("**:blue[Read Formatted Team Chat]**", expanded=True):
        # for msg in sender[0].chat_messages[recipient[0]]:
        #     st.write(f"\n\n**---->>> {msg['name']} <<<----** \n\n", msg["content"])
        for msg in recipient.messages:
            if msg:
                st.write(f"\n\n**---->>> {msg['name']} <<<----** \n\n", msg["content"])

# ----------------------------------------------------------------------------------
# Update text_area after getting a new label value
# try:
#     temp_msg = Chief_Marketing_Officer_Assistant.human_receive_list.pop(0)
#     empty_instructions.write(temp_msg)
# except:
#     pass

# ----------------------------------------------------------------------------------
# Save Chat
# st.subheader("Save Chat", divider='red')

# # Save Chat History to a file
# if st.button("Save Chat to File") or st.session_state.load_state:

#     st.session_state.load_state = True

#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     with open(f"chat_history/chat_{timestamp}.json", "w") as json_file:
#         json.dump(recipient.messages, json_file, indent=2)


# Get the human prompt from self.human_receive_queue
# try:
#     human_prompt = Chief_Marketing_Officer_Assistant.human_receive_list.pop(0)
#     placeholder.write(Chief_Marketing_Officer_Assistant.human_receive_list.pop(0))
# except:
#     pass
# human_prompt = Chief_Marketing_Officer_Assistant.human_receive_queue.get(block=True)
# with input_text_container:
#     input_text = st.text_area(human_prompt, height = 120, key="input")


# ----------------------------------------------------------------------------------
# # Update text_area after getting a new label value
# try:
#     temp_msg = Chief_Marketing_Officer_Assistant.human_receive_list.pop(0)
#     empty_instructions.write(temp_msg)
#     # input_text_container.empty()
#     # with input_text_container: 
#     #     input_text = st.text_area(temp_msg, height = 120, key="input")
#     # temp_msg = None
# except:
#     pass



# We want to generate a blog about leveraging the latest generative AI capabilities in the Retail industry.
# We want to write a very short blog about AI in Retail.