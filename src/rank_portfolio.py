from typing import List
from src.models import PortfolioEntry
import os
import json
import logging

def rank_portfolio(portfolio: List[PortfolioEntry]) -> List[PortfolioEntry]:
    """
    Ranks portfolio entries based on impact on total portfolio value and relative changes.
    
    Entries with absolute changes contributing to more than 5% of the total portfolio value
    are prioritized, sorted by absolute change. Next, entries with relative changes greater
    than 5% are sorted by absolute change. Finally, the remaining entries are sorted by 
    absolute change.
    """
    # Calculate the total portfolio value
    total_portfolio_value = sum(entry.absolute_value for entry in portfolio)

    high_impact_entries = []
    significant_relative_change_entries = []
    remaining_entries = []

    # Categorize entries in a single pass
    for entry in portfolio:
        abs_change_percentage = abs(entry.absolute_change) / total_portfolio_value

        if abs_change_percentage > 0.05:
            high_impact_entries.append(entry)
        elif entry.change > 5:
            significant_relative_change_entries.append(entry)
        else:
            remaining_entries.append(entry)

    # Sort the entries by absolute change in descending order for all categories
    high_impact_entries.sort(key=lambda x: abs(x.absolute_change), reverse=True)
    significant_relative_change_entries.sort(key=lambda x: abs(x.absolute_change), reverse=True)
    remaining_entries.sort(key=lambda x: abs(x.absolute_change), reverse=True)
    
    logging.info("HIGH IMPACT ENTRIES:", high_impact_entries)
    logging.info("SIGNIFICANT RELATIVE CHANGE ENTRIES:", significant_relative_change_entries)
    logging.info("REMAINING ENTRIES:", remaining_entries)

    # Combine all lists into the final sorted list
    return high_impact_entries + significant_relative_change_entries + remaining_entries

# just for testing
if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "src", "data", "portfolio.json")
    
    with open(path, "r") as file:
        portfolio_items = json.load(file)
        portfolio = [PortfolioEntry(**item) for item in portfolio_items]
        
    print("PORTFOLIO:", portfolio)
    ranked_portfolio = rank_portfolio(portfolio)
    print(ranked_portfolio)