from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from typing import Literal

class VideoGameSearchParser:
	def __init__(self, api_key, model, temperature):
		self.api_key = api_key
		self.model = model
		self.temperature = temperature
		self._setup()
  
	def _setup(self):
		class SearchSchema(BaseModel):
			includedGenres: list[Literal["action","indie","adventure","role-playing-games-rpg","strategy","shooter","casual","simulation","puzzle","arcade","platformer","racing","massively-multiplayer","sports","fighting","family","board-games","educational","card"]] = Field(alias= "genres",description="the list of video game genres that should be included in a RESTful query. array for example action,adventure.")
			includedTags: list[Literal["singleplayer","steam-achievements","multiplayer","full-controller-support","steam-cloud,atmospheric,steam-trading-cards","great-soundtrack","rpg","co-op","story-rich","open-world","cooperative","first-person","2d","third-person","sci-fi","partial-controller-support","horror","fps"]] = Field(alias= "tags",description="the list of video game tags that should be included in a RESTful query. for example singleplayer,multiplayer.")

		pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
		format_instructions = pydantic_parser.get_format_instructions()
  
		SEARCH_PROMPT = """
		Your goal is to understand and parse out the user's search paratemeters for a RESTful API for video games.

		{format_instruction}

		Video Game Search Request:
		{request}
		"""

		self.PARSER_PROMPT = ChatPromptTemplate.from_template(
			template=SEARCH_PROMPT, 
			partial_variables= {
				"format_instruction": format_instructions
			}
		)
  
		self.parser_llm = ChatOpenAI(openai_api_key=self.api_key, model=self.model, temperature=self.temperature)

	def parse_request(self, request):
		parser_chain = {"request": lambda x: x["request"]} | self.PARSER_PROMPT | self.parser_llm
		result = parser_chain.invoke({"request": request})
		return result