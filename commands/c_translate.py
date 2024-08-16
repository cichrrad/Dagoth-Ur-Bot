from translate import Translator as t
import py_stuff.send_wrapper as sw

# TODO maybe parse options to let the user specify input language ? autodetect seem to work though

man_description = str(
    "**$translate Command**\n"
    "Usage: `$translate <language> <text>`\n"
    "Description: Translates the text into the specified language. The <language> should be in an ISO 639-1 code format.\n"
    "Example:\n"
    "```\n"
    "$translate en Boa tarde amigos!\n"
    "```\n"
    "The bot will respond with 'Good afternoon friends!'."
)

async def run(message):
    contents = message.content
    #split off the command
    args = contents.split(' ',1)
    #if there is anything beside the command
    if len(args) > 1:
        #split off the language
        language, text = args[1].split(' ',1)
        
        #check for some common languages and fix their codes
        #if they are wrong
        if language.lower == 'eng' or language.lower == 'english':
            language = 'en'
        if language.lower == 'french':
            language = 'fr'
        if language.lower == 'spanish':
            language = 'es'
        #translate
        translator = t(from_lang='autodetect', to_lang=language)
        translation = translator.translate(text)
        if 'INVALID TARGET LANGUAGE' in translation:
            translation = f"Bad language code. See <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>\n" + man_description 
        #send
        await sw.wrapperSend(message, translation, 'normal')
    else:
        await message.channel.send(man_description)