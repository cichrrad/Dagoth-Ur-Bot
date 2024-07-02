import py_stuff.image_transform as it
import commands.send_wrapper as sw


man_description = str(
    "Demo showcase of color output. Work in progress.\nWhy? Because discord ansi thingamajig is the most disgusting thing ever.\nTo print a colored line of 60 characters, you actually need ~10-15x more.\nPlus you only really get 8 colors"
)

async def run(message):
    ansi_bs = str(
        "```ansi\n"
        "\u001b[0;30mGray\u001b[0;0m\n"
        "\u001b[0;31mRed\u001b[0;0m\n"
        "\u001b[0;32mGreen\u001b[0;0m\n"
        "\u001b[0;33mYellow\u001b[0;0m\n"
        "\u001b[0;34mBlue\u001b[0;0m\n"
        "\u001b[0;35mPink\u001b[0;0m\n"
        "\u001b[0;36mCyan\u001b[0;0m\n"
        "\u001b[0;37mWhite\u001b[0;0m\n"
        "\u001b[0;40mFirefly dark blue background\u001b[0;0m\n"
        "\u001b[0;41mOrange background\u001b[0;0m\n"
        "\u001b[0;42mMarble blue background\u001b[0;0m\n"
        "\u001b[0;43mGreyish turquoise background\u001b[0;0m\n"
        "\u001b[0;44mGray background\u001b[0;0m\n"
        "\u001b[0;45mIndigo background\u001b[0;0m\n"
        "\u001b[0;46mLight gray background\u001b[0;0m\n"
        "\u001b[0;47mWhite background\u001b[0;0m\n\n"
        "\u001b[0;40;30mExample\u001b[0;0m \u001b[0;40;31mExample\u001b[0;0m \u001b[0;40;32mExample\u001b[0;0m \u001b[0;40;33mExample\u001b[0;0m \u001b[0;40;34mExample\u001b[0;0m \u001b[0;40;35mExample\u001b[0;0m \u001b[0;40;36mExample\u001b[0;0m \u001b[0;40;37mExample\u001b[0;0m\n"
        "\u001b[0;41;30mExample\u001b[0;0m \u001b[0;41;31mExample\u001b[0;0m \u001b[0;41;32mExample\u001b[0;0m \u001b[0;41;33mExample\u001b[0;0m \u001b[0;41;34mExample\u001b[0;0m \u001b[0;41;35mExample\u001b[0;0m \u001b[0;41;36mExample\u001b[0;0m \u001b[0;41;37mExample\u001b[0;0m\n"
        "\u001b[0;42;30mExample\u001b[0;0m \u001b[0;42;31mExample\u001b[0;0m \u001b[0;42;32mExample\u001b[0;0m \u001b[0;42;33mExample\u001b[0;0m \u001b[0;42;34mExample\u001b[0;0m \u001b[0;42;35mExample\u001b[0;0m \u001b[0;42;36mExample\u001b[0;0m \u001b[0;42;37mExample\u001b[0;0m\n"
        "\u001b[0;43;30mExample\u001b[0;0m \u001b[0;43;31mExample\u001b[0;0m \u001b[0;43;32mExample\u001b[0;0m \u001b[0;43;33mExample\u001b[0;0m \u001b[0;43;34mExample\u001b[0;0m \u001b[0;43;35mExample\u001b[0;0m \u001b[0;43;36mExample\u001b[0;0m \u001b[0;43;37mExample\u001b[0;0m\n"
        "\u001b[0;44;30mExample\u001b[0;0m \u001b[0;44;31mExample\u001b[0;0m \u001b[0;44;32mExample\u001b[0;0m \u001b[0;44;33mExample\u001b[0;0m \u001b[0;44;34mExample\u001b[0;0m \u001b[0;44;35mExample\u001b[0;0m \u001b[0;44;36mExample\u001b[0;0m \u001b[0;44;37mExample\u001b[0;0m\n"
        "\u001b[0;45;30mExample\u001b[0;0m \u001b[0;45;31mExample\u001b[0;0m \u001b[0;45;32mExample\u001b[0;0m \u001b[0;45;33mExample\u001b[0;0m \u001b[0;45;34mExample\u001b[0;0m \u001b[0;45;35mExample\u001b[0;0m \u001b[0;45;36mExample\u001b[0;0m \u001b[0;45;37mExample\u001b[0;0m\n"
        "\u001b[0;46;30mExample\u001b[0;0m \u001b[0;46;31mExample\u001b[0;0m \u001b[0;46;32mExample\u001b[0;0m \u001b[0;46;33mExample\u001b[0;0m \u001b[0;46;34mExample\u001b[0;0m \u001b[0;46;35mExample\u001b[0;0m \u001b[0;46;36mExample\u001b[0;0m \u001b[0;46;37mExample\u001b[0;0m\n"
        "\u001b[0;47;30mExample\u001b[0;0m \u001b[0;47;31mExample\u001b[0;0m \u001b[0;47;32mExample\u001b[0;0m \u001b[0;47;33mExample\u001b[0;0m \u001b[0;47;34mExample\u001b[0;0m \u001b[0;47;35mExample\u001b[0;0m \u001b[0;47;36mExample\u001b[0;0m \u001b[0;47;37mExample\u001b[0;0m\n"
        "```"
        )
    await message.channel.send(ansi_bs)
    input_image_path = './py_stuff/mario-hero.png'
    target_width = 60 # Set target width for the ASCII art

    converted_image = it.resize_and_convert_image_with_custom_palette(input_image_path, target_width, it.custom_palette)
    ascii_art = it.generate_ascii_art(converted_image, it.custom_palette, it.ansi_colors, it.ansi_reset)
    print (ascii_art)
    await sw.wrapperSend_force_newline(message, ascii_art,'ansi')