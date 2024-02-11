from typing import List, Optional, Tuple, Union, Dict
import autogen
import json
from datetime import datetime

class Orchestrator:
    def __init__(self, name: str, agents: List[autogen.ConversableAgent]):
        self.name = name
        self.agents = agents
        self.messages = []
        # self.complete_keyword = "COMPLETED"
        # self.error_keyword = "ERROR"

        if len(agents) < 2:
            raise Exception("Orchestrator must have at least 2 agents")

    @property
    def total_agents(self) -> int:
        return len(self.agents)
    
    @property
    def last_message_is_string(self):
        return isinstance(self.messages[-1], str)

    @property
    def last_message_is_dict(self):
        return isinstance(self.messages[-1], dict)

    @property
    def last_message_has_func_call(self):
        return self.last_message_is_dict and self.last_message.get("function_call", None)

    @property
    def last_message_has_content(self):
        return self.last_message_is_dict and self.last_message.get("content", None)

    @property
    def last_message(self) -> Optional[Union[dict ,str]]:
        if not self.messages:
            return None
        return self.messages[-1]
    
    def message_to_dict(self, message: Union[Dict, str]):
        """Convert a message to a dictionary.
        The message can be a string or a dictionary. The string will be put in the "content" field of the new dictionary.
        """
        if isinstance(message, str):
            return {"content": message}
        else:
            return message

    def add_message(self, message):
        self.messages.append(message)

    def has_function(self, agent: autogen.ConversableAgent, last_message: Dict):
        if last_message["function_call"]["name"] in agent._function_map:
            return True
        else:
            return False


    def basic_chat(self, 
                   agent_a: autogen.ConversableAgent, 
                   agent_b: autogen.ConversableAgent, 
                   message: str,
                   ): 

        print(f"\n---- Basic_Chat: ({agent_a.name} -> {agent_b.name}) ----\n")

        # This only stores the message in Sender messages, & sends it to recipient
        agent_a.send(message=message, recipient=agent_b) 

        # Recipient will reply taking 'messages=self.chat_messages[sender]'. The reply is Union[str, Dict, None]
        # If basic_chat(agent_a, agent_a), then generate_reply() will execute the function suggested by 'agent_a'
        reply = agent_b.generate_reply(sender=agent_a) 

        # The reply is Union[str, Dict, None], we either add the output str or the 'function_call' suggestion Dict
        # We add the reply when its not None
        if reply:
            self.add_message(self.message_to_dict(reply))
            self.last_message["name"] = agent_b.name

        print(f"\n---- Basic_Chat: {agent_b.name} replied with:\n", reply)


    def function_chat(self,
                      agent_a: autogen.ConversableAgent,
                      agent_b: autogen.ConversableAgent,
                      message: str,
                      ):
        print(f"\n------ 🔁 Function_Chat: ({agent_a.name} -> {agent_b.name}) ------\n")

        # If last agent's ('agent_a') last message was a suggested function_call, then let it execute it
        self.basic_chat(agent_a, agent_a, message)

        # Make sure the execution of function_call resulted with output 'content' str
        # assert self.last_message_has_content

        # Continue the chat between 'agent_a' & 'agent_b' 
        # by sending the reply of basic_chat (this can be either str output or function call outtput) to 'agent_b'
        self.basic_chat(agent_a, agent_b, self.last_message)

        # print(f"\n---- Function_Chat: {agent_b.name} replied with:\n", self.last_message)
        print(f"\n------ ✅ Function_Chat Finished ------\n")


    def sequential_conversation(self, prompt: str) -> Tuple[bool, List[str]]:
        """Runs a sequential converstaion between agents

        Args:
            prompt (str): the input prompt for the conversation

        Returns:
            Tuple[bool, List[str]]: Tuple of was_successful flag and the messages
        """

        print(f"\n\n---------- {self.name} Orchestrator Starting ----------\n\n")

        self.add_message(self.message_to_dict(prompt))

        for idx, agent in enumerate(self.agents):
            agent_a = self.agents[idx]
            agent_b = self.agents[idx + 1]

            if idx==0:
                self.last_message["name"] = agent_a.name

            print(
                f"\n\n~~~~~~~~~~ Running iteration [{idx}] with (agent_a: {agent_a.name}, agent_b: {agent_b.name}) ~~~~~~~~~~\n\n"
                )
            
            # agent_a -> basic chat -> agent_b
            if self.last_message_has_content:
                self.basic_chat(agent_a, agent_b, self.last_message)

            # agent_a -> func_call -> agent_b
            if self.last_message_has_func_call and self.has_function(agent_a, self.last_message):
                self.function_chat(agent_a, agent_b, self.last_message)

            # Terminte the orchestrator when there is only 1 agent left
            # Lets say we have 4 agent. idx starts with 0:
            # 0 -> 1
            # 1 -> 2
            # 2 -> 3
            # 3 -> ??????   here we terminate
            if idx == self.total_agents - 2:
                print(f"\n\n~~~~~~~~~~ ✅ {self.name} Orchestrator was successful ~~~~~~~~~~\n\n")

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                with open(f"chat_history/{self.name}_{timestamp}.json", "w") as json_file:
                    json.dump(self.messages, json_file, indent=2)
                    
                return self.messages

                # print(f"\n\n---------- {self.name} Orchestrator Complete ----------\n\n")

                # was_successful = self.messages[-1].get("content", None) and self.messages[-1].get("content", None).rstrip().endswith("TERMINATE")

                # if was_successful:
                #     print(f"\n\n---------- ✅ {self.name} Orchestrator was successful ----------\n\n")
                # else:
                #     print(f"\n\n---------- ❌ {self.name} Orchestrator failed ----------\n\n")

                # return was_successful, self.messages


    def broadcast_conversation(self, prompt: str) -> Tuple[bool, List[str]]:
        pass
    
    def content_conversation(self, prompt: str):
        # CMOA ----broadcast()----> sequential(Content_Creator,Editor,Head_of_Content,Email_Marketer), Designer
        pass

    def research_content_conversation(self, prompt: str):
        pass
