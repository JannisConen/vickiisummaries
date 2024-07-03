from datetime import date
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from src.rank_news import rank_news
from src.models import NewsItem, PortfolioEntry
from src.fetch_all_news import fetch_all_news
from src.rank_portfolio import rank_portfolio
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

class NewsRequest(BaseModel):
    start_date: date
    end_date: date
    n_news: int
    portfolio: List[PortfolioEntry]

@app.post("/news")
async def get_most_interesting_news_for_a_portfolio(news_request: NewsRequest):
    relevant_news = []
    ranked_stocks = rank_portfolio(news_request.portfolio)
    for stock in ranked_stocks:
        
        try:
            # TODO: Replace this function with a DB lookup to avoid getting the most interesting news per portfolio
            top_news = await get_most_interesting_news_for_stock(RankNewsRequest(eod_ticker=stock.eod_ticker, start_date=news_request.start_date, end_date=news_request.end_date)) # todo: maybe map relevance to an int and use it
        except Exception as e:
            logging.error("Error ranking news for stock", stock, e)
            continue
        
        relevant_news.append({
            "stock": stock.stock,
            "news": top_news
        })
        
        if len(relevant_news) == news_request.n_news:
            break
        
    return relevant_news

class RankNewsRequest(BaseModel):
    eod_ticker: str
    start_date: date
    end_date: date

@app.post("/news/rank")
async def get_most_interesting_news_for_stock(rank_news_request: RankNewsRequest) -> NewsItem:
    news_for_stock = await fetch_all_news(rank_news_request.eod_ticker, rank_news_request.start_date, rank_news_request.end_date)
    
    if len(news_for_stock) == 0:
        raise ValueError("No news found for stock")
    
    return await rank_news(news_for_stock)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
