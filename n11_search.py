import logging

from locust import HttpUser, TaskSet, task, constant
from bs4 import BeautifulSoup
import random


class N11SearchLoadTest(HttpUser):
    search_query_path = "/arama?q="
    product_list_element = {"class": "catalogView"}
    host = "https://www.n11.com"
    wait_time = constant(1)

    @task
    def search(self):
        search_key_list = ['telefon', 'bilgisayar', 'tablet', 'elbise', 'oyuncak']
        search_key = random.choice(search_key_list)
        with self.client.get(self.search_query_path + search_key, catch_response=True) as response:
            pq = BeautifulSoup(response.content, "html.parser")
            if pq.find(attrs=self.product_list_element) is None:
                response.failure("Response does not contain product list")
            else:
                logging.info("Request success")
