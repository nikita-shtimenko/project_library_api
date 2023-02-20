import os
import pickle
import datetime
from api_library.customer import Customer
from api_library.book.book import Book
from api_library.book.book_type import BookType
from api_library.loan import Loan

from api_library.exceptions import (
    LibraryException,
    CustomerException,
    BookException,
    LoanException
)

class Library:
    def __init__(self, file_database: str) -> None:
        self.__file_database: str = f"{file_database}.pickle"
        self.__customers: dict[int, Customer] = dict()
        self.__books: dict[int, Book] = dict()
        self.__loans: dict[int, Loan] = dict()

        if not os.path.exists(self.__file_database):
            self.save()
        else:
            self.__load()

    def __load(self) -> None:
        with open(self.__file_database, "rb") as file_handler:
            temp_data = pickle.load(file_handler)
            self.__dict__.update(temp_data)

    def save(self) -> None:
        try:
            with open(self.__file_database, "wb") as file_handler:
                pickle.dump(self.__dict__, file_handler)
                file_handler.close()
        except Exception as file_exception:
            raise LibraryException(file_exception)

    def __is_customer_exists(self, customer_id: int) -> bool:
        return customer_id in self.__customers

    def add_customer(self, customer_id: int, name: str, address: str, 
                    email: str, birth_date: datetime.date) -> None:
        
        if self.__is_customer_exists(customer_id):
            raise CustomerException(f"Customer (ID: {customer_id}) already exists.")
        
        self.__customers[customer_id] = Customer(customer_id, name, address, email, birth_date)

    def get_customer_by_id(self, customer_id: int) -> Customer:
        if not self.__is_customer_exists(customer_id):
            raise CustomerException(f"Customer (ID: {customer_id}) does not exists.")
        
        return self.__customers[customer_id]

    def get_customer_by_name(self, name: str) -> Customer:
        return_customer = None

        for customer in self.__customers.values():
            if customer.get_name() != name:
                continue

            return_customer = customer
            break

        if return_customer is None:
            raise CustomerException(f"Customer (Name: {name}) does not exists.")
        
        return return_customer

    def get_customer_loans(self, customer_id: int) -> tuple[Loan]:
        if not self.__is_customer_exists(customer_id):
            raise CustomerException(f"Customer (ID: {customer_id}) does not exists.")
        
        return tuple(i for i in self.__loans.values() if i.get_customer_id() == customer_id)
    
    def remove_customer(self, customer_id: int) -> None:
        if not self.__is_customer_exists(customer_id):
            raise CustomerException(f"Customer (ID: {customer_id}) does not exists.")
        
        customer_loans: tuple[Loan] = self.get_customer_loans(customer_id)

        for loan in customer_loans:
            temp_book_id: int = loan.get_book_id()
            del self.__loans[temp_book_id]
        
        del self.__customers[customer_id]

    def get_all_customers(self) -> tuple[Customer]:
        return tuple(self.__customers.values())

    def __is_book_exists(self, book_id: int) -> bool:
        return book_id in self.__books
    
    def add_book(self, book_id: int, book_type: BookType, 
                name: str, author: str, date_published: datetime.date) -> None:
        
        if self.__is_book_exists(book_id):
            raise BookException(f"Book (ID: {book_id}) already exists.")
        
        self.__books[book_id] = Book(book_id, book_type, name, author, date_published)

    def remove_book(self, book_id: int) -> None:
        if not self.__is_book_exists(book_id):
            raise BookException(f"Book (ID: {book_id}) does not exists.")
        
        if book_id in self.__loans:
            del self.__loans[book_id]

        del self.__books[book_id]
        
    def get_book_by_id(self, book_id: int) -> Book:
        if not self.__is_book_exists(book_id):
            raise BookException(f"Customer (ID: {book_id}) does not exists.")
        
        return self.__books[book_id]

    def get_books_by_name(self, name: str) -> tuple[Book]:
        return tuple(i for i in self.__books.values() if i.get_name() == name)
    
    def get_books_by_author(self, author: str) -> tuple[Book]:
        return tuple(i for i in self.__books.values() if i.get_author() == author)

    def get_all_books(self) -> tuple[Book]:
        return tuple(self.__books.values())

    def is_book_loaned(self, book_id: int) -> bool:
        return book_id in self.__loans
    
    def loan_book(self, customer_id: int, book_id: int, loan_date: datetime.date, 
                return_date: datetime.date) -> None:
        
        if not self.__is_customer_exists(customer_id):
            raise CustomerException(f"Customer (ID: {customer_id}) does not exists.")
        
        if not self.__is_book_exists(book_id):
            raise BookException(f"Book (ID: {book_id}) does not exists.")

        if self.is_book_loaned(book_id):
            raise LoanException(f"Book (ID: {book_id}) is already loaned.")
        
        if loan_date > return_date:
            raise LoanException(f"Loan return date can not be earlier than loan date.")
        
        temp_book_max_loan_time: datetime.timedelta = self.__books[book_id].get_type().get_max_loan_time()
        
        if return_date - loan_date > temp_book_max_loan_time:
            raise LoanException(f"Maximum loan time for book (ID: {book_id}) is {temp_book_max_loan_time.days} day(s).")
        
        self.__loans[book_id] = Loan(customer_id, book_id, loan_date, return_date)

    def return_book(self, book_id: int) -> None:
        if not self.__is_book_exists(book_id):
            raise BookException(f"Book (ID: {book_id}) is not exists.")
        
        if not self.is_book_loaned(book_id):
            raise LoanException(f"Book (ID: {book_id}) is not loaned.")
        
        del self.__loans[book_id]

    def get_loan(self, book_id: int) -> Loan:
        if not self.is_book_loaned(book_id):
            raise LoanException(f"Book (ID: {book_id}) is not loaned.")
        
        return self.__loans[book_id]
        
    def get_all_loans(self) -> tuple[Loan]:
        return tuple(self.__loans.values())
    
    def get_all_late_loans(self) -> tuple[Loan]:
        return tuple(i for i in self.__loans.values() if datetime.datetime.now() > i.get_return_date())