from typing import List, Literal, Tuple
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import logging

from src.helpers import strip_html_tags
from src.models import NewsItem

# return the most interesting news item (assume one news per stock for now)
async def rank_news(news_items: List[NewsItem]) -> NewsItem:
    
    class NewsRanking(BaseModel):
      best_news_id: int = Field(description="The index of the best news item in the list")
    
    parser = JsonOutputParser(pydantic_object=NewsRanking)

    # Think about incorporating the relative change here as an additional information
    prompt = PromptTemplate(
        template="""
            You are a financial news reporter that has to select the news article that will generate the most clicks from your audience.
    
            Focus on the following criteria:
            - is the news item something one can talk about at a dinner party?
            - is the news item super relevant to the outlook of the stock?
            - does the news item have a catchy title?
            - does the news item have direct impact on the stock?
    
            #
            News Items:
            {news_items}
              
            #
            
            {format_instructions}
            """,
        input_variables=["news_items"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    llm = AzureChatOpenAI(
      deployment_name="gpt-4", # have to generally be the same
      model_name="gpt-4",
    )

    chain = prompt | llm | parser

    news_items_string = "\n#\n".join([f"ID{index + 1}: {news_item.title}: {strip_html_tags(news_item.description)}" for index, news_item in enumerate(news_items)])

    result = await chain.ainvoke({"news_items": news_items_string})
    
    logging.info("RANKING RESULT:", result)

    return news_items[result['best_news_id'] - 1]