from contact import Contact


class ContactBook:
    def __init__(self):
        self.contacts = []

    @classmethod
    def get_populated_contact_book(cls):
        book = ContactBook()
        contact1 = Contact(1, "john doe", "john@gmail.com", "9812345667")
        contact2 = Contact(2, "jane doe", "jane@gmail.com", "9812345667")
        contact3 = Contact(3, "jonah doe", "jonah@gmail.com", "9812345667")
        contact4 = Contact(4, "james doe", "james@gmail.com", "9812345667")
        contact5 = Contact(5, "jamie doe", "jamie@gmail.com", "9812345667")

        book.add_contact(contact1)
        book.add_contact(contact2)
        book.add_contact(contact3)
        book.add_contact(contact4)
        book.add_contact(contact5)
        return book

    def add_contact(self, contact):
        self.contacts.append(contact)

    def remove_contact(self, contact_id):
        self.contacts = list(filter(lambda contact: not (
            contact.id == contact_id), self.contacts))

    def display_table(self):
        print("SN   | Name              | Email                 | Phone")
        print("-----+-------------------+-----------------------+-----------------")
        for contact in self.contacts:
            print(f"{contact.id}" +
                  " "*(5 - len(str(contact.id))) +
                  "|" + f" {contact.name}" +
                  " "*(18 - len(contact.name)) +
                  "|" + f" {contact.email}" +
                  " "*(22 - len(contact.email)) +
                  "|" + f" {contact.phone}" +
                  " "*(18 - len(contact.phone))
                  )

    def view_contacts(self, page, no_of_contacts):
        to_be_printed = self.contacts[page: page + no_of_contacts]
        for contact in to_be_printed:
            print(contact)

    def populate(self):
        contact1 = Contact(1, "john doe", "john@gmail.com", "9812345667")
        contact2 = Contact(2, "jane doe", "jane@gmail.com", "9812345667")
        contact3 = Contact(3, "jonah doe", "jonah@gmail.com", "9812345667")
        contact4 = Contact(4, "james doe", "james@gmail.com", "9812345667")
        contact5 = Contact(5, "jamie doe", "jamie@gmail.com", "9812345667")

        self.add_contact(contact1)
        self.add_contact(contact2)
        self.add_contact(contact3)
        self.add_contact(contact4)
        self.add_contact(contact5)

    def check_duplicate_id(self, id):
        for contact in self.contacts:
            if id == contact.get_id():
                return True
        return False

    def get_total_pages(self, contact_per_page):
        return len(self.contacts) / contact_per_page + 1
