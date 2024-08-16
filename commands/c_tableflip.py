import py_stuff.animate_cli as a_cli
import py_stuff.send_wrapper as sw

man_description = str(
    "**$tableflip Command**\n"
    "Usage: `$tableflip`\n"
    "Description: Table flip animation"
)

frames = str(
    
    '(ヘ°-°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ°-°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ°□°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ°□°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ°-°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ°-°)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(ヘ‵□′)ヘ ┬─┬ \xa0'
    '\n#!\n'
    '(╯‵□′）╯\xa0︵ ┻━┻' 
    '\n#!\n'
    '╯‵□′）╯\xa0－－┻━┻'
    '\n#!\n'
    '‵□′）╯－－－┻━┻'
    '\n#!\n'
    '-°）╯－－－－┻━┻'
    '\n#!\n'
    '°）╯－－－－┻━┻'
    '\n#!\n'
    '）╯－－－－┻━┻'
    '\n#!\n'
    '╯－－－－┻━┻'
    '\n#!\n'
    '－－－－┻━┻'
    '\n#!\n'
    '－－－┻━┻ \xa0 \xa0˦'
    '\n#!\n'
    '－－┻━┻ \xa0 \xa0˦\xa0'
    '\n#!\n'
    '\xa0\xa0\xa0－┻━┻ \xa0\xa0 ˦ \xa0'
    '\n#!\n'
    '\xa0\xa0\xa0\xa0－┻━┻ \xa0 ˦ \xa0'
    '\n#!\n'
    '\xa0\xa0\xa0\xa0\xa0\xa0 ┻━┻ ˦ \xa0'
    '\n#!\n'
    '\xa0\xa0\xa0\xa0\xa0 ┻ ━┻ ˦ \xa0'
    '\n#!\n'
    '\xa0\xa0\xa0\xa0\xa0 ┻ ━┻ ˦ \xa0'
    '\n#!\n'
    '\xa0\xa0\xa0\xa0\xa0 ┻ ━┻ ˦ \xa0'
    '\n#!\n'
    '）\xa0\xa0\xa0\xa0 ┻ ━┻ ˦ \xa0'
    '\n#!\n'
    'ಥ）\xa0\xa0\xa0 ┻ ━┻ ˦'
    '\n#!\n'
    '-ಥ）\xa0\xa0 ┻ ━┻ ˦'
    '\n#!\n'
    'ಥ-ಥ）\xa0 ┻ ━┻ ˦ '
    '\n#!\n'
    '(ಥ-ಥ） ┻ ━┻ '
    '\n#!\n'
    '(ಥ-ಥ） ┻ ━┻ '
)

async def run(message):
    await a_cli.animate(message,frames,500,1)
    await sw.wrapperSend(message, "Table flip animation completed!")
    return