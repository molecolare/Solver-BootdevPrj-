import os
from dotenv import load_dotenv
import argparse
from openai import OpenAI
from prompt.prompts import system_prompt
from call_function import available_functions, call_function
from functions.get_files_info import get_files_info
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
parser = argparse.ArgumentParser(description="Solver")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    user_prompt = args.user_prompt
    messages=[
         {"role": "system", "content": system_prompt},
         {
            "role": "user",
            "content": user_prompt
         }
    ]
    try:
        response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
            #    temperature = 0,
                tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("Failed to get token usage from the API response")
        message = response.choices[0].message
        if args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print("\nResponse:")
        if message.tool_calls:
                    for tool_call in message.tool_calls:
                        result_message = call_function(tool_call, args.verbose)
                        print(result_message["content"])
        else:
                    # Se non ci sono tool_calls, stampa il contenuto testuale
                    print(message.content)
    except Exception as e:
        print(f"Errore durante la chiamata API: {e}")

if __name__ == "__main__":
    main()
