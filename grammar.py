import re
import random

class Grammar:
    start_symbols = {}
    terminal_symbols = {}
    nonterminal_symbols = {}
    
    def __init__ (self, file_path):
        self.file_path = file_path
        print(f"Grammar initialized with file '{file_path}'")

    def parseGrammar(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if re.match(r'^<start_.*>', line) or re.match(r'^<ter_.*>', line) or re.match(r'^<nter_.*>', line):
                    block = [line]
                    if not line.endswith(';'):
                        i += 1
                        while i < len(lines) and not lines[i].strip().endswith(';'):
                            block.append(lines[i].strip())
                            i += 1
                        if i < len(lines):  # append the line that ends with ';'
                            block.append(lines[i].strip())
                    # Parse the block into key and values
                    block_str = '\n'.join(block)
                    if '::=' in block_str:
                        key, value = block_str.split('::=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key.startswith('<start_'):
                            value = value.rstrip(';')
                            self.start_symbols[key] = value
                        elif key.startswith('<ter_'):
                            # Remove the ending semicolon
                            value = value.rstrip(';')
                            # Split the value by '|'
                            value_list = [part.strip().strip('"') for part in value.split('|')]
                            self.terminal_symbols[key] = value_list
                        elif key.startswith('<nter_'):
                            value = value.rstrip(';')
                            # Split the value by '|'
                            value_list = [part.strip() for part in value.split('|')]
                            self.nonterminal_symbols[key] = value_list
                i += 1

    def find_nonterminal(self, sex, race):
        key = f"<nter_{sex}_{race}_name>"
        if key in self.nonterminal_symbols:
            print(f"Nonterminal for sex={sex} and race={race}: {self.nonterminal_symbols[key]}")
            return random.choice(self.nonterminal_symbols[key])
        else:
            print(f"No nonterminal found for sex={sex} and race={race}")
            return None

    def expand_nonterminal(self, definition):
        while re.search(r'<(nter|ter)_.*?>', definition):
            definition = re.sub(
                r'<nter_.*?>',
                lambda match: random.choice(self.nonterminal_symbols.get(match.group(0), [match.group(0)])),
                definition
            )
            print(definition)
            definition = re.sub(
                r'<ter_.*?>',
                lambda match: random.choice(self.terminal_symbols.get(match.group(0), [match.group(0)])),
                definition
            )
            print(definition)
        return definition

    def generate_name(self, sex, race):
        nonterminal_key = f"<nter_{sex}_{race}_name>"
        if nonterminal_key not in self.nonterminal_symbols:
            return f"No name pattern found for sex={sex} and race={race}"
        
        start_key = f"<start_{sex}_{race}_name>"
        if start_key in self.start_symbols:
            start_value = self.start_symbols[start_key]
        else:
            start_value = ""
        
        nonterminal_value = random.choice(self.nonterminal_symbols[nonterminal_key])
        expanded_nonterminal = self.expand_nonterminal(nonterminal_value)
        
        name = f"{start_value} {expanded_nonterminal}".strip()
        return name