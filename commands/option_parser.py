class InvalidOptionValueError(Exception):
    pass

def parse_command_options(command: str, options_table: list):
    # Split the command to separate the options and the list
    parts = command.split()
    if len(parts) < 2:
        raise ValueError("Command must include a command name and arguments.")

    # Initialize the dictionary with default values
    options = {opt[0][0]: opt[2][0] for opt in options_table}

    # Extract and validate options
    for part in parts[1:]:
        if '=' in part:
            option, value = part.split('=')
            matching_options = [opt for opt in options_table if opt[0][0] == option]
            if matching_options:
                valid_values = matching_options[0][1]
                if valid_values == [42] or value in valid_values: # 42 = any value, because 42 is the answer to any question in the universe
                    options[option] = value
                else:
                    options[option] = matching_options[0][2][0]
                    raise InvalidOptionValueError(f"Invalid value for {option}: {value}. Using default: {options[option]}")
            else:
                raise ValueError(f"Unknown option: {option}")

    # Return the options dictionary
    return options
