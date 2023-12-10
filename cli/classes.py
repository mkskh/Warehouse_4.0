from data import personnel, stock
from loader import Loader
import datetime


class Warehouse:

    def __init__(self, warehouse_id: int) -> None:
        self.warehouse_id = warehouse_id
        self.stock = []

    @property
    def id(self):
        return self.warehouse_id
    
    @property
    def stock_here(self):
        return self.stock

    def occupancy(self):
        return len(self.stock)

    def add_item(self, item) -> None:
        self.stock.append(item)

    def search(self, search_term: str) -> list:
        items_list = []
        for item in self.stock:
            if search_term.lower() == str(item).lower(): # Need to finish
                items_list.append(item)
        return items_list


class Item:

    def __init__(self, state: str, category: str, warehouse: int, date_of_stock: datetime) -> None:
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self) -> str:
        return f'{self.state} {self.category}'

    @property
    def state_pr(self):
        return self.state
    
    @property
    def category_pr(self):
        return self.category
    
    @property
    def date_of_stock_pr(self):
        return self.date_of_stock



class User:
    def __init__(self, user_name="Anonymous") -> None:
        self._name = user_name
        self.is_authenticated = False

    @property
    def name_pr(self):
        return self._name
    
    @property
    def is_authenticated_pr(self):
        return self.is_authenticated
    
    def authenticate(self, password: str):
        return False

    def is_named(self, name: str):
        if name == self._name:
            return True

    def greet(self):
        print(f"\nHello, {self._name}! \nWelcome to our Warehouse Database. \nIf you don't find what you are looking for,\nplease ask one of our staff members to assist you.")

    def bye(self, actions: list):
        print(f'Thank you for your visit, {self._name}!\n{actions}')


class Employee(User):

    def __init__(self, password, user_name="Anonymous", head_of=[]) -> None:
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of

    @property
    def password_pr(self):
        return self.__password

    @property
    def head_of_pr(self):
        return self.head_of

    def authenticate(self, password: str):
        if password == self.__password:
            return True
        else:
            return False

    def order(self, item, amount): # The order method will print the name of the item and amount ordered by the user when they place an order
        print(f'{amount} {item} have been ordered.')

    def greet(self):
        print(f"\nHello, {self._name}! \nIf you experience a problem with the system,\nplease contact technical support.")

