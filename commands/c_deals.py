import requests
from bs4 import BeautifulSoup
import commands.send_wrapper as sw
man_description=str(
    "**$deals Command**\n"
    "Usage: `$deals <number>`\n"
    "Description: Sends a summary of the top <number> deals on games scraped from gg.deals.\n"
    "Example:\n"
    "```\n"
    "$deals 5\n"
    "```\n"
)

async def run(message):
    contents = message.content
    args = contents.split(' ',1);
    default = 5

    # argument was provided
    if len(args) >1:
        try:
            number_of_games = int(args[1].strip())
        except ValueError:
            await message.channel.send(f"Invalid input for 'number': {contents.split(' ',1)[1]}. Using default = {default}")
            number_of_games = default

        if number_of_games < 1:
            await message.channel.send(f"Invalid input for 'number': {number_of_games}. Using default = {default}.")
            number_of_games = default
    # no argument
    else:
        number_of_games = default

    await message.channel.send(f"Top {number_of_games} deals (fetched from gg.deals):")
    text = _fetch_deals(number_of_games)
    await sw.wrapperSend(message,text,'normal')
    return

def _fetch_deals(number_of_games=5):
    # URL of the page to scrape
    url = "https://gg.deals/deals/"

    # Send a request to fetch the page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with id="deals-list"
        deals_list_div = soup.find('div', id='deals-list')
        
        if deals_list_div:
            # Find all game items within the div
            game_items = deals_list_div.find_all('div', class_='game-list-item', limit=number_of_games)
            
            games = []
            
            for item in game_items:
                game_info = item.find('a', class_='game-info-title')
                store_link = item.find('a', class_='d-flex flex-align-center flex-justify-center label-with-arrows action-btn-full-box action-btn cta-label-desktop with-arrows action-ext')
                if game_info:

                    game_name = game_info.get('data-title-auto-hide', 'No title')
                    game_link = game_info.get('href', 'No link')
                    store_link = store_link.get('href', 'No link')
                    full_link = f"https://gg.deals{game_link}"
                    
                    price_span = item.find('span', class_='price-inner game-price-new')
                    game_price = price_span.text.strip() if price_span else 'No price'
                    
                    games.append({
                        'name': game_name,
                        'link': full_link,
                        'store_link': store_link,
                        'price': game_price
                    })
            
            # Format the output for a Discord message
            message = ""
            for i, game in enumerate(games, start=1):
                message += f"**Game {i}:**\n"
                message += f"**Name:** {game['name']}\n"
                #message += f"**Link:** {game['link']}\n"
                message += f"**Store Link:** <https://gg.deals{game['store_link']}>\n"
                message += f"**Price:** {game['price']}\n\n"
            
            return message
        else:
            return "Div with id 'deals-list' not found."
    else:
        return f"Failed to fetch the page. Status code: {response.status_code}"

