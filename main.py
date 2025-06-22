import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = list(filter(lambda arg: not arg.startswith("--"), sys.argv[1:]))

    if not args:
        print("AI Code Assistant")
        print('\nUsage -> python main.py "your prompt here"')
        print('Example -> python main.py "How do I build a calculator app?"')
        sys.exit(1)


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
         print(f"User prompt: {user_prompt}\n")
    

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    query_model_with_output(client, messages, verbose)

def query_model_with_output(client, messages, verbose):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
        )

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()

