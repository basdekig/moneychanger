from typing import Tuple, Dict
import dotenv
import os
from dotenv import load_dotenv
import requests
import json
import streamlit as st
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

load_dotenv()
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')

#st.title("Multilingual Money Changer")

# A single text input box
#user_text = st.text_input("Enter the amount and the currency:")

# Submit button
#if st.button("Submit"):
#    # Print the user input below the textbox
#    st.write(call_llm, (user_input))

def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    print(requests.get(url).text)
    response= json.loads(requests.get(url).text)
    """return(base, target, amount, EXCHANGERATE_API_KEY)"""
    return({base}, {target}, {amount}, f'{response["conversion_result"]:.2f}')

print(get_exchange_rate("USD","EUR","100")) 

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target
    """
    tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "exchange rate function",
                        "description": "Converts an amount from a base currency to a target currency.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "base": {
                                    "type": "string",
                                    "description": "The currency to convert from (e.g., 'USD', 'EUR')."
                        },
                                "target": {
                                    "type": "string",
                                    "description": "The currency to convert to (e.g., 'JPY', 'CAD')."
                        },
                                "amount": {
                                    "type": "string",
                                    "description": "The amount of currency to convert."
                        }
                        },
                        "required": ["base", "target", "amount"],
                        "additionalProperties": False,
                    }
                    }
                }
]
    try:
        response = client.chat.completions.create(
                messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            tools=tools
        )
    #print(response.choices[0].message.content)
    except Exception as e:
          print(f"Exception {e} for {text}")
    else:
        return response#.choices[0].message.content   
    

def run_pipeline(user_input):
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""
    response = call_llm(user_input)
    #st.write(response)
    
    if response.choices[0].finish_reason =="tool_calls":
    #if True: #tool_calls
        response_arguments = json.loads(response.choices[0].message.content.tool_calls[0].function.arguments)
        #st.write(response_arguments)
        base  =  response_arguments["base"]
        target =  response_arguments["target"]
        amount =  response_arguments["amount"]
        #st.write(get_exchange_rate(base, target, amount))
        _,_,_, conversion_result == get_exchange_rate(base, target, amount)
        #st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]}')
        st.write(f'{base} {amount} is {target} {conversion_result}')

    elif  response.choices[0].finish_reason =="stop":  # True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and {response.choices[0].message.content}")
    else:
        st.write("NotImplemented")
    
st.title("Multilingual Money Changer")

# A single text input box
user_text = st.text_input("Enter the amount and the currency:")

# Submit button
if st.button("Submit"):
    # Print the user input below the textbox
    #st.write(call_llm, (user_input)) 
    #response = call_llm(user_input)
    response = run_pipeline(user_input)
   # response_arguments = json.loads(response.choices[0].message.content.tool_calls[0].function.arguments)
   # #st.write(response_arguments)
   # base  =  response_arguments["base"]
   # target =  response_arguments["target"]
   # amount =  response_arguments["amount"]
   # st.write(get_exchange_rate(base, target, amount))

