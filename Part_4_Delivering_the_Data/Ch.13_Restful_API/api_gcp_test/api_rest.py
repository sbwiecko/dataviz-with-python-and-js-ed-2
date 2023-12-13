from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy optimized for Flask
from flask_marshmallow import Marshmallow  # SQL -> JSON
import os

# Init app
app = Flask(__name__)
CORS(app) #allows requests from any domain to access the data server
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/data/nobel_winners_cleaned_api_test.db'
# relative path to the database file below
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/nobel_winners_cleaned_api_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


# create the databe that initially lacks a primary key
# for d in df_tosql.to_dict(orient='records'):
#    session.add(Winner(**d))
# session.commit()

class Winner(db.Model):
    __tablename__ = 'winners'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    country = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    date_of_death = db.Column(db.String)
    gender = db.Column(db.String)
    link = db.Column(db.String)
    name = db.Column(db.String)
    place_of_birth = db.Column(db.String)
    place_of_death = db.Column(db.String)
    text = db.Column(db.Text)
    year = db.Column(db.Integer)
    award_age = db.Column(db.Integer)

    def __repr__(self):
        return "<Winner(name='%s', category='%s', year='%s')>"\
            % (self.name, self.category, self.year)


# serializing with marshmallow
class WinnerSchema(ma.Schema):
    class Meta:
        model = Winner
        fields = (
            'category', 'country', 'date_of_birth', 'date_of_death', 
            'gender', 'link', 'name', 'place_of_birth', 'place_of_death', 
            'text', 'year', 'award_age'
        )


winner_schema = WinnerSchema()           # single records
winners_schema = WinnerSchema(many=True) # multiple records


@app.route("/")
def hello():
    """Return a friendly HTTP greeting.
    Returns:
        A string with the words 'Hello World!'.
    """
    return "Hello World!"


# adding RESTful API routes
@app.route('/winners/')
def winner_list():
    """
    This route fetches winners from the SQL database, using request arguments 
    to form the SQL query. So '/winners/?country=Australia&category=Physics' 
    fetches all winning Australian Physicists.
    """
    
    valid_filters = ('year', 'category', 'gender', 'country', 'name')
    filters = request.args.to_dict()
    args = {name: value for name, value in filters.items() if name in valid_filters}
    # This for loop does the same job as the dict comprehension above
    # for vf in valid_filters:
    #     if vf in filters:
    #         args[vf] = filters.get(vf)

    app.logger.info(f'Filtering with the fields: {args}')
    all_winners = Winner.query.filter_by(**args)
    result = winners_schema.jsonify(all_winners)
    return result

# posting data to the API
# see extending the API with MethodViews and paginating the data returns
@app.route('/winners/', methods=['POST'])
def add_winner():
    valid_fields = winner_schema.fields
    winner_data = {name: value for name, value in request.json.items() if name in valid_fields}
    app.logger.info(f"Creating a winner with these fields: {winner_data}")
    new_winner = Winner(**winner_data)
    db.session.add(new_winner)
    db.session.commit()
    return winner_schema.jsonify(new_winner)


@app.route('/winners/<id>/')
def winner_detail(id):
    winner = Winner.query.get_or_404(id)
    result = winner_schema.jsonify(winner)
    return result


@app.route('/winners/<id>/', methods=['PATCH'])
def update_winner(id):
    winner = Winner.query.get_or_404(id)
    valid_fields = winner_schema.fields
    winner_data = {name: value for name, value in request.json.items() if name in valid_fields}
    app.logger.info(f"Updating a winner with these fields: {winner_data}")
    for k, v in winner_data.items():
        setattr(winner, k, v)
    db.session.commit()
    return winner_schema.jsonify(winner)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
