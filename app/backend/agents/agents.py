from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')
client=OpenAI(api_key=key)



def run_agent(system_prompt, user_prompt):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    print("in run_agent def")
    print(response)
    response.output_text

# Agent 1: Director
director_answer = run_agent(
    "You are the Director of this space mission. You are very confident but almost always wrong.",
    "What is the code to land safely?"
)

# Agent 2: Engineer
engineer_answer = run_agent(
    "You are the Engineer of this space mission. You are very upset that it has gone wrong",
    "How much time does the pilot have before the engines stop working?."
)

# Agent 3: Navigator
navigator_answer = run_agent(
    "You are the Navigator of this space mission. You are cool, calm, collected and British",
    "What is the safest route for our pilot."
)

# Agent 4: Mediator
mediator_answer = run_agent(
    "You are the mediator, called in to help with this crisis. You don't like to take sides",
    "Who is to blame for this?"
)

print(director_answer)
print(engineer_answer)
print(navigator_answer)
print(mediator_answer)