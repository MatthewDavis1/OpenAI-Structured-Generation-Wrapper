# OpenAI Structured Generation API Wrapper

This mini project provides a simple wrapper around OpenAI's structured generation API, designed for one-shot input/output (IO) prompting. It allows users to easily generate text, structured responses, multiple-choice selections, integers, and boolean values using OpenAI's models.

## Features

- Generate plain text responses.
- Generate structured responses using Pydantic models or JSON schema.
- Support for multiple-choice questions (choices determinable at runtime).
- Generate integers within a specified range.
- Generate boolean values.

## Installation

To install this package, clone this repo, and run ```pip install -r requirements.txt```.

## Usage

Here's how to use the wrapper in your code:

```
from llm import LLM

# Initialize the LLM with a specific model name
llm = LLM(model_name='gpt-4o-2024-08-06')

# Generate plain text response
text_response = llm.generate_text("What is the capital of France?")
print(text_response)  # Output: Paris

# Generate structured response
from pydantic import BaseModel

class ResponseModel(BaseModel):
    answer: str

structured_response = llm.generate_structured("What is the capital of France?", ResponseModel)
print(structured_response.answer)  # Output: Paris

# Generate multiple-choice response
choices = ['Paris', 'London', 'Berlin']
choice_response = llm.generate_multichoice("Choose the capital of France:", choices)
print(choice_response)  # Output: Paris

# Generate an integer within a range
integer_response = llm.generate_int("Pick a number between 1 and 10:", 1, 10)
print(integer_response)  # Output: A number between 1 and 10

# Generate a boolean response
bool_response = llm.generate_bool("Is Paris the capital of France?")
print(bool_response)  # Output: True
```
