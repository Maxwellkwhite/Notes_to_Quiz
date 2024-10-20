import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a quiz generator assistant."},
        {
            "role": "user",
            "content": "Create a quiz based on the following economics notes. Output the quiz in JSON format:\n\n" + open('notes.txt', 'r').read()
        }
    ]
)

quiz_json = completion.choices[0].message.content

with open('economics_quiz.json', 'w') as f:
    f.write(quiz_json)

print("Quiz generated and saved to economics_quiz.json")