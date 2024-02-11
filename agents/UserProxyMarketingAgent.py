from autogen import UserProxyAgent
from queue import Queue

class UserProxyMarketingAgent(UserProxyAgent):
    def __init__(self,  *args, **kwargs):
        super(UserProxyMarketingAgent, self).__init__(*args, **kwargs)

        # Queue to store human sent inputs
        self.human_sent_queue = Queue()
        # Queue to store prompt for human to take action upon
        # self.human_receive_queue = Queue()
        self.human_receive_list = list()
    
    # this is the method we override to interact with the chat
    def get_human_input(self, prompt: str=None) -> str:
        # Prompt to show ot Human to solicit his input
        prompt = f"Provide feedback to Chhief_Marketing_Officer. Press Enter to skip and use auto-reply, or type 'exit' to end the conversation."

        # Show the human the prompt
        self.human_receive_list.append(prompt)
        # Get human input text
        reply = self.human_sent_queue.get(block=True)

        if reply == "exit":
            # If human replied with "exit", show him "EXIT" message
            self.human_receive_list.append("EXIT")

        return reply
        
        
        

# When we pass the user input from st.area_text(), we have to assign it to self.human_sent_queue after we receive it
# so we can retrieve it inside the get_human_input() overridden function.
# We also need to clear st.area_text() from input

# Also set the "value" of the st.area_text() to be self.human_receive_queue 
# to show when the user receives a message from the Chat Manager to deal with. 