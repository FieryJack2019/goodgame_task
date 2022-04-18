from bot.data.config import API_URL
import requests
import json


def get_category() -> list:
    return json.loads(requests.get(f'{API_URL}/api/v1/category/').text)


def get_games(categoryId: int) -> list:
    return json.loads(requests.get(f'{API_URL}/api/v1/games/{categoryId}/').text)


def get_game(gameId: int) -> dict:
    return json.loads(requests.get(f'{API_URL}/api/v1/game/{gameId}/').text)


def get_users(gameId: int, userId: int, listShownPlayer: list) -> list:
    returnData = []
    for user in json.loads(requests.get(f'{API_URL}/api/v1/users/{gameId}/').text):
        if user['id'] != userId and user['id'] not in listShownPlayer:
            returnData.append(user)
    return returnData


def get_user(userId: int) -> int:
    return json.loads(requests.get(f'{API_URL}/api/v1/user/{userId}/').text)


def is_active_user(userId: int) -> dict:
    return json.loads(requests.get(f'{API_URL}/api/v1/user/{userId}/').text)['isActive']


def add_new_user(data: dict) -> int:
    return json.loads(requests.post(f'{API_URL}/api/v1/user-add/', data=data).text)['id']


def update_user(userId: int, data: dict) -> None:
    return json.loads(requests.put(f'{API_URL}/api/v1/user/{userId}/', data=data).text)