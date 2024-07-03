# Vickii News Ranking

The problem: There are news per share coming in every week. This is a first MVP on how to personalize the news shown to a user and cut them down to n_news amount of the most interesting news.

## 1. step
Rank stock importance in a portfolio by looking out for outliers in absolute and relative change given the overall portfolio size and otherwise sorting by absolute change to determine which share is worth showing news for.

## 2. step
Iterate over most important stocks for the user given the portfolio and select the most interesting news using GPT and telling it to look out for news that have a high impact on the stock price or news that serve well for users to be able to share the news with their friends.

# What is left to do:
1. fetching news is now done from using .json exports in the system from what Jai sent me -> connect this to Vickii API
2. store the "most-interesting" ranked news in a database and query it when assigning news to a portfolio to avoid having to reevaluate all news for every portfolio
3. optimize prompt

# What to consider:
Possibly let GPT also assign an "interest_score" to each news to maybe be able to skip news to high rated stocks in the portfolio if they are very uninteresting. If there was a super high rated news that could have the same impact as a super high relative/absolute change and then be moved up in the stock-importance ranking to also be included, even if it is a small position and did not result in a big stock price movement.

**Link to initial planning graphic: https://www.tldraw.com/r/JIU5_7VkrNGpppUTAQ3zZ?v=513,-334,2891,1534&p=cKpqfxg5UOTlYZl5uGs53**