import python_weather
import py_stuff.send_wrapper as sw

man_description = str(
    "**$weather Command**\n"
    "Usage: `$weather <location>`\n"
    "Description: Sends the current weather for the specified location.\n"
    "Example:\n"
    "```\n"
    "$weather New York\n"
    "```\n"
    "The bot will respond with the current weather for the specified location."
)

async def run(message):
    contents = message.content
    default = 'Prague'
    #split off the command - everything after the command is the location
    args = contents.split(' ',1);
    #if there is an argument
    if len(args) >1:
        place = args[1].strip()
    else:
        place=default
        await message.channel.send("No location provided. using default: " + default)
    
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(place)
        weather_string = f"\nWeather in {weather.location}:\n{weather.description}\nTemperature: {weather.temperature} Celsius (Feels like {weather.feels_like} Celsius)\nHumidity: {weather.humidity}%\nPressure: {weather.pressure}hPa\n"
        await sw.wrapperSend(message,weather_string,'mono')
    return