import openai

openai.api_key = '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'


def chat_parse(location, keywords, text) -> str:
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant to extract events related to the keyword provided by user."},
            {"role": "user", "content":
                f'Extract the events happened in {location} and related to {keywords} from the given text.' +
                'For each related event, provid its name, start date, location and a one sentence summary of it.' +
                'Example format: [{"Name": "event name", "Date": "event start date", "Location": "event location", '
                '"Summary": "one sentence summary of the event", {...}, ...]' +
                f'If there is no event founded in the text, return "[]". Here is the text:\n{text}'}
        ]
    )["choices"][0]["message"]["content"]
    return res
