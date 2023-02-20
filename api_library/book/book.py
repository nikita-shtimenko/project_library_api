import datetime
from api_library.book.book_type import BookType

class Book:
    def __init__(self, book_id: int, book_type: BookType, 
                name: str, author: str, date_published: datetime.date) -> None:
        
        self.__book_id: int = book_id
        self.__book_type: BookType = book_type
        self.__name: str = name
        self.__author: str = author
        self.__date_published: datetime.date = date_published

    def get_id(self) -> int:
        return self.__book_id
    
    def get_type(self) -> BookType:
        return self.__book_type
    
    def get_max_loan_time(self) -> datetime.timedelta:
        return self.__book_type.get_max_loan_time()
    
    def get_name(self) -> str:
        return self.__name
    
    def get_author(self) -> str:
        return self.__author
    
    def get_date_published(self) -> datetime.date:
        return self.__date_published