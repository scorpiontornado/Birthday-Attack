# Birthday attack script to find variants of two given files that have the same hash (to a certain number of characters from the end)
#
# Appends 0 or 1 spaces on the end of each line for both files, trying every combination until a
# collision with any previously calculated files are found. In this way, each line becomes a "bit",
# meaning that the possible number of combinations is 2^(num_lines).
# This approach looks more natural (visually) than appending spaces to the end of the whole file
#
# Usage: python3 line_spaces_mvp.py <real_file> <fake_file> <num_chars>

# TODO - what if files already have line with a space at the end? Might look unnatural to have 2 spaces
# Also, this is either having 0 or X spaces, where X is a positive integer. Would be better if we
# could mix the number of spaces in the file - e.g. having 0, 1, 2, 3 spaces in the file (would mean
# the num spaces per line is reduced)

import sys
from hashlib import sha256
# import pprint  #! Testing

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <real_file> <fake_file> <num_chars>")
    exit(1)

# num_chars is the number of characters at the end of each hash that must be the
# same to be considered a collision
real_file = sys.argv[1]
fake_file = sys.argv[2]
num_chars = int(sys.argv[3])

# print(real_file, fake_file, num_chars)

# Read in the input files as lists of lines
with open(real_file) as file:
    real_og = (
        file.read().splitlines()
    )  # TODO fix issue with this containing the newlines. Might have to .read().splitlines()
    real_modified = real_og.copy()
    num_real_lines = len(real_og)
    real_combs = (
        2**num_real_lines
    )  # Number of unique integers that can be represented with num_real_lines bits
with open(fake_file) as file:
    fake_og = file.read().splitlines()
    fake_modified = fake_og.copy()
    num_fake_lines = len(fake_og)
    fake_combs = (
        2**num_fake_lines
    )  # Number of unique integers that can be represented with num_fake_lines bits

# # TODO remove - testing
# pp = pprint.PrettyPrinter()
# for item in [real_og, real_modified, fake_og, fake_modified]:
#     pp.pprint(item)
#     print()

# We want to store all the hashes we've calculated so far. If we find a collision, we can quickly look up the corresponding text value that produced it
# In Python, dictionaries are implemented as hash tables, so lookups are O(1) on average
all_real_hashes = {}
all_fake_hashes = {}
i = 0

# Keep looping while real and fake have different hashes (to a certain number of characters from the end)
while True:
    real_hash = sha256("\n".join(real_modified).encode()).hexdigest()[-num_chars:]
    fake_hash = sha256("\n".join(fake_modified).encode()).hexdigest()[-num_chars:]

    # We want to store calculated hashes to save time in the future. As, for each iteration, there are
    # more and more possible fake_hash values, the likelihood of a collision with a real_hash value increases.
    # This is why it takes the square root of the time taken to bruteforce all combinations on average,
    # i.e. half the bits of security (way better than a second-preimage attack where you only modify one file at once)

    all_real_hashes[real_hash] = real_modified
    all_fake_hashes[fake_hash] = fake_modified

    # If we find a collision, we can stop
    if real_hash in all_fake_hashes or fake_hash in all_real_hashes:
        hash = real_hash if real_hash in all_fake_hashes else fake_hash
        print(
            f"Collision found! {real_file}.out and {fake_file}.out have the same hash: {hash}"
        )

        with open(f"{real_file}.out", "w") as file:
            file.writelines("\n".join(all_real_hashes[hash]))
        with open(f"{fake_file}.out", "w") as file:
            file.writelines("\n".join(all_fake_hashes[hash]))

        break

    # Otherwise, pad both files with spaces on various lines and try again
    # E.g. if i = 0b1101, then we add spaces to lines 0, 2, 3
    # The number of spaces added to each line is the same for each line, and increases by 1 each
    # time we run out of combinations (i.e., exceed the limit the binary can represent)

    # Bitmasks representing which lines to add (i // real_combs) spaces to
    # Note - have to store in an array 
    real_mask = i % real_combs
    fake_mask = i % fake_combs
    
    # TODO remove - debugging
    # print(i)
    # print("\t", real_mask, bin(real_mask), real_combs, i // real_combs + 1)
    # print("\t", fake_mask, bin(fake_mask), fake_combs, i // fake_combs + 1)

    # (Could this be optimised? e.g. only modify the relevant lines)
    real_modified = [
        line
        + " "
        * ((real_mask >> j) & 1)  # Extract the jth bit (0-indexed from right)
        * (
            i // real_combs + 1
        )  # Num spaces is either 0, or one more than the number of times we've run out of combinations
        for j, line in enumerate(real_og)
    ]
    fake_modified = [
        line
        + " "
        * ((fake_mask >> j) & 1)  # Extract the jth bit (0-indexed from right)
        * (
            i // fake_combs + 1
        )  # Num spaces is either 0, or one more than the number of times we've run out of combinations
        for j, line in enumerate(fake_og)
    ]
    i += 1
