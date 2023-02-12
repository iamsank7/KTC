class ReplyHandler:
    def __init__(self, whatsAppMessenger) -> None:
        self.messenger = whatsAppMessenger
    
    def handleText(self, data):
        message = self.messenger.get_message(data)
        name = self.messenger.get_name(data)
        mobile = self.messenger.get_mobile(data)
        print("Message: %s", message)
        self.messenger.send_reply_button(
            recipient_id=mobile,
            button={
                "type": "button",
                "body": {
                    "text": "Hey {}, \nYou are speaking to a chatbot.\nWhat do you want to do next?".format(name)
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "see_categories",
                                "title": "View some products"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "speak_to_human",
                                "title": "Speak to a human"
                            }
                        }
                    ]
                }
            },
        )