from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from heyoo import WhatsApp
import time
from .ecommerce_store import EcommerceStore

wa_token = 'EAAWNXwCMvnYBAKZCYLZB89szK9emalxxPwfJkZBLjpYfghmC3AMEvZBffuS0zbZC45Xr90FS9Nv24KxaY6N7FeMcSUpJAmgu7y2XrlgNMnltcCZC5bSTg7seEObZCQHFVJaNZAFwytZAZCKy1oa7cyieGq3FDShqvfZBnUAnYE9dByGbMFCkCC6Al9pOD2BkwFGHZBdLFhgN7NYMdQZDZD'
webhook_verify_token = 'a5ab670c-a4ac-11ed-b9df-0242ac120003'
phone_num_id = '116564778008868'

@api_view(['GET', 'POST'])
def whatsAppWebhhok(req):
    if req.method == 'POST':
        print('POST: Someone pinged!')
        data = req.data
        messenger = WhatsApp(token=wa_token, phone_number_id=phone_num_id)
        changed_field = messenger.changed_field(data)
        store = EcommerceStore()
        
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
                  message = messenger.get_message(data)
                  name = messenger.get_name(data)
                  print("Message: %s", message)
                  messenger.send_reply_button(
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
              if message_type == 'interactive' and interactive_message_type['type'] == 'button_reply':
                  print(interactive_message_type['button_reply']['id'])
                  if interactive_message_type['button_reply']['id'] == 'speak_to_human':
                      messenger.send_message("Arguably, chatbots are faster than humans.\nCall my human with the below details:", recipient_id=mobile)
                      messenger.send_contacts(
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
                  if interactive_message_type['button_reply']['id'] == 'see_categories':
                      categories = store.getAllCategories()
                      print(categories)
                      reply_buttons = []
                      for category in categories:
                          reply_buttons.append({
                              "type": "reply",
                              "reply": {
                                  "id": "category_{}".format(category['id']),
                                  "title": category['name']
                              }
                          })
                      messenger.send_reply_button(
                          recipient_id=mobile,
                          button={
                              "type": "button",
                              "body": {
                                  "text": "We have several categories.\nChoose one of them.",
                              },
                              "action": {
                                  "buttons": reply_buttons
                              }
                        },
                      )
                  if interactive_message_type['button_reply']['id'].startswith("category_"):
                      category_id = interactive_message_type['button_reply']['id'].split("_")[1]
                      products = store.getProductsInCategory(category_id)
                      print(products[:10])
                      product_rows = []
                      for product in products:
                          product_rows.append({
                              "id": "product_{}".format(product['id']),
                              "title": product['title'][:20],
                              "description": product['description'][:72] if 'description' in product else ""
                          })
                      product_rows = product_rows[:10]
                      messenger.send_button(
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
                  if interactive_message_type['button_reply']['id'].startswith("add_to_cart_"):
                      product_id = interactive_message_type['button_reply']['id'].split("_")[-1]
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
                  if interactive_message_type['button_reply']['id'].startswith("checkout"):
                      product_id = interactive_message_type['button_reply']['id'].split("_")[-1]
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