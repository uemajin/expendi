class User():

    def __init__(self, user_id, username, fullname, photo, password_hash, salt, preferred_currency):
        self.user_id = user_id
        self.username = username
        self.fullname = fullname
        self.photo = photo
        self.password_hash = password_hash  
        self.salt = salt
        self.preferred_currency = preferred_currency

    def info(self):

        return {
            "user_id": self.user_id,
            "username": self.username,
            "fullname": self.fullname,
            "photo": self.photo,
            "preferred_currency": self.preferred_currency
        }