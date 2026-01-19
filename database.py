users = {}

def get_user(user_id):
    return users.get(user_id)

def save_user(user_id, data):
    users[user_id] = data