from datetime import date
from typing import Any, List, Literal, Optional
from pydantic import BaseModel
import re

class PortfolioEntry(BaseModel):
    stock: str
    eod_ticker: str
    amount: float
    change: float
    absolute_value: float
    absolute_change: float
    
# news models
    
class NewsItem(BaseModel):
    title: str
    description: str
    
# use this a kind of interface
class ConvertibleToNewsItem(BaseModel):
    def to_news_item(self) -> NewsItem:
        raise NotImplementedError
    
class StandardNewsInput(ConvertibleToNewsItem):
    id: int
    url: Optional[str]
    uuid: Optional[str]
    eod_ticker: Optional[str]
    ticker_isin: Optional[str]
    ticker_type: Optional[str]
    ticker_logo_url: Optional[str]
    content_type: Literal["spotify_podcast", "news"] # spotify_podcast, news
    image_url: Optional[str]

class Podcast(StandardNewsInput):
    title: Optional[str]
    podcaster: Optional[str]
    podcast_id: int
    description: Optional[str]
    publish_date: Optional[str]
    timestamped_url: Optional[str]
    
    def to_news_item(self) -> NewsItem:
        return NewsItem(title=self.title, description=self.description)
    
class News(StandardNewsInput):
    body: Optional[str]
    lang: Optional[str]
    link: Optional[str]
    title: Optional[str]
    tickers: List[Any]
    read_time: Optional[str]
    article_id: int
    source_url: Optional[str]
    description: Optional[str]
    source_name: Optional[str]
    article_type: Literal["AN", "DN"]
    publish_time: Optional[str]
    vickii_ai_summary: Optional[str]
    source_image_url: Optional[str]
    analyst_price_target: Optional[str]
    analyst_price_currency: Optional[str]
    analyst_recommendation: Optional[str]
    analyst_institution_name: Optional[str]
    analyst_previous_price_target: Optional[str]
    
    def to_news_item(self):
        
        if self.vickii_ai_summary is None:
            # raise error
            raise ValueError("vickii_ai_summary is required")
        
        return NewsItem(title=self.title, description=self.vickii_ai_summary)