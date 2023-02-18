from menu import Menu
from contact_book import ContactBook

# contact_book = ContactBook()
# contact_book.populate()
contact_book = ContactBook.get_populated_contact_book()
m = Menu(contact_book)
m.home()
