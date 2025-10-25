#!/usr/bin/env python3

import re
import sys
import os

def create_replacer(s: str) -> str:
    """
    Applies the series of regex replacements to a given string.
    """
    
    # Rule 1: \1 -> \x01 (but not \0)
    # e.g., "\1" becomes "\x01"
    s = re.sub(r'\\([1-9])', r'\\x0\1', s)
    
    # Rule 2: \07 -> \x007
    # Note: This rule is unusual. It changes an octal 7 (one byte: 0x07)
    # into a NULL byte followed by the character '7' (two bytes: 0x00 0x37).
    # Implementing as requested.
    s = re.sub(r'\\0(\d)', r'\\x00\1', s)
    
    # Rule 3: \v -> \x0B
    # e.g., "\v" becomes "\x0B"
    s = re.sub(r'\\v', r'\\x0B', s)
    
    # Rule 4: ' -> \' (escapes unescaped single quotes)
    # e.g., "foo'bar" becomes "foo\'bar"
    s = re.sub(r"([^\\])'", r"\1\\'", s)
    
    return s

def process_file_matches(match_obj: re.Match) -> str:
    """
    This function is called by re.sub for each string that matches
    the scope_regex. It passes the string content to the replacer.
    """
    # We capture the quotes and the content separately
    # group(1) is the opening quote
    # group(2) is the string content
    # group(3) is the closing quote
    opening_quote = match_obj.group(1)
    content = match_obj.group(2)
    closing_quote = match_obj.group(3)
    
    # Apply the fixes only to the content
    fixed_content = create_replacer(content)
    
    # Return the reassembled string
    return f"{opening_quote}{fixed_content}{closing_quote}"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {os.path.basename(__file__)} <input_file> <output_file>")
        print("Example: python fix_firmware_escapes.py firmware.dump firmware.fixed.dump")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
        
    print(f"Processing '{input_file}'...")

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # This regex finds all C-style strings (starting and ending with ")
        # that contain at least one "\x" sequence.
        # It correctly handles escaped quotes (\") inside the string.
        # It captures the quotes (group 1, 3) and content (group 2) separately.
        scope_regex = r'(")((?:\\.|[^"\\])*\\x(?:\\.|[^"\\])*)(")'
        
        # We use re.sub with a callback function (process_file_matches)
        # This applies the replacements only to the matched strings.
        new_content = re.sub(scope_regex, process_file_matches, content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Successfully fixed escapes and saved to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()