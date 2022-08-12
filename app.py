#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from jinja2 import Markup
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')



# TODO: connect to a local postgresql database  DONE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:olatunji@localhost:5432/fyyurproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=False)

    def __repr__(self):
      return f'<Venue: {self.id}, name: {self.name}, city: {self.city}, state:{self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, genres: {self.genres}, website_link: {self.website_link}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate DONE

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=False)

    def __repr__(self):
      return f'<Artist: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, website_link: {self.website_link}, description: {self.description}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate   DONE

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__='show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.String(), db.ForeignKey("venue.id"), nullable=False)
  artist_id = db.Column(db.String(), db.ForeignKey("artist.id"), nullable=False)
  date = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show: {self.id}, venue_id: {self.venue_id}, artist_id: {self.artist_id}, date: {self.date}>'





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=Venue.query.all()
  print(data)
  # [{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_word = request.form.get('search_term')
  lost = "%{}%".format(search_word.replace(" ", "\ "))
  data = Venue.query.filter(Venue.name.match(lost)).order_by('name').all()

  wanted = []
  for p in data:
    want = {
      "id": p.id,
      "name": p.name,
      "num_upcoming_shows": len(p.shows)
    }
    wanted.append(want)
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": len(wanted),
    "data": wanted
    # "count": 1,
    # "data": [{
    #   "id": 2,
    #   "name": "The Dueling Pianos Bar",
    #   "num_upcoming_shows": 0,
    # }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.filter_by(id=venue_id).first()
  data.genres = json.loads(data.genres)
  shows_to_do = []
  shows_done = []
  for s in data.shows:

    if s.date > datetime.now():
      shows_to_do.append(s)
    else:
      shows_done.append(s)
    data.shows_to_do = shows_to_do
    data.shows_done = shows_done




  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
#   data1={
#     "id": 1,
#     "name": "The Musical Hop",
#     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#     "address": "1015 Folsom Street",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "123-123-1234",
#     "website": "https://www.themusicalhop.com",
#     "facebook_link": "https://www.facebook.com/TheMusicalHop",
#     "seeking_talent": True,
#     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     "past_shows": [{
#       "artist_id": 4,
#       "artist_name": "Guns N Petals",
#       "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#       "start_time": "2019-05-21T21:30:00.000Z"
#     }],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
#   }
#   data2={
#     "id": 2,
#     "name": "The Dueling Pianos Bar",
#     "genres": ["Classical", "R&B", "Hip-Hop"],
#     "address": "335 Delancey Street",
#     "city": "New York",
#     "state": "NY",
#     "phone": "914-003-1132",
#     "website": "https://www.theduelingpianos.com",
#     "facebook_link": "https://www.facebook.com/theduelingpianos",
#     "seeking_talent": False,
#     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#     "past_shows": [],
#     "upcoming_shows": [],
#     "past_shows_count": 0,
#     "upcoming_shows_count": 0,
#   }
#   data3={
#     "id": 3,
#     "name": "Park Square Live Music & Coffee",
#     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#     "address": "34 Whiskey Moore Ave",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "415-000-1234",
#     "website": "https://www.parksquarelivemusicandcoffee.com",
#     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#     "seeking_talent": False,
#     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "past_shows": [{
#       "artist_id": 5,
#       "artist_name": "Matt Quevedo",
#       "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#       "start_time": "2019-06-15T23:00:00.000Z"
#     }],
#     "upcoming_shows": [{
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-01T20:00:00.000Z"
#     }, {
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-08T20:00:00.000Z"
#     }, {
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-15T20:00:00.000Z"
#     }],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 1,
#   }
#   data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

# #  Create Venue
# #  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  app = Flask(__name__)
  error - False
  body = {}
  data_received = request.get_json()
  try:
    name = data_received['name']
    city = data_received['city']
    state = data_received['state']
    address = data_received['address']
    phone = data_received['phone']
    genres = json.dumps(data_received['genres'])
    facebook_link = data_received['facebook_link']
    image_link = data_received['image_link']
    website_link = data_received['website_link']
    seeking_talent = data_received['seeking_talent']

    venue = Venue(name=name, city=city, state=state, phone=phone, address=address, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link)
    db.session.add(venue)
    db.session.commit()

  except:
    db.session.rollback()
    error=True

  finally:
    db.session.close()

  if error:
    abort(500)
    body['success']=False
    # body['msg']='errrrrorrorrrr'  JNSDJKJFKJKFBVKJDFNB,FDJ
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  else:
    body['success']=True
    # body['msg']='venue created successfully'  NDKJNDFKJKJKVGNFKJGVNFJNGVFKJ
    flash('Venue ' + request.form['name'] + ' was successfully listed!')


# return jsonify(body)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
# return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by('name').all()


  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  input_search = request.form.get('search_term')
  input = "%{}%".format(input_search.replace(" ", "\ "))
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  data = Artist.query.filter(Artist.name.match(input)).order_by('name').all()
  results = []
  for r in data:
    extra={
      "id": r.id,
      "name": r.name,
      "num_upcoming_shows": len(r.shows)
    }
    results.append(extra)
  response = {
    "count": len(resuits),
    "data": results
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')

  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

def show_artist(artist_id):
  data = Artist.query.filter_by(id=artist_id).first()
  data.genres = json.loads(data.genres)
  shows_to_do = []
  shows_done = []
  for s in data.shows:
    if s.date > datetime.now():
      shows_to_do.append(s)
    else:
      shows_done.append(s)

  data.shows_to_do = shows_to_do
  data.shows_done = shows_done



  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]


  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  input_artist = Artist.query.filter_by(id=artist_id).first()

  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>

  form.name.data = input_artist.name
  form.city.data = input_artist.city
  form.phone.data = input_artist.phone
  form.facebook_link.data = input_artist.facebook_link
  form.website.data = input_artist.website
  form.image_link.data = input_artist.image_link
  form.genres.data = json.loads(artist.genres)

  return render_template('forms/edit_artist.html', form=form, artist=input_artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  app = Flask(__name__)
  error = False
  body = {}
  data_received = request.get_json()
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    artist.name = data_received['name']
    artist.city = data_received['city']
    artist.state = data_received['state']
    artist.phone = data_received['phone']
    artist.genres = json.dumps(data_received['genres'])
    artist.facebook_link = data_received['facebook_link']
    artist.website = data_received['website']
    artist.image_link = data_received['image_link']

    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()

  if error:
    abort(500)
    body['success']=False
    # body['msg']='errrrrorrorrrr'  JNSDJKJFKJKFBVKJDFNB,FDJ
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  else:
    body['success']=True
    # body['msg']='venue created successfully'  NDKJNDFKJKJKVGNFKJGVNFJNGVFKJ
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return jsonify(body)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.address.data = venue.address
  form.facebook_link.data = venue.facebook_link
  form.website.data = venue.website
  form.image_link.data = venue.image_link
  form.genres.data = json.loads(venue.genres)
  
  
  # {
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  app = Flask(__name__)
  error=False
  body = {}
  data_received = request.get_json()
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    venue.name = data_received['name']
    venue.city = data_received['city']
    venue.state = data_received['state']
    venue.phone = data_received['phone']
    venue.address = data_received['address']
    venue.genres = json.dumps(data_received['genres'])
    venue.facebook_link = data_received['facebook_link']
    venue.website = data_received['website']
    venue.image_link = data_received['image_link']

    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()
  if error:
    abort(500)
    body['success']=False
    # body['msg']='errrrrorrorrrr'  JNSDJKJFKJKFBVKJDFNB,FDJ
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  else:
    body['success']=True
    # body['msg']='venue created successfully'  NDKJNDFKJKJKVGNFKJGVNFJNGVFKJ
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  
  return jsonify(body)

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  app = Flask(__name__)
  error=False
  body = {}
  data_received = request.get_json()
  try:
    name = data_received['name']
    city = data_received['city']
    state = data_received['state']
    phone = data_received['phone']
    genres = json.dumps(data_received['genres'])
    facebook_link = data_received['facebook_link']
    website = data_received['website']
    image_link = data_received['image_link']

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, website=website, image_link=image_link)
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()

  if error:
    abort(500)
    body['success']=False
    # body['msg']='errrrrorrorrrr'  JNSDJKJFKJKFBVKJDFNB,FDJ
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  else:
    body['success']=True
    # body['msg']='venue created successfully'  NDKJNDFKJKJKVGNFKJGVNFJNGVFKJ
    flash('Venue ' + request.form['name'] + ' was successfully listed!')


  return jsonify(body)

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  show_details = db.session.query(Show, Artist, Venue).join(Artist).join(Venue).filter(Show.date > datetime.now()).order_by('date').all()
  data=[]
  for r in rows:
    details = {
    "venue_id": r.Venue.id,
    "venue_name": r.Venue.name,
    "artist_id": r.Artist.id,
    "artist_name": r.Artist.name,
    "artist_image_link": r.Artist.image_link,
    "start_time": r.Show.date.strftime('%Y-%m-%d %H:%1')
    }
    data.append(details)
  
  
  # [{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]


  return render_template('pages/shows.html', shows=data)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)



@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  app = Flask(__name__)
  error=False
  body = {}
  data_received = request.get_json()
  try:
    artist_id = data_received['artist_id']
    venue_id = data_received['venue_id']
    start_time = data_received['start_time']

    show = Show(artist_id=artist_id, venue_id=venue_id, date=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()

  if error:
    abort(500)
    body['success']=False
    # body['msg']='errrrrorrorrrr'  JNSDJKJFKJKFBVKJDFNB,FDJ
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  else:
    body['success']=True
    # body['msg']='venue created successfully'  NDKJNDFKJKJKVGNFKJGVNFJNGVFKJ
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return jsonify(body) 



  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
