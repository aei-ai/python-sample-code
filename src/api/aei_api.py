"""
aEi.ai Python API.
"""

import json
from requests import post, get, put, delete
from requests.models import Response
from typing import Text, Dict, List
from base64 import b64encode

AEI_AI_URL = "https://aei.ai"
API_VERSION = "v1"
API_URL = AEI_AI_URL + "/api/" + API_VERSION


class Status:
    """HTTP response status."""
    def __init__(self, code: int = None, error: Text = None, help: Text = None, **kwargs):
        """
        Constructs an HTTP response status.

        Args:
            code: HTTP response status code.
            error: Error message when response code is not 200.
            help: Instruction on how to fix the error.
            **kwargs: Arguments as key-value pairs.
        """
        self.code = code
        self.error = error
        self.help = help


def auth_headers(access_token: Text) -> Dict[Text, Text]:
    return {"Authorization": "Bearer " + access_token}


def params_2_string(params: Dict[Text, Text]) -> Text:
    if params is None or len(params.keys()) == 0:
        return ""

    out = "?"
    for k, v in params.items():
        out = out + k + "=" + v + "&"
    out = out[:-1]  # remove last &
    return out


def is_success(status: Dict[Text, Text]) -> bool:
    """
    Asserts if HTTP response is successful.

    Args:
        status: HTTP response to assert.

    Returns:
        True if response is successful, false otherwise.
    """
    if (status["code"] != 200):
        print(status["error"])
        print(status["help"])
        return False
    return True


def register(username: Text, email: Text, password: Text, agreed: bool) -> Response:
    """
    Registers a new client to the aEi.ai service with given client username, email, and password.

    Args:
        username: Client's username.
        email: Client's email.
        password: Client's password.
        agreed: True if client agreed to the statement of use and privacy policy.

    Returns:
        Response to registration request.
    """
    # prepare URL
    url = AEI_AI_URL + "/register"

    # prepare headers
    headers = {
        "username": username,
        "email": email,
        "password": password,
        "agreed": agreed
    }

    # make an API call to the aEi.ai service to register
    return post(url=url, headers=headers)


def login(username: Text, password: Text) -> Response:
    """
    Logs in to the aEi.ai service with given client username and password.

    Args:
        username: Client's username.
        password: Client's password.

    Returns:
        Response to the login request.
    """
    # prepare URL
    url = AEI_AI_URL + "/oauth/token"

    # prepare params
    params = {
        "grant_type": "client_credentials"
    }

    # prepare headers
    credentials = username + ':' + password
    credentials = credentials.encode("ascii")
    headers = {
        'Authorization': 'Basic ' + b64encode(credentials).decode("ascii"),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # make an API call to the aEi.ai service to get access token
    return post(url=url, data=params, headers=headers)


def create_new_user(access_token: Text, attributes: Dict[Text, Text] = None) -> Response:
    """
    Creates a new user with given username in aEi.ai service.

    Args:
        attributes: User custom attributes as string key-value pairs.
        access_token: Client's access token.

    Returns:
        Response to the new user creation request.
    """
    # prepare URL
    url = API_URL + "/users"

    # prepare headers
    headers = auth_headers(access_token)

    # prepare body
    body = json.dumps(attributes) if attributes else None

    # make an API call to the aEi.ai service to create a new user for user
    return post(url=url, data=body, headers=headers)


def create_new_interaction(user_ids: List[Text], access_token: Text) -> Response:
    """
    Creates a new aEi.ai interaction for given list of user IDs.

    Args:
        user_ids: List of user IDs in new interaction.
        access_token: Client's access token.

    Returns:
        Response to the new interaction request.
    """
    # prepare URL
    url = API_URL + "/interactions"

    # prepare headers
    headers = auth_headers(access_token)

    # prepare parameters
    params = [("user_id", user_id) for user_id in user_ids]

    # make an API call to the aEi.ai service to create a new interaction for given user IDs
    return post(url=url, data=params, headers=headers)


def get_interaction(interaction_id: Text, access_token: Text) -> Response:
    """
    Gets an interaction with given interaction ID.

    Args:
        interaction_id: Target interaction ID.
        access_token: Client's access token.

    Returns:
        Response to getting the interaction.
    """
    # prepare URL
    url = API_URL + "/interactions/" + interaction_id

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get an interaction with given ID
    return get(url=url, headers=headers)


def get_interaction_list(access_token: Text) -> Response:
    """
    Gets list of all interactions of the client.

    Args:
        access_token: Client's access token.

    Returns:
        Response to getting list of all the interactions of the client.
    """
    # prepare URL
    url = API_URL + "/interactions"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get an interaction with given ID
    return get(url=url, headers=headers)


def add_users_to_interaction(interaction_id: Text, user_ids: List[Text], access_token: Text) -> Response:
    """
    Adds given user to the given interaction in aEi.ai service.

    Args:
        interaction_id: Given interaction ID.
        user_ids: List of user IDs to add to the interaction.
        access_token: Client's access token.

    Returns:
        Response to adding users to interaction request.
    """
    # prepare URL
    url = API_URL + "/interactions/" + interaction_id + "/users"

    # prepare headers
    headers = auth_headers(access_token)

    # prepare parameters
    params = [("user_id", user_id) for user_id in user_ids]

    # make an API call to the aEi.ai service to add users to an interaction
    return put(url=url, data=params, headers=headers)


def new_text_input(user_id: Text, interaction_id: Text, text: Text, access_token: Text) -> Response:
    """
    Sends given user's text to given interaction.

    Args:
        user_id: Source user ID.
        interaction_id: Target interaction ID.
        text: User's utterance.
        access_token: Client's access token.

    Returns:
        Response to sending a new text input to an interaction.
    """
    # prepare URL
    url = API_URL + "/inputs/text"

    # prepare headers
    headers = auth_headers(access_token)

    # prepare parameters
    url = url + params_2_string(params={
        "user_id": user_id,
        "interaction_id": interaction_id
    })

    # make an API call to the aEi.ai service to send the new user utterance to the interaction
    return post(url=url, data=text, headers=headers)


def new_interaction_list_input(json_string: Text, access_token: Text) -> Response:
    """
    Analyzes a list of interactions passed as JSON.

    Args:
        json_string: Interaction list as JSON string.
        access_token: Client's access token.

    Returns:
        Response to analyzing given list of interactions.
    """
    # prepare URL
    url = API_URL + "/inputs/interaction-list"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to send the new user utterance to the interaction
    return post(url=url, data=json_string, headers=headers)


def get_user(user_id: Text, access_token: Text) -> Response:
    """
    Gets aEi.ai user with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the aEi.ai user.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user
    return get(url=url, headers=headers)


def get_user_emotion(user_id: Text, access_token: Text) -> Response:
    """
    Gets user's emotion with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the user's emotion.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id + "/emotion"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user's emotion
    return get(url=url, headers=headers)


def get_user_mood(user_id: Text, access_token: Text) -> Response:
    """
    Gets user's mood with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the user's mood.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id + "/mood"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user's mood
    return get(url=url, headers=headers)


def get_user_personality(user_id: Text, access_token: Text) -> Response:
    """
    Gets user's personality with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the user's personality.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id + "/personality"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user's personality
    return get(url=url, headers=headers)


def get_user_satisfaction(user_id: Text, access_token: Text) -> Response:
    """
    Gets user's satisfaction with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the user's satisfaction.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id + "/satisfaction"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user's satisfaction
    return get(url=url, headers=headers)


def get_user_social_perception(user_id: Text, access_token: Text) -> Response:
    """
    Gets user's social perception with given user ID.

    Args:
        user_id: Given user ID.
        access_token: Client's access token.

    Returns:
        Response to getting the user's social perception.
    """
    # prepare URL
    url = API_URL + "/users/" + user_id + "/social-perception"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get user's social perception
    return get(url=url, headers=headers)


def get_user_list(access_token: Text) -> Response:
    """
    Gets list of all aEi.ai users of the client.

    Args:
        access_token: Client's access token.

    Returns:
        Response to getting the aEi.ai users.
    """
    # prepare URL
    url = API_URL + "/users/"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get list of all client users
    return get(url=url, headers=headers)


def get_used_free_queries(access_token: Text) -> Response:
    """
    Gets number of  aEi.ai used free queries of the currently signed in client.

    Args:
        access_token: Client's access token.

    Returns:
        Response to getting number of used free queries to the aEi.ai API.
    """
    # prepare URL
    url = API_URL + "/metrics/queries/used"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get the number of free queries to the the aEi.ai API
    return get(url=url, headers=headers)


def get_used_paid_queries(access_token: Text) -> Response:
    """
    Gets number of aEi.ai used paid queries (in current month) of the currently signed in client.

    Args:
        access_token: Client's access token.
    Returns:
        Response to getting number of used paid queries to the aEi.ai API.
    """
    # prepare URL
    url = API_URL + "/metrics/queries"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get the number of paid queries to the the aEi.ai API
    return get(url=url, headers=headers)


def get_payment_sources(access_token: Text) -> Response:
    """
    Gets the payment method information from Stripe for a given customer.

    Args:
        access_token: Client's access token.
    Retruns:
        Response to getting payment methods.
    """
    # prepare URL
    url = API_URL + "/sources"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get payment methods information
    return get(url=url, headers=headers)


def get_payment_source(source_id: Text, access_token: Text) -> Response:
    """
    Gets the payment method information from Stripe for a given customer and source Id.

    Args:
        source_id: Target payment source ID.
        access_token: Client's access token.

    Returns:
        Response to getting a specific payment method information.
    """
    # prepare URL
    url = API_URL + "/sources/" + source_id

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get a payment method given its ID
    return get(url=url, headers=headers)


def add_payment_source(source_id: Text, access_token: Text) -> Response:
    """
    Adds a payment source ID (previously generated via Stripe API) to the client account.

    Args:
        access_token: Client's access token.
        source_id: Payment source ID.

    Returns:
        Response to adding a payment source ID to client account.
    """
    # prepare URL
    url = API_URL + "/sources/" + source_id

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to add a payment source to client's account
    return post(url=url, headers=headers)


def get_subscription(access_token: Text) -> Response:
    """
    Get the subscription information for given customer.

    Args:
        access_token: Client's access token.

    Returns:
        Response to getting subscription information.
    """
    # prepare URL
    url = API_URL + "/subscriptions"

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to get subscription information
    return get(url=url, headers=headers)


def update_subscription(subscription_type: Text, access_token: Text) -> Response:
    """
    Updates subscription to the given type.

    Args:
        access_token: Client's access token.
        subscription_type: Given new subscription type.

    Returns:
        Response to updating subscription.
    """
    # prepare URL
    url = API_URL + "/subscriptions"

    # prepare headers
    headers = auth_headers(access_token)

    # prepare parameters
    params = {"subscription_type": subscription_type}

    # make an API call to the aEi.ai service to update the subscription type
    return put(url=url, data=params, headers=headers)


def delete_source(source_id: Text, access_token: Text) -> Response:
    """
    Deletes a source from Stripe and aEi.ai account given the source ID.

    Args:
        source_id: Given source ID.
        access_token: Client's access token.

    Returns:
        Response to deleting the payment source with given ID.
    """
    # prepare URL
    url = API_URL + "/sources/" + source_id

    # prepare headers
    headers = auth_headers(access_token)

    # make an API call to the aEi.ai service to delete a payment method
    return delete(url=url, headers=headers)


def update_source(source_id: Text, update_params: Dict[Text, Text], access_token: Text) -> Response:
    """
    Updates a source in Stripe and aEi.ai account given the source ID and parameters to update.

    Args:
        source_id: Given source ID to update.
        update_params: Key-value params to update as request body.
        access_token: Client's access token.

    Returns:
        Response to updating the payment source.
    """
    # prepare URL
    url = API_URL + "/sources/" + source_id

    # prepare headers
    headers = auth_headers(access_token)

    # prepare body
    body = json.dumps(update_params) if update_params else None

    # make an API call to the aEi.ai service to update a payment source
    return put(url=url, data=body, headers=headers)


def change_password(password: Text, access_token: Text) -> Response:
    """
    Changes aEi.ai account password to the given new password, when use has a valid access token.

    Args:
        password: Given new password.
        access_token: Client's access token.

    Returns:
        Response to changing the password to the given new password.
    """
    # prepare URL
    url = API_URL + "/clients/password"

    # prepare headers
    headers = auth_headers(access_token)
    headers["password"] = password

    # make an API call to the aEi.ai service to change password
    return put(url=url, headers=headers)


def reset_password(email: Text) -> Response:
    """
    Resets aEi.ai account password by sending an email to the client.

    Args:
        email: Client's email.

    Returns:
        Response to sending a password reset email.
    """
    # prepare URL
    url = AEI_AI_URL + "/reset-password"

    # prepare params
    params = {"email": email}

    # make an API call to the aEi.ai service to send reset password email
    return post(url=url, data=params)


def update_password(username: Text, password_reset_token: Text, new_password: Text) -> Response:
    """
    Updates aEi.ai account password for the given username and password-reset token.

    Args:
        username: Client's username.
        password_reset_token: Password-reset token provided by server.
        new_password: Client's new password.

    Returns:
        Response to updating client's password.
    """
    # prepare URL
    url = AEI_AI_URL + "/update-password"

    # prepare headers
    headers = {
        "username": username,
        "token": password_reset_token,
        "password": new_password
    }

    # make an API call to the aEi.ai service to change password
    return put(url=url, headers=headers)
