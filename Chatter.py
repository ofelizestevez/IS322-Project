from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

EMPTY_ACCEPTABLE_PROMPT = " It's acceptable to leave this empty if necessary."

RESPONSE_DESCRIPTION = "your usual chatbot response to the user"
SEARCHQUERY_DESCRIPTION = "search query for video games. only use this when you have enough information from the user to query for a general category or tag, etc. Don't search for games that the user has already played, but search for games similar to it. be more verbose, as this will be used to send to another gpt bot. you want to send information that fulfills the users needs but also is verbose enough to send to another gpt model. Only reset this when user says that want to start over again. Also, remember that the other gpt model will not see the context of your conversation with the user, so the information you send over needs to be self-relient."

class Chatter:
    def __init__(self, api_key, model, temperature) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self._setup()

    def _setup(self):
        class ChatterSchema(BaseModel):
            response: str = Field(alias="response", description=RESPONSE_DESCRIPTION)
            searchQuery: str = Field(alias="search", description=SEARCHQUERY_DESCRIPTION, default=None)
        
        pydantic_parser = PydanticOutputParser(pydantic_object=ChatterSchema)
        format_instructions = pydantic_parser.get_format_instructions()
        
        SEARCH_PROMPT = """
        Your goal is to chat with the user about video games so you can query for games to recommend to them.
        Remember to keep your conversation focused on you wanting to recommend the player a game.
        Also remember to use searchquery when necessary, as this is connected to an API.
        When you use the searchquery, a list of games will be showcased to the user.
        The chat history provided will only contain the user messages, not your messages, so you will know what the user has said but not your replies.
        
        {format_instruction}
        
        chat History:
        {chat_history}
        
        Request:
        {request}
        """
        
        self.PARSER_PROMPT = ChatPromptTemplate.from_template(
			template=SEARCH_PROMPT,
			partial_variables = {
				"format_instruction": format_instructions
			}
		)
        
        self.llm = ChatOpenAI(openai_api_key=self.api_key, model=self.model, temperature=self.temperature)
    
    def parse_request(self, request, chat_history):
        parser_chain = {
			"request": lambda x: x["request"],
   			"chat_history": lambda x: x["chat_history"]
		}| self.PARSER_PROMPT | self.llm
        result = parser_chain.invoke({"request": request, "chat_history": chat_history})
        return result