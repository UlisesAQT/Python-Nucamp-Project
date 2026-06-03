from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets
import sqlalchemy

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs. GET for all tweets
def index():
    users = User.query.all() # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize()) # build list of Tweets as dictionaries
    return jsonify(result) # return JSON response



@bp.route('/<int:id>', methods=['GET']) # this is a get for the individual tweet
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())



@bp.route('', methods=['POST'])
def create():
    if 'username' not in request.json or 'password' not in request.json:
         abort(400)

    # username must be at least 3 characters long
    # password must be at least 8 characters long
    if len(request.json['username']) < 3 or len(request.json['password']) < 8:
         abort(400)

    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )

    db.session.add(u)  
    db.session.commit()  

    return jsonify(u.serialize())



@bp.route('/<int:id>', methods=['DELETE']) 
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id):
    u = User.query.get_or_404(id)

    if 'username' in request.json:
        if len(request.json['username']) < 3:
            abort(400)
        u.username = request.json['username']

    if 'password' in request.json:
        if len(request.json['password']) < 8:
            abort(400)
        u.password = scramble(request.json['password'])
    
    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)


@bp.route('/<int:id>/liked_tweets',methods = ['GET'])
def liked_tweets(id:int):
    u = User.query.get_or_404(id)

    result = []
    for t in u.liked_tweets:
        result.append(t.serialize())
    return jsonify(result)






@bp.route('/<int:id>/users_like', methods = ['POST'])
def users_like(id:int):
    if 'tweet_id' not in request.json:
        abort(400)

    u = User.query.get_or_404(id)
    t = Tweet.query.get_or_404(request.json['tweet_id'])

    existing_like = db.session.execute(
        sqlalchemy.select(likes_table).where(
            likes_table.c.user_id == u.id,
            likes_table.c.tweet_id == t.id
        )
    ).first()

    if existing_like:
        return jsonify(False)

    stmt = sqlalchemy.insert(likes_table).values(
        user_id=u.id,
        tweet_id=t.id
        )
    
    db.session.execute(stmt)
    db.session.commit()


    return jsonify(True)

    
@bp.route('/<int:id>/users_unlike', methods=['DELETE'])
def users_unlike(id: int):

    u = User.query.get(id)

    tweet_id = request.json.get('tweet_id') if request.json else None
    t = Tweet.query.get(tweet_id) if tweet_id else None

    if not u or not t:
        return jsonify("missing user or tweet"), 404

    stmt = sqlalchemy.delete(likes_table).where(
        likes_table.c.user_id == u.id,
        likes_table.c.tweet_id == t.id
    )

    result = db.session.execute(stmt)
    db.session.commit()

    if result.rowcount == 0:
        return jsonify(False)

    return jsonify(True)
        #flask run debug
        #flask run debug