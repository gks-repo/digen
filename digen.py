import itertools
import string
import os
import argparse

CHAR_SETS = {
    'a': string.ascii_letters + string.digits + string.punctuation,
    'l': string.ascii_lowercase,
    'u': string.ascii_uppercase,
    'd': string.digits,
    's': string.punctuation,
}

MASK_HELP = """\
Mask types:
  ?l - lowercase (a-z)
  ?u - uppercase (A-Z)
  ?d - digits (0-9)
  ?s - special chars
  ?a - all of the above
  ?w - word from file

Examples:
  python digen.py "?w?d?d" dict.txt
  python digen.py "?u?l?l?l" dict.txt
  python digen.py "prefix_?w_suffix" dict.txt
"""


def parse_mask(mask):
    if not mask:
        raise ValueError("Mask cannot be empty")
    positions = []
    w_indices = []
    i = 0
    while i < len(mask):
        if mask[i] == '?':
            if i + 1 >= len(mask):
                raise ValueError("'?' must be followed by a type: a, l, u, d, s, w")
            t = mask[i + 1]
            if t == 'w':
                w_indices.append(len(positions))
                positions.append(None)
            elif t in CHAR_SETS:
                positions.append(CHAR_SETS[t])
            else:
                raise ValueError(f"Unknown type '?{t}'. Valid: a, l, u, d, s, w")
            i += 2
        else:
            positions.append(mask[i])
            i += 1
    return positions, w_indices


def load_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            words = list(set(line.strip() for line in f if line.strip()))
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return None
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        return None
    if not words:
        print(f"File '{filename}' is empty!")
        return None
    print(f"Loaded {len(words)} unique words from '{filename}'")
    return words


def prompt_word_files(w_indices, positions):
    if not w_indices:
        return positions
    for idx, pos in enumerate(w_indices):
        prompt = f"Word file for position {idx + 1}: " if len(w_indices) > 1 else "Word file: "
        while True:
            words = load_words(input(prompt).strip())
            if words is not None:
                positions[pos] = words
                break
            if input("Continue? (y/n): ").lower() != 'y':
                return None
    return positions


def generate(positions):
    total = 1
    for p in positions:
        total *= len(p)
    if total > 1_000_000:
        print(f"\nWARNING: {total:,} combinations (~{total * 10 / 1024 / 1024:.1f} MB)")
        if input("Continue? (y/n): ").lower() != 'y':
            return None
    print("\nGenerating...")
    result = []
    for i, combo in enumerate(itertools.product(*positions)):
        result.append(''.join(combo))
        if total > 100_000 and i % 100_000 == 0 and i > 0:
            print(f"  {i:,} / {total:,} ({i / total * 100:.1f}%)")
    return result


def save(words, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(w + '\n' for w in words)
        size = os.path.getsize(filename)
        unit = 'B'
        for u in ('KB', 'MB', 'GB'):
            if size < 1024:
                break
            size /= 1024
            unit = u
        print(f"\n[OK] Saved {len(words):,} words to '{filename}' ({size:.1f} {unit})")
    except Exception as e:
        print(f"[ERR] Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="DiGen - DIctionary GENerator",
        epilog=MASK_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("mask", nargs='?', help="Generation mask")
    parser.add_argument("output_file", nargs='?', default="wordlist.txt", help="Output filename")
    args = parser.parse_args()
    if args.mask is None:
        print("usage: digen.py [-h] mask [output_file]")
        return

    print("=" * 60)
    print("         DiGen - DIctionary GENerator")
    print("=" * 60)

    try:
        positions, w_indices = parse_mask(args.mask)
    except ValueError as e:
        print(f"Invalid mask: {e}")
        return

    positions = prompt_word_files(w_indices, positions)
    if positions is None:
        return

    words = generate(positions)
    if words is None:
        print("\nCancelled.")
        return

    filename = args.output_file
    if not filename.endswith('.txt'):
        filename += '.txt'
    save(words, filename)
    print("=" * 60)


if __name__ == "__main__":
    main()
