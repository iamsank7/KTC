from .button_utils import ButtonUtils

class ReplyHandler:
    def __init__(self, whatsAppMessenger) -> None:
        self.messenger = whatsAppMessenger
        self.button_utils = ButtonUtils()
    
    def handleText(self, name, mobile):
        self.messenger.send_reply_button(
            recipient_id=mobile,
            button={
                "type": "button",
                "body": {
                    "text": "Hey {}, \nYou are speaking to a chatbot.\nWhat do you want to do next?".format(name)
                },
                "action": {
                    "buttons": self.button_utils.createReplyButtonList(
                        [
                            self.button_utils.createReplyButtonSpec(id="see_categories", title="View some products"),
                            self.button_utils.createReplyButtonSpec(id="speak_to_human", title="Speak to a human")
                        ]
                    )
                }
            },
        )
    
    def handleHumanAssistance(self, mobile):
        self.messenger.send_message("Arguably, chatbots are faster than humans.\nCall my human with the below details:", recipient_id=mobile)
        self.messenger.send_contacts(
            [{
                "addresses": [{
                    
                    "city": "GWL",
                    "state": "MP",
                    "zip": "474003",
                    "country": "INDIA",
                    "type": "HOME",
                    }],
                "name": {
                "formatted_name": "NAME",
                "first_name": "Sankalp",
                    "last_name": "Gupta",
                },
                "phones": [{
                    "phone": "7894561230",
                    "type": "HOME"
                }],
                }
            ],
            recipient_id=mobile
        )
    
    def handleSeeCategories(self, mobile, categories):
        reply_buttons = []
        self.button_utils.createReplyButtonSpec(id="category_{}".format(category['id']), title=category['name'])
        for category in categories:
            reply_buttons.append(
                self.button_utils.createReplyButtonSpec(id="category_{}".format(category['id']), title=category['name'])
            )
        self.messenger.send_reply_button(
            recipient_id=mobile,
            button={
                "type": "button",
                "body": {
                    "text": "We have several categories.\nChoose one of them.",
                },
                "action": {
                    "buttons": self.button_utils.createReplyButtonList(reply_buttons)
                }
            },
        )
    
    def handleProductsInCategory(self, mobile, products):
        product_rows = []
        for product in products:
            product_rows.append({
                "id": "product_{}".format(product['id']),
                "title": product['title'][:20],
                "description": product['description'][:72] if 'description' in product else ""
            })
        self.messenger.send_button(
            recipient_id=mobile,
            button={
                "body": "Please select one of the products below:",
                "action": {
                    "button": "Select a product",
                    "sections": [{
                        "title": "Our Products",
                        "rows": product_rows
                    }]
                },
            },
        )