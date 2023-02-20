from enum import IntEnum, auto
import time
import datetime
from api_library.library import Library
from api_library.book.book_type import BookType

from app_library.utils import (
    get_input_from_user_str,
    get_input_from_user_int,
    get_input_from_user_date
)

class _Actions(IntEnum):
    CUSTOMER_ADD = 1
    CUSTOMER_FIND_BY_NAME = auto()
    CUSTOMER_DISPLAY_LOANS = auto()
    CUSTOMER_DELETE = auto()
    BOOK_ADD = auto()
    BOOK_FIND_BY_NAME = auto()
    BOOK_FIND_BY_AUTHOR = auto()
    BOOK_LOAN = auto()
    BOOK_RETURN = auto()
    BOOK_DELETE = auto()
    DISPLAY_ALL_CUSTOMERS = auto()
    DISPLAY_ALL_BOOKS = auto()
    DISPLAY_ALL_LOANS = auto()
    DISPLAY_ALL_LATE_LOANS = auto()
    EXIT_PROGRAM = auto()

    def get_description(self) -> str:
        actions_desc: tuple = (
            "Add new customer",
            "Find customer by name",
            "Display customer loans",
            "Delete existing customer",
            "Add new book",
            "Find books by name",
            "Find books by author",
            "Loan a book",
            "Return a book",
            "Delete existing book",
            "Display all customers",
            "Display all books",
            "Display all loans",
            "Display all late loans",
            "Exit Program"
        )

        return actions_desc[self.value - 1]

class LibraryApp:
    def __init__(self, library_name: str, file_database: str) -> None:
        self.__library_name: str = library_name
        self.__library: Library = Library(file_database)
        self.__user_action = None

    def run(self) -> None:
        while True:
            time.sleep(2.0)
            self.__print_start_message()
            self.__print_main_menu()

            try:
                self.__get_action_from_user()
                self.__execute_action()
            except KeyboardInterrupt:
                self.__library.save()

    def stop(self) -> None:
        self.__library.save()
        exit()

    def __print_start_message(self) -> None:
        print("\n")
        print(f"......... [ {self.__library_name} Library ] ..........")

    def __print_main_menu(self) -> None:
        for action in _Actions:
            print(f"{action.value}. {action.get_description()}")

    def __get_action_from_user(self) -> None:
        while True:
            self.__user_action = input("> Enter action number: ")

            if not self.__user_action.isdigit():
                print("Error: Invalid action.")
                continue

            self.__user_action = int(self.__user_action)

            if self.__user_action not in range(1, len(_Actions) + 1):
                print("Error: Invalid action number.")
                continue

            break

    def __display_customer(self, customer_id: int) -> None:
        customer = None

        try:
            customer = self.__library.get_customer_by_id(customer_id)

            print(f"""
            - Customer (ID: {customer_id})
                > Name: {customer.get_name()}
                > Address: {customer.get_address()}
                > Email: {customer.get_email()}
                > Birth date: {customer.get_birth_date().strftime("%d.%m.%Y")}
        """)
        except Exception as error:
            print(error)

    def __display_book(self, book_id: int) -> None:
        book = None

        try:
            book = self.__library.get_book_by_id(book_id)

            print(f"""
                - Book (ID: {book_id})
                    > Name: {book.get_name()}
                    > Author: {book.get_name()}
                    > Publish date: {book.get_date_published().strftime("%d.%m.%Y")}
                    > Max loan time: {str(book.get_max_loan_time().days)} day(s)
            """)
        except Exception as error:
            print(error)

    def __display_loan(self, book_id: int) -> None:
        book = None

        try:
            book = self.__library.get_book_by_id(book_id)
            loan = self.__library.get_loan(book_id)
            customer = self.__library.get_customer_by_id(loan.get_customer_id())

            print(f"""
                - Loan (Book ID: {book_id})
                    > Loaned to: {customer.get_name()} (ID: {customer.get_id()})
                    > Loan date: {loan.get_loan_date().strftime("%d.%m.%Y")}
                    > Return date: {loan.get_return_date().strftime("%d.%m.%Y")}
            """)
        except Exception as error:
            print(error)

    def __execute_action(self) -> None:
        action = self.__user_action

        match action:
            case _Actions.EXIT_PROGRAM:
                self.stop()

            case _Actions.CUSTOMER_ADD:
                print("\n... Add new customer")

                while True:
                    customer_id: int = get_input_from_user_int("customer ID")
                    customer_name: str = get_input_from_user_str("customer name")
                    customer_address: str = get_input_from_user_str("customer address")
                    customer_email: str = get_input_from_user_str("customer email")
                    customer_birth_date: datetime.date = get_input_from_user_date("customer birth date", "%d.%m.%Y")

                    try:
                        self.__library.add_customer(customer_id, customer_name, customer_address, 
                                                    customer_email, customer_birth_date)
                        
                        print(f"Customer (ID: {customer_id}, Name: {customer_name}) created.")
                    except Exception as error:
                        print(error)
                        continue

                    break

            case _Actions.CUSTOMER_FIND_BY_NAME:
                print("\n... Find customer by name")

                while True:
                    customer_name: str = get_input_from_user_str("customer name")
                    customer = None

                    try:
                        customer = self.__library.get_customer_by_name(customer_name)
                        self.__display_customer(customer.get_id())
                    except Exception as error:
                        print(error)
                        continue

                    break

            case _Actions.CUSTOMER_DISPLAY_LOANS:
                print("\n... Display customer loans")

                while True:

                    customer_id: int = get_input_from_user_int("customer id")
                    customer = None

                    try:
                        customer = self.__library.get_customer_by_id(customer_id)
                    except Exception as error:
                        print(error)
                        continue

                    break

                customer_loans = self.__library.get_customer_loans(customer_id)

                if not len(customer_loans):
                    print(f"[X] Customer (ID: {customer_id}) has no loans.")
                else:
                    for loan in customer_loans:
                        self.__display_loan(loan.get_book_id())

            case _Actions.CUSTOMER_DELETE:
                print("\n... Delete customer")

                while True:
                    customer_id: int = get_input_from_user_int("customer id")
                    customer = None

                    try:
                        customer = self.__library.get_customer_by_id(customer_id)
                    except Exception as error:
                        print(error)
                        continue

                    break

                self.__display_customer(customer_id)

                try:
                    self.__library.remove_customer(customer_id)
                    print(f"[V] Customer (ID: {customer_id}) deleted.")
                except Exception as error:
                    print(error)

            case _Actions.BOOK_ADD:
                print("\n... Add new book")

                while True:
                    book_id: int = get_input_from_user_int("book ID")
                    book_type = None

                    print("> Avaliable book types: ")

                    for b_type in BookType:
                        print(b_type.get_description())

                    while True:
                        temp_value: int = get_input_from_user_int("book type")

                        for i in set(i for i in BookType):
                            if temp_value != i.value:
                                continue

                            book_type = i
                            break
                        
                        if book_type is None:
                            continue

                        break

                    book_name: str = get_input_from_user_str("book name")
                    book_author: str = get_input_from_user_str("book author")
                    book_date_published: datetime.date = get_input_from_user_date("book publish date", "%d.%m.%Y")

                    try:
                        self.__library.add_book(book_id, book_type, book_name, 
                                                book_author, book_date_published)
                        
                        print(f"Book (ID: {book_id}) created.")
                    except Exception as error:
                        print(error)
                        continue

                    break

            case _Actions.BOOK_FIND_BY_NAME:
                print("\n... Find book by name")

                book_name: str = get_input_from_user_str("book name")
                books = self.__library.get_books_by_name(book_name)
                books_count: int = len(books)

                print(f"... Searching for books with name '{book_name}'")

                if not books_count:
                    print(f"[X] There are no books with name '{book_name}'")

                print(f"[V] Found {books_count} book(s) with name '{book_name}'")

                for book in books:
                    self.__display_book(book.get_id())

            case _Actions.BOOK_FIND_BY_AUTHOR:
                print("\n... Find book by author")

                book_author: str = get_input_from_user_str("book author")
                books = self.__library.get_books_by_author(book_author)
                books_count: int = len(books)

                print(f"... Searching for books with author '{book_author}'")

                if not books_count:
                    print(f"[X] There are no books with author '{book_author}'")

                print(f"[V] Found {books_count} book(s) with author '{book_author}'")

                for book in books:
                    self.__display_book(book.get_id())

            case _Actions.BOOK_LOAN:
                print("\n... Loan a book")

                book_id: int
                customer_id: int
                loan_return_date = None

                while True:
                    book_id = get_input_from_user_int("book id")
                    book = None

                    try:
                        book = self.__library.get_book_by_id(book_id)
                    except Exception as error:
                        print(error)
                        continue

                    break

                self.__display_book(book_id)
                temp_max_loan_time = book.get_type().get_max_loan_time().days

                while True:
                    customer_id: int = get_input_from_user_int("customer id")
                    customer = None

                    try:
                        customer = self.__library.get_customer_by_id(customer_id)
                    except Exception as error:
                        print(error)
                        continue

                    break

                self.__display_customer(customer_id)

                while True:
                    print("Date format for loan return: dd.mm.yyyy")
                    loan_return_date = get_input_from_user_str("loan return date")

                    try:
                        loan_return_date = datetime.datetime.strptime(loan_return_date, "%d.%m.%Y")
                    except Exception as error:
                        print(error)
                        continue

                    break
                
                try:
                    self.__library.loan_book(customer_id, book_id,
                        datetime.datetime.now(), loan_return_date)
                    
                    print(f"""
                        Book (ID: {book_id}) loaned to {customer.get_name()} (ID: {customer_id}).
                        Return date: {loan_return_date.strftime('%d.%m.%Y')}
                    """)
                except Exception as error:
                    print(f"[X] {error}")

            case _Actions.BOOK_RETURN:
                book_id: int

                while True:
                    book_id = get_input_from_user_int("book id")

                    try:
                        self.__library.return_book(book_id)
                        print(f"Book (ID: {book_id}) returned to library.")
                    except Exception as error:
                        print(error)
                        continue

                    break

            case _Actions.BOOK_DELETE:
                book_id: int

                while True:
                    book_id = get_input_from_user_int("book id")

                    try:
                        self.__library.remove_book(book_id)
                        print(f"Book (ID: {book_id}) deleted.")
                    except Exception as error:
                        print(error)
                        continue

                    break

            case _Actions.DISPLAY_ALL_CUSTOMERS:
                all_customers = self.__library.get_all_customers()

                if not len(all_customers):
                    print("... There are no customers in the library.")
                else:
                    print("\n... Displaying all customers")

                    for customer in all_customers:
                        self.__display_customer(customer.get_id())

            case _Actions.DISPLAY_ALL_BOOKS:
                all_books = self.__library.get_all_books()

                if not len(all_books):
                    print("... There are no books in the library.")
                else:
                    print("\n... Displaying all books")

                    for book in all_books:
                        self.__display_book(book.get_id())

            case _Actions.DISPLAY_ALL_LOANS:
                all_loans = self.__library.get_all_loans()

                if not len(all_loans):
                    print("... There are no loans in the library.")
                else:
                    print("\n... Displaying all loans")

                    for loan in all_loans:
                        self.__display_loan(loan.get_book_id())

            case _Actions.DISPLAY_ALL_LATE_LOANS:
                all_late_loans = self.__library.get_all_late_loans()
                
                if not len(all_late_loans):
                    print("... There are no late loans in the library.")
                else:
                    print("\n... Displaying all late loans")

                    for loan in all_late_loans:
                        self.__display_loan(loan.get_book_id())
                
                