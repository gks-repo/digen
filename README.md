# DiGen — DIctionary GENerator

A command-line tool for generating wordlists based on a mask. It combines character sets and/or words from a file into all possible combinations. Useful for building dictionaries for password and username brute-forcing.

## Usage

```
python digen.py mask [output_file]
```

| Argument      | Description                                       |
|---------------|---------------------------------------------------|
| `mask`        | Generation mask (required)                        |
| `output_file` | Output filename (default: `wordlist.txt`)         |

If `output_file` is not specified, the result is saved to `wordlist.txt`. If the filename does not end with `.txt`, the extension is appended automatically.

## Mask syntax

| Placeholder | Character set                             |
|-------------|-------------------------------------------|
| `?l`        | lowercase letters (a-z)                   |
| `?u`        | uppercase letters (A-Z)                   |
| `?d`        | digits (0-9)                              |
| `?s`        | special characters (!"#$%&'...)           |
| `?a`        | all of the above (`?l?u?d?s`)             |
| `?w`        | word from file (prompted interactively)   |

Any other characters in the mask are inserted as-is.

## Examples

```bash
# Three digits: 000, 001, ..., 999
python digen.py "?d?d?d" pins.txt

# Word + two digits: admin00, admin01, ..., admin99
python digen.py "?w?d?d"

# Uppercase + three lowercase: Aaaa, Aaab, ..., Zzzz
python digen.py "?u?l?l?l" names.txt

# Prefix + word + suffix: admin_gordeev_01, ...
python digen.py "admin_?w_?d?d" dict.txt

# Two word files: word1_word2
python digen.py "?w_?w" pairs.txt

# Fixed characters only: abc
python digen.py "abc" single.txt
```

When using `?w`, the program interactively prompts for a word file path (one word per line). Duplicates and empty lines are removed automatically.

If the total number of combinations exceeds 1,000,000, the program asks for confirmation before proceeding.
