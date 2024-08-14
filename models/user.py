import json
import bcrypt
from flask_login import UserMixin
from flask_principal import RoleNeed, Permission, Principal

USER_DATA_PATH = 'data/user.json'
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

class User(UserMixin):
    def __init__(self, id, fullname, email, password, role):
        self.id = id
        self.fullname = fullname
        self.email = email
        self.password = password
        self.role = role

    @classmethod
    def load_users(cls):
        try:
            with open(USER_DATA_PATH, 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []
        return users

    @classmethod
    def save_users(cls, users):
        with open(USER_DATA_PATH, 'w') as f:
            json.dump(users, f)

    @classmethod
    def get(cls, email):
        users = cls.load_users()
        for user in users:
            if user['email'] == email:
                return cls(
                    id=user['id'],
                    fullname=user.get('fullname', user['email']),
                    email=user['email'],
                    password=user['password'],
                    role=user.get('role', 'user')
                )
        return None

    @classmethod
    def get_role(cls, email):
        users = cls.load_users()
        for user in users:
            if user['email'] == email:
                return user.get('role', 'user')
        return 'user'

    @classmethod
    def validate_password(cls, email, password):
        user = cls.get(email)
        hash_password = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        if hash_password == False:
            return None
        if user and hash_password:
            return user
        return None

    @classmethod
    def create(cls, fullname, email, password, role='user'):
        users = cls.load_users()
        same_email = 0
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        for user in users:
            if email == user['email']:
                same_email += 1
        if same_email == 0:
            user_id = len(users) + 1
            users.append({
                'id': user_id,
                'email': email,
                'fullname': fullname,
                'password': password.decode('utf-8'),
                'role': role
            })
            cls.save_users(users)
            return cls(user_id, fullname, email, password.decode('utf-8'), role)             
        return None

    @classmethod
    def update_password(cls, email, new_password):
        users = cls.load_users()
        new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        for user in users:
            if email == user['email']:
                user['password'] = new_password.decode('utf-8')
                cls.save_users(users)
                user_data = user
                return cls(
                    id=user_data['id'],
                    fullname=user_data['fullname'],
                    email=email,
                    password=new_password.decode('utf-8'),
                    role=user_data.get('role', 'user')
                )
        return None

    @classmethod
    def delete(cls, email):
        users = cls.load_users()
        for i, user in enumerate(users):
            if email == user['email']:
                del users[i]  # Hapus elemen dari list berdasarkan indeks
                cls.save_users(users)
                return True
        return False
