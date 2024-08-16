from gnews import GNews
import py_stuff.send_wrapper as sw

man_description = str(
    "**$news Command**\n"
    "Usage: `$news`\n"
    "Description: Provides the latest news articles headlines scraped from google news.\n"
)


async def run(message):
    g = GNews()
    g.exclude_websites = ['yahoo.com', 'cnn.com']
    g.max_results = 5
    news = g.get_top_news()
    text = ''
    for article in news:
        text += f'```\n{article["title"]}\n\nDate: {article["published date"]}\n```\nLink: <{article["url"]}>\n\n'
    await sw.wrapperSend(message, text) 