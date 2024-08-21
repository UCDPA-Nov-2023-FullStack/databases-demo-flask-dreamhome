"""An educational example of a basic blog application using Flask and SQLAlchemy.

Note that we're using the simpler Legacy Query API in this example:
https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/legacy-query/
"""
from statistics import median, mean

from flask import Flask, render_template, redirect, request, url_for
from sqlalchemy import desc, or_

from models import Booking, Member, Facility, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py and particularly the DBMS URI


with app.app_context():
    db.init_app(app)  # It connects the SQLAlchemy db object with the Flask app and the DBMS engine
    db.create_all()  # Create the database tables for all the models

# bookings routes
@app.route("/")
@app.route("/bookings")
def bookings():
    # option 1 - using SQL and static method on Booking class
    #bookings = Booking.get_bookings()
    #return render_template("bookings.html", bookings=bookings)
    # option 2 - query() and all()
    #return render_template("bookings.html", bookings=Booking.query.order_by(desc(Booking.starttime)).all())
    # option 3 - pagination
    page = request.args.get('page', 1, type=int)
    pagination = Booking.query.order_by(desc(Booking.starttime)).paginate(page=page, per_page=12)
    return render_template("bookings.html", pagination=pagination)

@app.route("/bookings/search", methods=['GET'])
def search_bookings():
    query = request.args.get('q')
    #bookings = Booking.query.filter(Booking.facility.name.like(f'%{query}%')).all()
    #bookings = db.session.query(Booking).join(Facility).join(Member).filter(
    #    or_(Facility.name.ilike(f'%{query}%'), Member.firstname.ilike(f'%{query}%'), Member.surname.ilike(f'%{query}%'))).all()
    #return render_template("bookings.html", bookings=bookings, query=query)

    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Booking).join(Facility).join(Member).filter(
        or_(Facility.name.ilike(f'%{query}%'), Member.firstname.ilike(f'%{query}%'), Member.surname.ilike(f'%{query}%'))).paginate(page=page, per_page=12)
    return render_template("bookings.html", pagination=pagination, query=query)

@app.route("/bookings/<int:book_id>")
def booking_details(book_id):
    booking = Booking.query.get_or_404(book_id)
    return render_template("booking_details.html", booking=booking)

@app.route("/bookings/create", methods=["GET"])
def create_booking():
    return render_template("create_booking.html", members=Member.query.all(), facilities=Facility.query.all())

@app.route("/bookings/create", methods=["POST"])
def create_booking_action():
    booking = Booking(
        memid = request.form['member'],
        facid = request.form['facility'],
        starttime = request.form['starttime'],
        slots = request.form['slots'],
    )
    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("bookings"))

@app.route("/bookings/<int:book_id>/edit", methods=["GET"])
def booking_edit(book_id):
    booking = Booking.query.get_or_404(book_id)
    members = Member.query.all()
    facilities = Facility.query.all()
    return render_template("edit_booking.html", booking=booking, members=members, facilities=facilities)

@app.route("/bookings/<int:book_id>/edit", methods=["POST"])
def edit_booking_action(book_id):
    #bookid = request.form['book_id']
    booking = Booking.query.get(book_id)
    booking.memid = request.form['member'],
    booking.facid = request.form['facility'],
    booking.starttime = request.form['starttime'],
    booking.slots = request.form['slots'],
    
    db.session.commit()

    return redirect(url_for("bookings"))

@app.route("/bookings/<int:book_id>/delete", methods=["GET"])
def booking_delete_action(book_id):
    booking = Booking.query.get(book_id)
    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for("bookings"))

# members routes
@app.route("/members")
def members():
    return render_template("members.html", members=Member.query.all())

@app.route("/members/<int:mem_id>")
def member_details(mem_id):
    member = Member.query.get_or_404(mem_id)
    return render_template("member_details.html", member=member)


# facilities routes
@app.route("/facilities")
def facilities():
    return render_template("facilities.html", facilities=Facility.query.all())

@app.route("/facilities/<int:fac_id>")
def facility_details(fac_id):
    facility = Facility.query.get_or_404(fac_id)
    return render_template("facility_details.html", facility=facility)


#@app.route("/create", methods=["POST"])
#def create_post_action():
#    post = BlogPost(
#        title=request.form["title"],
#        content=request.form["content"],
#        author=request.form["author"],
#    )
#    db.session.add(post)
#    db.session.commit()
#    return redirect(url_for("index"))


#@app.route("/post/<int:post_id>")
#def post(post_id):
#    post = BlogPost.query.get_or_404(post_id)
#    return render_template("post.html", post=post)


#@app.route("/edit/<int:post_id>", methods=["GET"])
#def edit_page(post_id):
#    post = BlogPost.query.get_or_404(post_id)
#    return render_template("edit.html", post=post)


#@app.route("/edit/<int:post_id>", methods=["POST"])
#def edit_action(post_id):
#    post = BlogPost.query.get_or_404(post_id)
#    post.title = request.form["title"]
#    post.content = request.form["content"]
#    db.session.commit()
#    return redirect(url_for("post", post_id=post.id))


#@app.route("/delete/<int:post_id>", methods=["POST"])
#def delete_action(post_id):
#    post = BlogPost.query.get_or_404(post_id)
#    db.session.delete(post)
#    db.session.commit()
#    return redirect(url_for("index"))


#@app.route("/stats")
#def stats():
#    post_lengths = BlogPost.get_post_lengths()
#
#    return render_template(
#        "stats.html",
#        average_length=mean(post_lengths),
#        median_length=median(post_lengths),
#        max_length=max(post_lengths),
#        min_length=min(post_lengths),
#        total_length=sum(post_lengths),
#    )

# REST API 
#@app.route("/api/", methods=['GET'])
#def rest_index():
#    return jsonpickle.encode(BlogPost.query.all())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
