#!/usr/bin/env python3

import argparse
from llm import LLM
import os

if __name__ == "__main__":
    if 'OPENAI_API_KEY' not in os.environ:
        raise EnvironmentError("The OPENAI_API_KEY environment variable is not set.")

    parser = argparse.ArgumentParser(description="Generate a response from input prompt.")
    parser.add_argument("input_prompt", type=str, help="Input prompt for generation")
    parser.add_argument("--choices", type=str, help="Comma-separated list of choices for multiple-choice")
    parser.add_argument("--boolean", action='store_true', help="Specify if the response should be a boolean")
    
    args = parser.parse_args()
    
    if args.boolean:
        result = LLM().generate_bool(args.input_prompt)
    elif args.choices:
        choices = args.choices.split(',')
        result = LLM().generate_multichoice(args.input_prompt, choices)
    else:
        result = LLM().generate_text(args.input_prompt)
    
    print(result)