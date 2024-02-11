from functools import wraps

from flask import jsonify, request

from app.config import Config


# https://circleci.com/blog/authentication-decorators-flask/

def is_valid(api_key):
  available_api_keys = [Config.API_KEY]
  if api_key in available_api_keys:
    return True



def api_key_required(func):

  @wraps(func)
  def decorator(*args, **kwargs):
    if headers := request.headers:
      api_key: str = headers.get("x-access-token")
    else:
      return jsonify(error="Please provide an API key"), 401

    # Check if API key is correct and valid
    if is_valid(api_key):
      return func(*args, **kwargs)

    return jsonify(error="The provided API key is not valid"), 403

  return decorator