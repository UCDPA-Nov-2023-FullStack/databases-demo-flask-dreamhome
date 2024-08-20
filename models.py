from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class Bookings(db.Model):
    __table_args__ = {"schema": "cd"}
    bookid = db.mapped_column(db.Integer, primary_key=True)
    facid = db.mapped_column(db.Integer, primary_key=False)
    memid = db.mapped_column(db.Integer, primary_key=False)
    starttime = db.mapped_column(db.DateTime, default=datetime.utcnow)
    slots = db.mapped_column(db.Integer, primary_key=False)

    def __str__(self):
        return f'"{self.bookid}" at {self.facid} {self.memid} ({self.starttime:%Y-%m-%d}) {self.slots}'

    @staticmethod
    def get_bookings():
        # An example of how to use raw SQL inside a model
        sql = text("""select mems.firstname, mems.surname, bks.starttime, bks.slots, bks.bookid 
                        from cd.bookings bks inner join cd.members mems on mems.memid = bks.memid 
                        order by bks.starttime desc""")
        return db.session.execute(sql).all()  # Returns just the integers

class Members(db.Model):
    __table_args__ = {"schema": "cd"}
    joindate = db.mapped_column(db.DateTime, default=datetime.utcnow)
    zipcode = db.mapped_column(db.Integer, nullable=False)
    recommendedby = db.mapped_column(db.Integer, nullable=True)
    memid = db.mapped_column(db.Integer, primary_key=True)
    telephone = db.mapped_column(db.String(20), nullable=False)
    surname = db.mapped_column(db.String(200), nullable=False)
    firstname = db.mapped_column(db.String(200), nullable=False)
    address = db.mapped_column(db.String(300), nullable=False)


class Facilities(db.Model):
    __table_args__ = {"schema": "cd"}
    facid = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    membercost = db.mapped_column(db.Numeric, nullable=False)
    guestcost = db.mapped_column(db.Numeric, nullable=False)
    initialoutlay = db.mapped_column(db.Numeric, nullable=False)
    monthlymaintenance = db.mapped_column(db.Numeric, nullable=False)


    def __str__(self):
        return f'"{self.memid}", {self.zipcode}, {self.recommendedby}, {self.telephone}, {self.firstname}, {self.surname}, {self.address}, ({self.joindate:%Y-%m-%d}) '




#    @staticmethod
#    def get_post_lengths():
#        # An example of how to use raw SQL inside a model
#        sql = text("SELECT length(title) + length(content) FROM blog_post")
#        return db.session.execute(sql).scalars().all()  # Returns just the integers
