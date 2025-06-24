import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_MAIN_LOOP

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
    
    for i in range(20):
        if i > MAX_MAIN_LOOP:
            print(f"max iterations {MAX_MAIN_LOOP} reached")
            sys.exit(1)

        try: 
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
            
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                 tools=[available_functions], system_instruction=system_prompt),
        )

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if not response.function_calls:
            return response.text

        function_responses = [] 
        for f in response.function_calls:
            result = call_function(f, verbose)
            if (
                 not result.parts
                 or not result.parts[0].function_response
            ):
                 raise Exception("Error: empty function call result")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        
        messages.append(types.Content(role="tool", parts=function_responses))
    
    
if __name__ == "__main__":
    main()

