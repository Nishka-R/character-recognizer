from __init__ import db

def create_db():
    db.create_all()

class Prediction(db.Model):

    Entry = db.Column(db.Integer,primary_key=True)
    Character = db.Column(db.String(1),unique=False,nullable=False)

    def __repr__(self):
        return('<Prediction Hist %r>'% id)

if __name__ == '__main__':
    create_db()