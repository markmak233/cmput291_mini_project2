[
    {
        '$match': {
            'genres': {
                '$regex': 'myst', 
                '$options': 'i'
            }
        }
    }, {
        '$lookup': {
            'from': 'title_ratings', 
            'localField': 'tconst', 
            'foreignField': 'tconst', 
            'as': 'rating'
        }
    }, {
        '$unwind': {
            'path': '$rating'
        }
    }, {
        '$project': {
            '_id': '$_id', 
            'primaryTitle': '$primaryTitle', 
            'originalTitle': '$originalTitle', 
            'startYear': '$startYear', 
            'runtimeMinutes': '$runtimeMinutes', 
            'genres': '$genres', 
            'averagRating': {
                '$toDecimal': '$rating.averageRating'
            }, 
            'numVotes': {
                '$toInt': '$rating.numVotes'
            }
        }
    }, {
        '$unwind': {
            'path': '$numVotes'
        }
    }, {
        '$match': {
            'numVotes': {
                '$gte': 200000
            }
        }
    }, {
        '$sort': {
            'averagRating': -1
        }
    }
]