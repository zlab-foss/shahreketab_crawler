import abc
import requests

from src.crawler import config


class AbstractCrawler(abc.ABC):

    @abc.abstractmethod
    def get_token(self, email:str, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_products(self, from_id: int, to_id:int, page:int):
        raise NotImplementedError


class Crawler(AbstractCrawler):

    def __init__(self):
        self._setting = config.Settings().get_shahreketab_setting()
        self._shahreketab_url = self._setting[0]
        self._email = self._setting[1]
        self._password = self._setting[2]

    def get_token(self, email: str, password: str):
        login_obj = requests.post(
            f"{str(config.Settings().get_shahreketab_setting()[0])}/Login",
            json={
                "email": email,
                "password": password
            }
        )
        return login_obj.json()

    def get_products(self, from_id: int, to_id: int, page: int):
        response = requests.get(
            f"{str(self._shahreketab_url)}/SemanticSearch/GetProducts",
            params={
                "FromID": from_id,
                "ToID": to_id,
                "Page": page
            },
            headers={'Authorization': f'Bearer {Crawler.get_token(self=Crawler, email=str(self._email), password=str(self._password))["accessToken"]}'}
        )
        return response.json()


# crawler = Crawler()

# print(f"products: {crawler.get_products(1,3,1)}")
