import py_stuff.animate_cli as a_cli
import py_stuff.send_wrapper as sw

man_description = str(
    "**$pendulum Command**\n"
    "Usage: `$pendulum`\n"
    "Description: Pendulum animation"
)

frames =str(
"╔════╤╤╤╤════╗\n" 
"║    │││ \\   ║\n" 
"║    │││  O  ║\n" 
"║    OOO     ║\n"
"\n#!\n"
"╔════╤╤╤╤════╗\n" 
"║    │││|    ║\n" 
"║    │││|    ║\n" 
"║    OOOO    ║\n"
"\n#!\n"
"╔════╤╤╤╤════╗\n" 
"║   / ││|    ║\n" 
"║  O  ││|    ║\n" 
"║     OOO    ║\n"
"\n#!\n"
"╔════╤╤╤╤════╗\n" 
"║    │││|    ║\n" 
"║    │││|    ║\n" 
"║    OOOO    ║\n"
)

async def run(message):
    await a_cli.animate(message,frames,500,5)
    await sw.wrapperSend(message, "Pendulum animation completed!")
    return