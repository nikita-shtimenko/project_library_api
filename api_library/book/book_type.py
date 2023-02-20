from enum import IntEnum
from datetime import timedelta

class BookType(IntEnum):
    BASIC = 1,
    STANDART = 2
    IMPORTANT = 3

    def get_max_loan_time(self) -> timedelta:
        LOAN_TYPE_MAX_TIME: dict[BookType, timedelta] = {
            self.BASIC: timedelta(days=10),
            self.STANDART: timedelta(days=5),
            self.IMPORTANT: timedelta(days=2)
        }

        return LOAN_TYPE_MAX_TIME[self]
    
    def get_description(self) -> str:
        LOAN_TYPE_DESCRIPTION: dict[BookType, str] = {
            self.BASIC: f"Number: {self.BASIC.value}, Name: {self.BASIC.name}, Time: {str(self.BASIC.get_max_loan_time().days)} day(s)",
            self.STANDART: f"Number: {self.STANDART.value}, Name: {self.STANDART.name}, Time: {str(self.STANDART.get_max_loan_time().days)} day(s)",
            self.IMPORTANT: f"Number: {self.IMPORTANT.value}, Name: {self.IMPORTANT.name}, Time: {str(self.IMPORTANT.get_max_loan_time().days)} day(s)"
        }

        return LOAN_TYPE_DESCRIPTION[self]