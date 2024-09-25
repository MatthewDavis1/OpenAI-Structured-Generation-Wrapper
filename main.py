#!/usr/bin/env python3

import argparse
from llm import LLM

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a boolean response from input prompt.")
    parser.add_argument("input_prompt", type=str, help="Input prompt for boolean generation")
    
    args = parser.parse_args()
    result = LLM().generate_bool(args.input_prompt)
    print('YES' if result else 'NO')