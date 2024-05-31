import heapq
from collections import defaultdict, namedtuple

class HuffmanNode:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def print_huffman_codes(root, code, huffman_code_map):
    if not root:
        return
    if root.character != '#':
        #print(f"{root.character}: {code}")
        huffman_code_map[root.character] = code
    print_huffman_codes(root.left, code + "0", huffman_code_map)
    print_huffman_codes(root.right, code + "1", huffman_code_map)

def generate_huffman_tree_string(root, prefix="", is_left=True):
    if not root:
        return ""
    result = []
    result.append(prefix)
    result.append("├──" if is_left else "└──")
    if root.character != '#':
        result.append(f"'{root.character}' ({root.frequency})\n")
    else:
        result.append(f"# ({root.frequency})\n")
    result.append(generate_huffman_tree_string(root.left, prefix + ("│   " if is_left else "    "), True))
    result.append(generate_huffman_tree_string(root.right, prefix + ("│   " if is_left else "    "), False))
    return "".join(result)
