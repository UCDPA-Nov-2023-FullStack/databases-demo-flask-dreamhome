"""An educational example of a basic blog application using Flask and SQLAlchemy.

Note that we're using the simpler Legacy Query API in this example:
https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/legacy-query/
"""
from statistics import median, mean

from flask import Flask, render_template, redirect, request, url_for
from sqlalchemy import desc

from models import Bookings, Members, Facilities, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py and particularly the DBMS URI


with app.app_context():
    db.init_app(app)  # It connects the SQLAlchemy db object with the Flask app and the DBMS engine
    db.create_all()  # Create the database tables for all the models

# bookings routes
@app.route("/")
@app.route("/bookings")
def bookings():
    bookings = Bookings.get_bookings()
    #print(bookings[:5])
    #return render_template("bookings.html", bookings=Bookings.query.order_by(desc(Bookings.starttime)).all())
    return render_template("bookings.html", bookings=bookings)

@app.route("/bookings/search", methods=['GET'])
def search_bookings():
    print(request.form)
    bookings = Bookings.get_bookings()
    return render_template("bookings.html", bookings=bookings)
  
@app.route("/bookings/<int:book_id>")
def booking_details(book_id):
    booking = Bookings.query.get_or_404(book_id)
    member = Members.query.get(booking.memid)
    facility = Facilities.query.get(booking.facid)
    return render_template("booking_details.html", booking=booking, member=member, facility=facility)

@app.route("/bookings/create", methods=["GET"])
def create_booking():
    return render_template("create_booking.html", members=Members.query.all(), facilities=Facilities.query.all())

@app.route("/bookings/create", methods=["POST"])
def create_booking_action():
    booking = Bookings(
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
    booking = Bookings.query.get_or_404(book_id)
    members = Members.query.all()
    facilities = Facilities.query.all()
    return render_template("edit_booking.html", booking=booking, members=members, facilities=facilities)

@app.route("/bookings/<int:book_id>/edit", methods=["POST"])
def edit_booking_action(book_id):
    #bookid = request.form['book_id']
    booking = Bookings.query.get(book_id)
    booking.memid = request.form['member'],
    booking.facid = request.form['facility'],
    booking.starttime = request.form['starttime'],
    booking.slots = request.form['slots'],
    
    db.session.commit()

    return redirect(url_for("bookings"))

@app.route("/bookings/<int:book_id>/delete", methods=["GET"])
def booking_delete_action(book_id):
    booking = Bookings.query.get(book_id)
    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for("bookings"))

# members routes
@app.route("/members")
def members():
    return render_template("members.html", members=Members.query.all())

@app.route("/members/<int:mem_id>")
def member_details(mem_id):
    member = Members.query.get_or_404(mem_id)
    return render_template("member_details.html", member=member)


# facilities routes
@app.route("/facilities")
def facilities():
    return render_template("facilities.html", facilities=Facilities.query.all())

@app.route("/facilities/<int:fac_id>")
def facility_details(fac_id):
    facility = Facilities.query.get_or_404(fac_id)
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
