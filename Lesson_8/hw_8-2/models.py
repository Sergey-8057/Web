from mongoengine import Document, connect, BooleanField, StringField


connect(db='hw_8', host="mongodb+srv://goitlearn:group-12@cluster0.tyzjgqb.mongodb.net/?retryWrites=true&w=majority")


class Contact(Document):
    fullname = StringField()
    email = StringField()
    status = BooleanField(default=False)
