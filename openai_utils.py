import openai
import backoff  # for exponential backoff
from config import openapi_key

openai.api_key = openapi_key

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def gpt3(stext):
	response = openai.Completion.create(
		engine="gpt-3.5-turbo-16k",
		prompt=stext,
		temperature=0.7,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0
	)
	return response.choices[0].text


def gpt4(systemprompt, usercontent, model="gpt-3.5-turbo-16k"):

	response = openai.ChatCompletion.create(
		model=model,
		# max_tokens=5000,
		messages=[
			{"role": "system", "content": systemprompt},
			{"role": "user", "content": usercontent},

		]
	)
	return response.choices[0].message.content