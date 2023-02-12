import requests

class EcommerceStore:
    def __init__(self):
        pass
    def fetchAssistant(self, endpoint):
        res = requests.get("https://api.escuelajs.co/api/v1{}".format(endpoint))
        if res.status_code == 200:
            return res.json()
        else:
            print(res.status_code)
            return []
    
    def getProductById(self, productId):
        return self.fetchAssistant("/products/{}".format(productId))
    
    def getAllCategories(self):
        return self.fetchAssistant("/categories?limit=2")
    
    def getProductsInCategory(self, categoryId):
        return self.fetchAssistant("/categories/{}/products?limit=3".format(categoryId))
