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
from flask_wtf import FlaskForm
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

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
  venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
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
  areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
  data = []

  for a in areas:
    result = Venue.query.filter(Venue.state == a.state).filter(Venue.city == a.city).all()
    venue_data = []
    for venue in result:
      venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(db.session.query(Show).filter(Show.date > datetime.now()).all())
      })

    data.append({
      'city': a.city,
      'state': a.state,
      'venues': venue_data
    })
  
    return render_template('pages/venues.html', areas=data)

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

  return render_template('pages/show_venue.html', venue=data)

# #  Create Venue
# #  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False

  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    # seeking_talent = True if 'seeking_talent' in request.form else False

    venue = Venue(name=name, city=city, state=state, phone=phone, address=address, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link)
    db.session.add(venue)
    db.session.commit()
    print(venue)

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)

  finally:
    db.session.close()

  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
  return render_template('pages/home.html')
  # # return jsonify(body)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter(Venue.id == venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')


  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database DONE
  data = Artist.query.order_by('name').all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  input_search = request.form.get('search_term')
  input = "%{}%".format(input_search.replace(" ", "\ "))
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".  DONE

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
    "count": len(results),
    "data": results
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')

  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id DONE

def show_artist(artist_id):
  data = Artist.query.filter_by(id=artist_id).first()

  shows_to_do = []
  done_shows = []
  for s in data.shows:
    if s.date > datetime.now():
      shows_to_do.append(s)
    else:
      done_shows.append(s)

  data.shows_to_do = shows_to_do
  data.done_shows = done_shows

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  input_artist = Artist.query.filter_by(id=artist_id).first()

  # TODO: populate form with fields from artist with ID <artist_id>

  form.name.data = input_artist.name
  form.city.data = input_artist.city
  form.phone.data = input_artist.phone
  form.facebook_link.data = input_artist.facebook_link
  form.website_link.data = input_artist.website_link
  form.image_link.data = input_artist.image_link
  form.genres.data = json.loads(input_artist.genres)

  return render_template('forms/edit_artist.html', form=form, artist=input_artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  # artist = Artist.query.filter_by(id=artist_id).first()
  artist = Artist.query.get(artist_id)
  
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.image_link = request.form['image_link']
    # artist.seeking_venue = True if 'seeking_venue' in request.form else False
    # artist.seeking_description = request.form['seeking_description']

    # db.session.add(json.load(artist))
    db.session.commit()

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)

  finally:
    db.session.close()

  if error:
    flash('errrrrrrrrrrrrrrrpppoooooooooooorrrr')
  if not error:
    flash('ddoooooooonnnnneeeeee')

  return jsonify(artist)
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
    flash('NOT DONE')
  else:
    flash('DONEEEE')

  
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
  error=False

  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website_link = request.form['website_link']
    image_link = request.form['image_link']

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, website_link=website_link, image_link=image_link)
    db.session.add(artist)
    db.session.commit()
    print(artist)

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)

  finally:
    db.session.close()

  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')


  # return jsonify(body)

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

  data = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()

  response = []

  for s in data:
    response.append({
       "venue_id": s.venue_id,
      "venue_name": s.venue.name,
      "artist_id": s.artist_id,
      "artist_name": s.artist.name,
      "artist_image_link": s.artist.image_link,
      "start_time": str(s.date)
    })

  
  return render_template('pages/shows.html', shows=response)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)



@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  
  error=False
  
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Show(artist_id=artist_id, venue_id=venue_id, date=start_time)
    db.session.add(show)
    db.session.commit()
    print(show)

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)

  finally:
    db.session.close()

  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')



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
