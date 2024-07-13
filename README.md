# BellaCiao Programming Language </>

## Introduction

BellaCiao is a programming language themed around the popular TV series "Money Heist" (La Casa de Papel). It allows users to plan and execute virtual heists using a simple, intuitive syntax, combined with thematic built-in functions.

## Features

- Custom syntax inspired by heist planning
- Conditional statements (if-else)
- Loops (while)
- Variables and basic arithmetic operations
- Print statements
- Heist planning and execution commands
- Money Heist themed built-in functions

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Clone this repository or download the `lang.py` and `shell.py` files.

## Usage

To start the BellaCiao shell, run:
```bash
python shell.py
```
This will open an interactive shell where you can write and execute BellaCiao code.

## Syntax and Commands

### Basic Syntax

- Statements end with a semicolon (`;`)
- Code blocks are enclosed in curly braces (`{}`)
- Variables are assigned using the equals sign (`=`)

### Control Structures

#### If-Else Statement
```plaintext
if condition {
    // code block
} else {
    // code block
}
```

#### While Loop
```plaintext
while condition {
    // code block
}
```


### Heist Execution
To execute a planned heist:
```plaintext
execute heist_name;
```

### Built-in Functions

- `bella_ciao`: Returns the heist anthem
- `professor`: Returns info about the heist mastermind
- `random_codename`: Generates a random city codename
- `vault_code`: Generates a random vault code
- `police_response_time`: Estimates police response time
- `hostage_count`: Generates a random number of hostages
- `security_guards`: Generates a random number of security guards
- `money_printer_status`: Checks the status of the money printer
- `escape_route`: Suggests a random escape route
- `hacker_status`: Checks the status of the hacking operation
- `police_negotiator`: Provides the name of the police negotiator
- `time_remaining`: Gives the remaining time for the heist

## Example

Here's a simple heist plan using BellaCiao:
```plaintext
heist royal_mint plan
print "Team leader:";
print professor;

print "Codename for this mission:";
print random_codename;

print "Vault code to crack:";
code = vault_code;
print code;

if code > 5000 {
    print "High security! Be cautious.";
} else {
    print "Standard security. Proceed as planned.";
}

print "Escape route:";
print escape_route;

end;
execute royal_mint;
```

## Shell Commands

- `exit`: Quit the BellaCiao shell
- `help`: Display help information
- `clear`: Clear the current workspace and start a new plan

## Contributing

Contributions to BellaCiao are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

## License

This project is open source and available under the [MIT License](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt).

## Disclaimer

BellaCiao is a fictional programming language created for educational and entertainment purposes. 
