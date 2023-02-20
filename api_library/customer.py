from datetime import date

class Customer:
    def __init__(self, customer_id: int, name: str, address: str, 
                email: str, birth_date: date) -> None:
        
        self.__customer_id: int = customer_id
        self.__name: str = name
        self.__address: str = address
        self.__email: str = email
        self.__birth_date: date = birth_date

    def get_id(self) -> int:
        return self.__customer_id

    def get_name(self) -> str:
        return self.__name
    
    def get_address(self) -> str:
        return self.__address
    
    def get_email(self) -> str:
        return self.__email
    
    def get_birth_date(self) -> date:
        return self.__birth_date