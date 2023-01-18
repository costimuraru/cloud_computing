from flask_login import UserMixin



class User(UserMixin):
    def __init__(self, _id, password, email, firstname, phone_number, notes, sms_code):
        self._id = _id
        self.password = password
        self.email = email
        self.firstname = firstname
        self.phone_number = phone_number

    def get_id(self):
        return self._id

def map_user_db_to_domain(user_data):
    return User(user_data['_id'], user_data['password'], user_data['email'], user_data['first_name'], user_data['phone_number'], user_data['notes'], user_data['sms_code'])

