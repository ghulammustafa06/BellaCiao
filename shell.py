# ------------------- shell.py -------------------

from lang import lex, Parser, Interpreter

def repl():
    print("BellaCiao Programming Language - 'La Casa de Papel' Edition")
    print("Type 'exit' to quit, 'help' for commands, or start planning your heist!")
    interpreter = Interpreter()
    
    while True:
        try:
            code = input('>>> ')
            if code.lower() == 'exit':
                print("Ciao! The heist is over.")
                break
            elif code.lower() == 'help':
                show_help()
            elif code.lower() == 'clear':
                interpreter = Interpreter()  # Reset the interpreter
                print("Workspace cleared. Start a new heist!")
            else:
                tokens = lex(code)
                parser = Parser(tokens)
                ast = parser.parse()
                result = interpreter.interpret(ast)
                if result:
                    for item in result:
                        if item is not None:
                            print(item)
        except Exception as e:
            print(f"Error: {e}")

def show_help():
    print("\nBellaCiao Language Commands:")
    print("  exit          - Exit the BellaCiao shell")
    print("  help          - Show this help message")
    print("  clear         - Clear the current workspace")
    print("\nBuilt-in Functions:")
    print("  bella_ciao    - Print the heist anthem")
    print("  professor     - Get info about the heist mastermind")
    print("  random_codename - Get a random city codename")
    print("  vault_code    - Generate a random vault code")
    print("  police_response_time - Get estimated police response time")
    print("  hostage_count - Get a random number of hostages")
    print("  security_guards - Get a random number of security guards")
    print("  money_printer_status - Check the status of the money printer")
    print("  escape_route  - Get a random escape route")
    print("  hacker_status - Check the status of the hacking operation")
    print("  police_negotiator - Get the name of the police negotiator")
    print("  time_remaining - Get the remaining time for the heist")
    print("\nExample:")
    print('  heist royal_mint plan')
    print('    print "Team leader:";')
    print('    print professor;')
    print('    print "Escape route:";')
    print('    print escape_route;')
    print('  end;')
    print('  execute royal_mint;')
    print()

if __name__ == "__main__":
    repl()