from openai import OpenAI

client = OpenAI(api_key="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")

print("Checking the connection...")

try:
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are a career mentor for IIT/ISB/IIM/MBA grads."},
        {"role": "user", "content": "Give me a 1-sentence tip for a job seeker today."}
      ]
    )
    print("\n--- SUCCESS! ---")
    print(response.choices[0].message.content)
except Exception as e:
    print("\n--- SOMETHING WENT WRONG ---")
    print(e)