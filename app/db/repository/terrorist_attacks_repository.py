from app.db.database import terrorist_attacks_collection


def get_all_data():
    return terrorist_attacks_collection.find()


def get_casualties_data():
    return terrorist_attacks_collection.find({}, {'casualties': 1})








