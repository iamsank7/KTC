from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from heyoo import WhatsApp
import time
from .ecommerce_store import EcommerceStore
from .handler import ReplyHandler

wa_token = 'EAAWNXwCMvnYBALmTm0A7zWtC4LYedAhNMbcWrVC2aAY72oWwyvvppLW8hGRecpEgfPFdX38wLWmnatFEiqYNrA1XGVxVHf08bVZCuwx2SvAI3AAUXOD8FbYpYowZA4CtzeBvLJDWgM4ZARa8R0vwlSmizcSEFt4Fb5C6LUMWQo1DtwxOLW8ZAlRMRgg5PteV3KJoj8JReAZDZD'
webhook_verify_token = 'a5ab670c-a4ac-11ed-b9df-0242ac120003'
phone_num_id = '116564778008868'
store = EcommerceStore()

@api_view(['GET', 'POST'])
def whatsAppWebhhok(req):
    if req.method == 'POST':
        print('POST: Someone pinged!')
        data = req.data
        messenger = WhatsApp(token=wa_token, phone_number_id=phone_num_id)
        
        changed_field = messenger.changed_field(data)
        
        handler = ReplyHandler(messenger)

        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            
            if new_message:
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_type = messenger.get_message_type(data)
                interactive_message_type = messenger.get_interactive_response(data)
                CustomerSession = {
                    mobile: {
                        "cart": []
                    }
                } 
                
                print(
                    f"New Message; sender:{mobile} name:{name} type:{message_type} interactive_type: {interactive_message_type}"
                )
                
                if message_type == "text":
                    handler.handleText(name, mobile)
                if message_type == 'interactive' and interactive_message_type['type'] == 'button_reply':
                    reply_button_id = interactive_message_type['button_reply']['id']
                    if reply_button_id == 'speak_to_human':
                        handler.handleHumanAssistance(mobile) 
                    
                    if reply_button_id == 'see_categories':
                        categories = store.getAllCategories()
                        handler.handleSeeCategories(mobile, categories)
                        
                    if reply_button_id.startswith("category_"):
                        category_id = reply_button_id.split("_")[1]
                        products = store.getProductsInCategory(category_id)
                        handler.handleProductsInCategory(mobile, products[:10])
                        
                    if reply_button_id.startswith("add_to_cart_"):
                        product_id = reply_button_id.split("_")[-1]
                        product = store.getProductById(product_id)
                        CustomerSession[mobile]['cart'].append(product)
                        messenger.send_reply_button(
                            recipient_id=mobile,
                            button={
                                "type": "button",
                                "body": {
                                    "text": "Your cart has been updated.\nNumber of items in cart: {}.\n\nWhat do you want to do next?".format(len(CustomerSession[mobile]['cart'])),
                                },
                                "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "checkout",
                                            "title": "Checkout 🛍️"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "see_categories",
                                            "title": "See more products"
                                        }
                                    }
                                ]
                            }
                            },
                        )
                    if reply_button_id.startswith("checkout"):
                        pass
                        
                if message_type == 'interactive' and interactive_message_type['type'] == 'list_reply':
                    if interactive_message_type['list_reply']['id'].startswith("product_"):
                        product_id = interactive_message_type['list_reply']['id'].split("_")[1]
                        product = store.getProductById(product_id)
                        print(product)
                        
                        text = "_Title_: *{}*\n\n\n".format(product['title'])
                        text = text + "_Description_: {}\n\n\n".format(product['description'])
                        text = text + "_Price_ ${}\n".format(product['price'])

                        messenger.send_image(
                                recipient_id=mobile,
                                image=product['images'][0],
                                caption=text
                            )
                        time.sleep(3)
                        messenger.send_reply_button(
                            recipient_id=mobile,
                            button={
                                "type": "button",
                                "body": {
                                    "text": "Here is the product, what do you want to do next?",
                                },
                                "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "add_to_cart_{}".format(product_id),
                                            "title": "Add to cart🛒"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "see_categories",
                                            "title": "See more products"
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
        return HttpResponse(status=200)
    
    elif req.method == 'GET':
        print('GET: Someone ping me!')
        mode = req.GET['hub.mode']
        challenge = req.GET['hub.challenge']
        token = req.GET['hub.verify_token']
        print(token, challenge, mode)
        if webhook_verify_token == token and mode == 'subscribe':
            return HttpResponse(challenge, status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=403)
    return HttpResponse(status=500)