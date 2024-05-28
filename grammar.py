import re
import random

class Grammar:
    start_symbols = {}
    terminal_symbols = {}
    nonterminal_symbols = {}
    file_path = 'grammar.gr'
    def __init__ (self,file_path):
        self.file_path = file_path

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
                            self.nonterminal_symbols[key] = value
                    #print(f"BLOCK ===\n{block_str}\n===\n\n")
                i += 1


    def find_nonterminal(self, sex, race):
        key = f"<nter_{sex}_{race}_name>"
        if key in self.nonterminal_symbols:
            print(f"Nonterminal for sex={sex} and race={race}: {self.nonterminal_symbols[key]}")
            return self.nonterminal_symbols[key]
        else:
            print(f"No nonterminal found for sex={sex} and race={race}")
            return None

    def expand_nonterminal(self, definition):
        while re.search(r'<(nter|ter)_.*?>', definition):
            definition = re.sub(
                r'<nter_.*?>',
                lambda match: self.nonterminal_symbols.get(match.group(0), match.group(0)),
                definition
            )
            print(definition)
            definition = re.sub(
                r'<ter_.*?>',
                lambda match: random.choice(self.terminal_symbols.get(match.group(0), [match.group(0)])),
                definition
            )
            print(definition)
        #print (f"\nExpanded name\n{definition}")
        return definition




#a = Grammar("grammar.gr")
#a.parseGrammar()
#print(f"START SYMBOLS ===\n{a.start_symbols}\n===\n\n")
#print(f"NONTERMINAL SYMBOLS ===\n{a.nonterminal_symbols}\n===\n\n")
#print(f"TERMINAL SYMBOLS ===\n{a.terminal_symbols}\n===\n\n")
#non_terminal = a.find_nonterminal('male','dunmer')
#name = a.expand_nonterminal(non_terminal)
#print(f"NAME : {name}")

