from datetime import date

class Loan:
    def __init__(self, customer_id: int, book_id: int, loan_date: date, 
                return_date: date) -> None:
        
        self.__customer_id: int = customer_id
        self.__book_id: int = book_id
        self.__loan_date: date = loan_date
        self.__return_date: date = return_date

    def get_customer_id(self) -> int:
        return self.__customer_id
    
    def get_book_id(self) -> int:
        return self.__book_id

    def get_loan_date(self) -> date:
        return self.__loan_date
    
    def get_return_date(self) -> date:
        return self.__return_date
        