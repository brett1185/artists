from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Picture:
    db='paintings_db'
    @staticmethod
    def validate_picture(picture):
        is_valid=True
        if len(picture['title']) < 2:
            flash('location must be at least 2 characters', 'picture')
            is_valid=False
        if len(picture['description']) < 10:
            flash('description must be at least 10 characters long','picture')
            is_valid=False
        if len(picture ['price']) < 1:
            flash('Price must be greater than 0', 'picture')
            is_valid=False
        return is_valid

    def __init__(self, data):
        self.id=data['id']
        self.title=data['title']
        self.description=data['description']
        self.price=data['price']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']

    @classmethod
    def save(cls,data):
        query='insert into paintings (title, description, price, user_id) values (%(title)s, %(description)s, %(price)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query='select * from paintings join users on users.id=paintings.user_id;'
        results=connectToMySQL(cls.db).query_db(query)
        all_paintings=[]
        for i in results:
            all_paintings.append(cls(i))
        return all_paintings
    
    @classmethod
    def get_one(cls, data):
        query='select * from paintings where id=%(id)s;'
        results=connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query='update paintings set title=%(title)s, description=%(description)s, price=%(price)s, updated_at=now(), user_id=%(user_id)s where id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def delete(cls, data):
        query='delete from paintings where id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
