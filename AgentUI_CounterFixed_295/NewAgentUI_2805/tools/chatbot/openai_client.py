class OpenAIClient:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI()

    def send_message(self, message):
        completion = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": message}]
        )
        return completion.choices[0].message.content