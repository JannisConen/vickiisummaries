from datetime import date
from typing import Dict, List
import httpx
import asyncio
import json
import os
import logging

from src.models import ConvertibleToNewsItem, News, NewsItem, Podcast

def news_item_factory(item: Dict) -> ConvertibleToNewsItem:
    content_type = item.get('content_type')
    if content_type == "spotify_podcast":
        return Podcast(**item)
    elif content_type == "news":
        return News(**item)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")    
    
def parse_news_items(data: List[Dict]) -> List[NewsItem]:
    news_items = []
    for item in data:
        try:
            news_items.append(news_item_factory(item).to_news_item())
        except Exception as e:
            logging.warning(f"Error parsing news item: {e}")
    return news_items

# TODO: Add auth to automatically fetch this
async def fetch_all_news(stock_name: str, start_date: date, end_date: date) -> List[NewsItem]:
    
    # Define the path as the current directory plus the stock name and file extension
    path = os.path.join(os.getcwd(), "src", "data", stock_name + ".json")
    
    try:
        with open(path, "r") as file:
            data = json.load(file)
            return parse_news_items(data['results'])
    except FileNotFoundError:
        logging.error("File not found.")
        return []
    except json.JSONDecodeError:
        logging.error("Error decoding JSON.")
        return []
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []
        
    # TODO: Add auth to automatically fetch news
    url = f"https://vickiibackend.herokuapp.com/feed/info/"
    params = {
        "content_types": "podcasts,news,newsletter,earning_summary,dpa_analysis",
        "start_date": start_date,
        "end_date": end_date,
        "eod_ticker": f"{stock_name}.US"
    }
    async with httpx.AsyncClient() as client:
        page = 1
        all_news = []
        while True:
            response = await client.get(url, params={**params, "page": page})
            news_page = response.json()
            all_news.extend(news_page['data'])
            if 'next_page' not in news_page:
                break
            page += 1
        return all_news

# for easier isolated testing
async def main():
    all_news = await fetch_all_news("AAPL.US", "2024-05-01", "2024-05-31")
    print(all_news)
    
if __name__ == "__main__":
    asyncio.run(main())