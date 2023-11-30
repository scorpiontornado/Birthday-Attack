# Birthday attack script to find variants of two given files that have the same hash (to a certain number of characters from the end)
#
# Appends 0 or 1 spaces on the end of each line for both files, trying every combination until a
# collision with any previously calculated files are found. In this way, each line becomes a "bit",
# meaning that the possible number of combinations is 2^(num_lines).
# This approach looks more natural (visually) than appending spaces to the end of the whole file
#
# Usage: python3 line_spaces_mvp.py <real_file> <fake_file> <num_chars>

# TODO - what if files already have line with a space at the end? Might look unnatural to have 2 spaces
# Also, what if we run out of combinations? Might have to double-up on some lines (add 2, 3 spaces)

import sys
from hashlib import sha256
import pprint  #! Testing

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
        file.readlines()
    )  # TODO fix issue with this containing the newlines. Might have to .read().splitlines()
    real_modified = real_og.copy()
with open(fake_file) as file:
    fake_og = file.readlines()
    fake_modified = fake_og.copy()

# TODO remove - testing
pp = pprint.PrettyPrinter()
for item in [real_og, real_modified, fake_og, fake_modified]:
    pp.pprint(item)
    print()

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
        print(
            f"Collision found! {real_file}.out and {fake_file}.out have the same hash: {real_hash}"
        )

        with open(f"{real_file}.out", "w") as file:
            file.writelines(all_real_hashes[real_hash])
        with open(f"{fake_file}.out", "w") as file:
            file.writelines(all_fake_hashes[fake_hash])

        break

    # Otherwise, pad both files with spaces on various lines and try again
    # E.g. if i = 0b1101, then we add spaces to lines 0, 2, 3

    # (Could this be optimised?)
    real_modified = [
        line
        + " "
        * (
            (i >> j) & 1
        )  # Extract the jth bit (0-indexed from right), and add that many spaces (0 or 1)
        for j, line in enumerate(real_modified.copy())
    ]
    fake_modified = [
        line
        + " "
        * (
            (i >> j) & 1
        )  # Extract the jth bit (0-indexed from right), and add that many spaces (0 or 1)
        for j, line in enumerate(fake_modified.copy())
    ]
    i += 1
