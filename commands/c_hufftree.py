
import heapq
from collections import defaultdict
import py_stuff.huffman as hf
import commands.send_wrapper as sw

man_description = str(
    "**$hufftree Command**\n"
    "Usage: `$hufftree <text>`\n"
    "Description: Prints the huffman tree for the specified text. Should not contain '#'.\n"
    "Example:\n"
    "```\n"
    "$hufftree hello world\n"
    "```\n"
    "The bot will respond with the huffman tree for the specified text."
)

async def run(message):
    contents = message.content
    default = 'hello world'
    args = contents.split(' ',1)
    if len(args) > 1:
        text = args[1].strip()
    else:
        text = default

    frequency_map = defaultdict(int)
    for c in text:
        frequency_map[c] += 1

    pq = []
    for character, frequency in frequency_map.items():
        heapq.heappush(pq, hf.HuffmanNode(character, frequency))

    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        combined_node = hf.HuffmanNode('#', left.frequency + right.frequency)
        combined_node.left = left
        combined_node.right = right
        heapq.heappush(pq, combined_node)

    root = heapq.heappop(pq)
    tree = hf.generate_huffman_tree_string(root)
    await sw.wrapperSend(message,tree,'mono')