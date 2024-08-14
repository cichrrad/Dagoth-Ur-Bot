import commands.animate_cli as a_cli
import commands.send_wrapper as sw

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
    await a_cli.animate(message,frames,250,5)
    await sw.wrapperSend(message, "Pendulum animation completed!")
    return