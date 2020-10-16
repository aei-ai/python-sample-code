import sys
from api.aei_ai import *

# replace username with your username
USERNAME = "<YOUR USERNAME>"
# replace email with your email
EMAIL = "<YOUR ACCOUNT EMAIL>"
# replace password with your password
PASSWORD = "<YOU PASSWORD>"
# change registered to false if you have not registered an account in aEi.ai yet
REGISTERED = True


def main():

    # replace user1_id and user2_id with IDs of users you had created before
    # if you have not created users before, set user1_id and user2_id to None
    user1_id = None  # OR "<1ST USER ID>"
    user2_id = None  # OR "<2nd USER ID>"
    # replace interaction_id with ID of an interaction you had created before
    # if you have not created an interaction before, set interaction_id to None
    interaction_id = None  # OR "<INTERACTION ID>"

    # register a new user (if you don't have an account in aEi.ai yet)
    if not REGISTERED:
        response = register(username=USERNAME, email=EMAIL, password=PASSWORD, agreed=True)
        if not is_success(status=response.json()["status"]):
            sys.exit(1)

    # login (authentication)
    auth_response = login(username=USERNAME, password=PASSWORD)
    access_token = auth_response.json()["access_token"]
    print(f"Access token: {access_token}")

    # create two users
    if user1_id is None:
        user1_id = create_new_user(access_token=access_token).json()["user"]["userId"]
    print(f"User1 ID: {user1_id}")

    if user2_id is None:
        user2_id = create_new_user(access_token=access_token).json()["user"]["userId"]
    print(f"User2 ID: {user2_id}")

    # create an interaction and add users to it
    if interaction_id is None:
        interaction_id = create_new_interaction(user_ids=[user1_id, user2_id], access_token=access_token).json()["interaction"]["interactionId"]
    print(f"Interaction ID: {interaction_id}")

    # send an utterance by user1 to the interaction
    text = "I am happy"
    response = send_text(user_id=user1_id, interaction_id=interaction_id, text=text, access_token=access_token)
    if not is_success(status=response.json()["status"]):
        sys.exit(1)

    # send an image by user1 to the interaction
    image = "https://aei.ai/img/faces.jpg"
    response = send_image(user_id=user1_id, interaction_id=interaction_id, image=image, access_token=access_token)
    if not is_success(status=response.json()["status"]):
        sys.exit(1)

    # get all user models
    users = get_user_list(access_token=access_token).json()["users"]
    # NOTICE: user1 says she is happy, and user2 empathizes with her (e.g., check out emotion pleasure scores)
    for user in users:
        pad = user["affect"]["emotion"]["pad"]
        print("User[%s] Emotion PAD: (%1.2f, %1.2f, %1.2f)" % (user['userId'], pad['pleasure'], pad['arousal'], pad['dominance']))

    # check how many free queries you've made until now
    queries = get_used_free_queries(access_token=access_token).json()["queries"]
    print(f"Free queries: {queries}")


if __name__ == '__main__':
    main()