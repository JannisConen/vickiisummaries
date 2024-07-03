import re

## strip all html tags
def strip_html_tags(text: str) -> str:
    return re.sub('<[^<]+?>', '', text)