class LibraryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CustomerException(LibraryException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BookException(LibraryException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LoanException(LibraryException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)