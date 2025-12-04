import itertools
import string
import os


def print_name():
    print("=" * 60)
    print("""
    ██████╗ ██╗ ██████╗ ███████╗███╗   ██╗
    ██╔══██╗██║██╔════╝ ██╔════╝████╗  ██║
    ██║  ██║██║██║  ███╗█████╗  ██╔██╗ ██║
    ██║  ██║██║██║   ██║██╔══╝  ██║╚██╗██║
    ██████╔╝██║╚██████╔╝███████╗██║ ╚████║
    ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
    """)
    print("           DIctionary GENerator")
    print("=" * 60)


def print_help():
    print("?l - lower case (a-z)")
    print("?u - upper case (A-Z)")
    print("?d - digit (0-9)")
    print("?s - special (!@#$%^&*()_+-=)")
    print("?a - ?l?u?d?s")
    print("?w - word from file")
    print("Hardcoded characters are inserted as is")
    print("\nExamples:")
    print("  ?w?d?d          - word00, word01,...")
    print("  ?u?l?l?l?w      - Aaaaword")
    print("  prefix_?w_suffix - prefix_word_suffix")
    print("  ?w?w?d          - wordword0, wordword1,...")


def get_mask_from_user():
    while True:
        mask = input("\nEnter mask for wordlists generation: ")
        if not mask:
            print("Empty mask!")
            continue
        # Checking the mask's correctness
        i = 0
        valid = True
        while i < len(mask):
            if mask[i] == '?':
                if i + 1 >= len(mask):
                    print("'?' must be before the type symbol (a, l, u, d, s, w)")
                    valid = False
                    break
                elif mask[i + 1] not in ['a', 'l', 'u', 'd', 's', 'w']:
                    print(f"Unknown symbol '{mask[i + 1]}' after '?'")
                    print("Acceptable types: a, l, u, d, s, w")
                    valid = False
                    break
                i += 2
            else:
                i += 1
        if valid:
            return mask


def load_words_from_file(filename):
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:  # Skipping empty lines
                    words.append(word)
        if not words:
            print(f"File '{filename}' is empty!")
            return None
        # Delete dublicates
        unique_words = list(set(words))
        print(f"Words loaded from file: {len(words)} (uniq: {len(unique_words)})")
        return unique_words
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return None
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None


def generate_combinations(mask, word_files=None):
    if word_files is None:
        word_files = {}
    # Define character sets for each type
    char_sets = {
        'a': list(string.ascii_letters + string.digits + string.punctuation),
        'l': list(string.ascii_lowercase),
        'u': list(string.ascii_uppercase),
        'd': list(string.digits),
        's': list(string.punctuation)
    }
    # Parse the mask and create lists of characters for each position.
    positions = []
    w_positions = []  # For ?w
    i = 0
    pos_index = 0
    while i < len(mask):
        if mask[i] == '?' and i + 1 < len(mask) and mask[i + 1] in ['a', 'l', 'u', 'd', 's', 'w']:
            char_type = mask[i + 1]
            if char_type == 'w':
                # This position for word from file
                w_positions.append(pos_index)
                # Add empty list
                positions.append([])
            else:
                positions.append(char_sets[char_type])
            i += 2
        else:
            positions.append([mask[i]])
            i += 1
        pos_index += 1
    # Request files
    if w_positions:
        print(f"\nPosition for words from file: {len(w_positions)}")
        # Request files for each ?w position
        word_lists = {}
        for w_idx, pos_idx in enumerate(w_positions):
            while True:
                if len(w_positions) > 1:
                    file_prompt = f"Enter the path to the file with the words for the position {w_idx + 1}: "
                else:
                    file_prompt = "Enter the path to the file with the words: "
                filename = input(file_prompt).strip()
                words = load_words_from_file(filename)
                if words is not None:
                    word_lists[pos_idx] = words
                    break
                else:
                    print("Please try again or type 'exit'.")
                    if input("Continue? (y/n): ").lower() != 'y':
                        return []
        # Filling in the positions with words from files
        for pos_idx, words in word_lists.items():
            positions[pos_idx] = words
    # Calculate the total number of combinations
    total_combinations = 1
    for pos in positions:
        total_combinations *= len(pos)
    if total_combinations > 1000000:
        print("\n⚠ Attention: Generating a large number of words can take time and a lot of memory. Be quiet...")
        print(f"Estimated file size: {total_combinations * 10 / 1024 / 1024:.1f} MB")
        response = input("Continue? (y/n): ").lower()
        if response != 'y':
            return []
    # Generation all combinations
    generated_words = []
    print("\nGeneration...")
    for i, combination in enumerate(itertools.product(*positions)):
        generated_words.append(''.join(combination))
        # Progress bar for large wordlists
        if total_combinations > 100000 and i % 100000 == 0 and i > 0:
            progress = (i / total_combinations) * 100
            print(f"Progress: {i:,} / {total_combinations:,} ({progress:.1f}%)")
    return generated_words


def save_to_file(words, filename="dictionary.txt"):
    if not words:
        print("No words!")
        return
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')
        print(f"\n✓ Successful stored in '{filename}'!")
        print(f"✓ Words: {len(words):,}")

        # Size info
        file_size = os.path.getsize(filename)
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        print(f"✓ File size: {size_str}")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    print_name()
    print_help()
    mask = get_mask_from_user()
    # Check ?w
    if '?w' in mask:
        print("\n" + "-" * 60)
        print("Detected ?w - you will need to use file(s) with words")
        print("-" * 60)
    # Generation words
    words = generate_combinations(mask)
    if not words:
        print("\nGeneration cancelled or failed.")
        return
    # Stored in file
    default_name = "Dictionary.txt"
    filename = input(f"\nEnter filename (default '{default_name}'): ")
    if not filename:
        filename = default_name
    if not filename.endswith('.txt'):
        filename += '.txt'
    save_to_file(words, filename)
    print("\n" + "=" * 60)
    print("Thank's for using DiGen")
    print("=" * 60)


if __name__ == "__main__":
    main()
