class Contact:
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        s = f"""
        +----------------------------------------------------+
        | 🙍 {self.name}
        | 📧 {self.email}
        | 📞{self.phone}
        +----------------------------------------------------+
        """
        return s

    def get_id(self):
        return self.id
