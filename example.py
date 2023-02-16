from app_library.app_library import LibraryApp

def main():
    app_library: LibraryApp = LibraryApp("John Bryce", "library_john_bryce") 
    app_library.run()

if __name__ == "__main__":
    main()