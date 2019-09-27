from twilio.rest import Client
from Constants import env
from Environment import get_env


class _twilio:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sid = get_env(env.TWILIO_SID)
        token = get_env(env.TWILIO_TOKEN)
        self.client = Client(sid, token)

    def send_message(self, message):
        message = self.client.messages.create(
            to="+15417978409",
            from_="+15412044631",
            body=message)

        print(message.sid)


if __name__ == "__main__":
    twil = _twilio()
    twil.send_message("This is a test!")
