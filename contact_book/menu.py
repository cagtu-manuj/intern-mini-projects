import os
from contact_book import ContactBook
from contact import Contact


class Menu:
    def __init__(self, contact_book):
        self.page = 0
        self.no_of_contact = 3
        self.contact_book: ContactBook = contact_book

    def display_home(self):
        print("Select 1-3:")
        print("1.Add Contact")
        print("2.Delete Contact")
        print("3.View Contacts")
        print("4.Display Table")
        print("5.Exit")

    def home(self):
        os.system("clear")
        self.display_home()
        choice = ""
        while choice != "5":
            choice = input()
            match choice:
                case "1":
                    self.add_contact()
                case "2":
                    self.remove_contact()
                case "3":
                    self.view_contacts()
                case "4":
                    self.display_table()
                case "5":
                    exit(0)
                case _:
                    pass
            os.system("clear")
            self.display_home()

    def change_page(self, number):
        self.page += number
        if self.page < 0 or self.page > self.contact_book.get_total_pages(self.no_of_contact):
            self.page -= number

    def add_contact(self):
        os.system("clear")
        id = input("Enter id:")
        name = input("Enter name:")
        email = input("Enter email:")
        phone = input("Enter phone number:")
        contact = Contact(id=id, name=name, email=email, phone=phone)
        self.contact_book.add_contact(contact)
        os.system("clear")

    def remove_contact(self):
        os.system("clear")
        id = int(input("Enter contact id to be removed: "))
        self.contact_book.remove_contact(id)
        os.system("clear")

    def view_contacts(self):
        self.contact_book.view_contacts(self.page, self.no_of_contact)
        print("")
        print("")
        print("<<Prev [P]\t\tExit[E]\t\tNext[N]>>")
        choice = ""
        while choice.lower() != "e":
            choice = input()
            match choice.lower():
                case "p":
                    self.change_page(-1)
                case "n":
                    self.change_page(1)
                case  _:
                    pass
            os.system("clear")
            self.contact_book.view_contacts(self.page, self.no_of_contact)
            print("")
            print("")
            print("<<Prev [P]\t\tExit[E]\t\tNext[N]>>")

        os.system("clear")

    def display_table(self):
        os.system("clear")
        self.contact_book.display_table()
        print("")
        print("")
        print("Press E to exit")
        choice = ""
        while choice.lower() != "e":
            choice = input()

    def set_contacts_per_page(self, n: int):
        if n <= 0:
            return
        self.no_of_contact = n
