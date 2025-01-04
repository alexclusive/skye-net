from openai import OpenAI
from assets.core_utils import openai_key

client = OpenAI(
  api_key=openai_key
)

def openai_chat(messages):
	try:
		completion = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=messages
		)
		return completion.choices[0].message.content
	except Exception as e:
		return e