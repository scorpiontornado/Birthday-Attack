# Birthday attack script to find variants of two given files that have the same hash (to a certain number of characters from the end)
# Appends spaces to the end of both files until a collision with any previously calculated files are found
#
# Usage: python3 trailing_spaces.py <real_file> <fake_file> <num_chars>
#
# Inspired by: https://github.com/YashDudam/birthday-attack/blob/main/birthday_attack.py
# Tried to code this myself though without looking, just had a quick skim for the gist & libraries to use

import sys
from hashlib import sha256

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <real_file> <fake_file> <num_chars>")
    exit(1)

# num_chars is the number of characters at the end of each hash that must be the
# same to be considered a collision
real_file = sys.argv[1]
fake_file = sys.argv[2]
num_chars = int(sys.argv[3])

# print(real_file, fake_file, num_chars)

# Read in the input files
with open(real_file) as file:
    real = file.read()
with open(fake_file) as file:
    fake = file.read()

# We want to store all the hashes we've calculated so far. If we find a collision, we can quickly look up the corresponding text value that produced it
# In Python, dictionaries are implemented as hash tables, so lookups are O(1) on average
all_real_hashes = {}
all_fake_hashes = {}

# Keep looping while real and fake have different hashes (to a certain number of characters from the end)
while True:
    real_hash = sha256(real.encode()).hexdigest()[-num_chars:]
    fake_hash = sha256(fake.encode()).hexdigest()[-num_chars:]

    # We want to store calculated hashes to save time in the future. As, for each iteration, there are
    # more and more possible fake_hash values, the likelihood of a collision with a real_hash value increases.
    # This is why it takes the square root of the time taken to bruteforce all combinations on average,
    # i.e. half the bits of security (way better than a second-preimage attack where you only modify one file at once)

    all_real_hashes[real_hash] = real
    all_fake_hashes[fake_hash] = fake

    # If we find a collision, we can stop
    #! Note - this should be way faster than their approach of making sets of keys & checking len(intersection)x
    if real_hash in all_fake_hashes or fake_hash in all_real_hashes:
        hash = real_hash if real_hash in all_fake_hashes else fake_hash
        print(
            f"Collision found! 'confession_real.txt.out' and 'confession_fake.txt.out' have the same hash: {hash}"
        )

        with open(f"{real_file}.out", "w") as file:
            file.write(all_real_hashes[hash])
        with open(f"{fake_file}.txt.out", "w") as file:
            file.write(all_fake_hashes[hash])

        break

    # Otherwise, pad both files with a space and try again
    real += " "
    fake += " "
