import abc
import requests



BASE_URL = "https://api.shahreketabonline.com"

EMAIL = "zlab@fanap.ir"
SECRET_KEY = "ZL@b$1399"

class AbstractCrawler(abc.ABC):

    @abc.abstractmethod
    def get_token(self, email:str, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_products(self, from_id: int, to_id:int, page:int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_attribuutes(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_types(self):
        raise NotImplementedError


class Crawler(AbstractCrawler):

    def get_token(self, email: str, password: str):
        login_obj = requests.post(
            f"{BASE_URL}/Login",
            json={
                "email": email,
                "password": password
            }
        )
        return login_obj.json()

    def get_products(self, from_id: int, to_id: int, page: int):
        
        response = requests.get(
            f"{BASE_URL}/SemanticSearch/GetProducts",
            params={
                "FromID": from_id,
                "ToID": to_id,
                "Page": page
            },
            headers={'Authorization': f'Bearer {Crawler.get_token(self=Crawler, email=f"{EMAIL}", password=f"{SECRET_KEY}")["accessToken"]}'}
        )
        return response.json()

    def get_attribuutes(self):
        response = requests.get(
            f"{BASE_URL}/SemanticSearch/GetAttributes",
            headers={'Authorization': f'Bearer {Crawler.get_token(self=Crawler, email=f"{EMAIL}", password=f"{SECRET_KEY}")["accessToken"]}'}
        )
        return response.json()

    def get_types(self):
        response = requests.get(
            f"{BASE_URL}/SemanticSearch/GetTypes",
            headers={'Authorization': f'Bearer {Crawler.get_token(self=Crawler, email=f"{EMAIL}", password=f"{SECRET_KEY}")["accessToken"]}'}
        )
        return response.json()



crawler = Crawler()


print(f"Response : {crawler.get_types()}")

# print(f"products: {crawler.get_products(1,3,1)}")
# print(f"response: {response.json()}")


# for i in get_types():
#     if i['id'] == 3707:
#         print(i['title']) 

