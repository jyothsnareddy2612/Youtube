from app.database.mongo import users_collection

def get_or_create_user(user_data: dict):
    existing_user = users_collection.find_one({"email": user_data["email"]})

    if existing_user:
        # ✅ Convert ObjectId → string
        existing_user["_id"] = str(existing_user["_id"])
        return existing_user

    result = users_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)  # ✅ important
    return user_data