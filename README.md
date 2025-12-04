# digen
DIctionary GENerator

Very often, during pentests, we receive an account hash (of any form) that needs to be recovered.
And success largely depends on the dictionary we use for brute-force. DIGEN was created for this purpose.

Using this script, we can generate effective passwords for brute-force by combining character sets and/or words from a file.
It can also help with brute-forcing logins if we know the mask (c.j.smith, monaghann_fr etc.).

# Usage:
python3 digen.py mask

**Mask:**

  *?l - lower case (a-z)*
  
  *?u - upper case (A-Z)*
  
  *?d - digit (0-9)*
  
  *?s - special*
  
  *?a - ?l?u?d?s*
  
  *?w - word from file*
  
  Hardcoded characters are inserted as is.
  
**Examples:**

  *?w?d?d*           - word00, word01,...
  
  *?u?l?l?l?w*       - Aaaaword, Aaabword,...
  
  *prefix_?w_suffix* - prefix_word_suffix,...
  
  *?w?w?d*           - wordword0, wordword1,...
