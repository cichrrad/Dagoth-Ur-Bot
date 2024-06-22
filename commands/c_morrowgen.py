import py_stuff.grammar as gr
import random

import commands.send_wrapper as sw

man_description = str(
    "**$morrowgen Command**\n"
    "Usage: `$morrowgen <race> <sex>`\n"
    "Description: Generates a random character for the game Morrowind with various attributes and skills. If no race and/or sex is specified, random one(s) will be chosen.\n"
    "Example:\n"
    "```\n"
    "$morrowgen Dunmer Male\n"
    "```\n"
    "This command will generate a random male Dunmer male character."
)


async def run(message):
    specialization_list = ["Combat", "Magic", "Stealth"]
    favored_attributes_list = ["Strength", "Intelligence", "Willpower", "Agility", "Speed", "Endurance", "Personality", "Luck"]
    birthsign_list = ["The Apprentice", "The Atronach", "The Lady", "The Lord", "The Lover", "The Mage", "The Ritual", "The Serpent", "The Shadow", "The Steed", "The Thief", "The Tower", "The Warrior"]
    skills_list = ["Alchemy", "Alteration", "Armorer", "Athletics", "Axe", "Block", "Blunt Weapon", "Conjuration", "Destruction", "Enchant", "Hand-to-hand", "Heavy Armor", "Illusion", "Light Armor", "Long Blade", "Marksman", "Medium Armor", "Mercantile", "Mysticism", "Restoration", "Security", "Short Blade", "Sneak", "Spear", "Speechcraft", "Unarmored"]
    
    chosen_specialization = random.choice(specialization_list)
    
    # Choose 2 favored attributes (cannot choose the same twice)
    chosen_favored_attributes = random.sample(favored_attributes_list, 2)

    # Choose 5 major skills and 5 minor skills (no duplicates)
    chosen_skills = random.sample(skills_list, 10)
    chosen_major_skills = chosen_skills[:5]
    chosen_minor_skills = chosen_skills[5:]

    # Choose 1 birthsign
    chosen_birthsign = random.choice(birthsign_list)

    #define viable races
    race_list = ["Argonian", "Breton", "Dunmer", "Altmer", "Imperial", "Khajiit", "Nord", "Orc", "Redguard", "Bosmer"]
    #define viable sex
    sex_list = ["Male", "Female"]

    #parse commands
    args = message.content.split(" ")
    #first one is command, seconnd and third are arguments (if they were provided), anything beyond we ignore
    if len(args) >= 2:
        if (args[1].capitalize()) in race_list:
            chosen_race = args[1].capitalize()
        else:
            #random
            await message.channel.send(f"Cant recognize \'{args[1]}\' as a race. Choosing race at random")
            chosen_race = random.choice(race_list)

        if len(args) >= 3:
            if (args[2].capitalize()) in sex_list:
                chosen_sex = args[2].capitalize()
            else:
                #random
                await message.channel.send(f"Cant recognize \'{args[2]}\' as a sex. Choosing sex at random")
                chosen_sex = random.choice(sex_list)
        else:
            #random
            chosen_sex = random.choice(sex_list)
    else:
        #random
        chosen_race = random.choice(race_list)
        chosen_sex = random.choice(sex_list)

    g = gr.Grammar('py_stuff/grammar.gr')
    g.parseGrammar()
    chosen_name = 'none'
    if chosen_race == 'Dunmer':
        #sometimes take ashlander name
        if random.choice([True, False]):
            chosen_race = "Dunmer - Ashlander"
            chosen_name = g.generate_name(chosen_sex.lower(),'ashlander')
        else:
            chosen_name = g.generate_name(chosen_sex.lower(),chosen_race.lower())
    else:
        chosen_name = g.generate_name(chosen_sex.lower(),chosen_race.lower())

    out = f"Name: {chosen_name}\n\n"
    out = out + f"Race: {chosen_race}\n\n"
    out = out + f"Sex: {chosen_sex}\n\n"
    out = out + f"Birthsign: {chosen_birthsign}\n\n"
    out = out + f"Specialization: {chosen_specialization}\n\n"
    out = out + f"Favored Attributes: {chosen_favored_attributes}\n\n"
    out = out + f"Major Skills: {chosen_major_skills}\n\n"
    out = out + f"Minor Skills: {chosen_minor_skills}"

    await sw.wrapperSend(message,out,'mono')