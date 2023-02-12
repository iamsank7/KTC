class ButtonUtils:
    def __init__(self) -> None:
        pass
    def createReplyButtonSpec(self, id, title):
        return {
            "id": id,
            "title": title
        }

    def createReplyButtonList(self, buttonsList):
        reply_button_list = []
        for button in buttonsList:
            reply_button_list.append({
                "type": "reply",
                "reply": button
            })
        return reply_button_list