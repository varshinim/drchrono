# -*- coding: utf-8 -*-
"""
    Oauth related functions
"""
import requests
import settings

TOKEN_URL = settings.DRCHRONO_BASE_URL + '/o/token/'


def _get_token(data):
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "charset": "UTF-8"}
    response = requests.post(TOKEN_URL, data=data,
                             headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}


def get_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.SOCIAL_AUTH_DRCHRONO_KEY,
        "client_secret": settings.SOCIAL_AUTH_DRCHRONO_SECRET,
        "code": code,
        "redirect_uri": settings.LOGIN_REDIRECT_URL 
    }
    return _get_token(data)


def referesh_token(user):
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.SOCIAL_AUTH_DRCHRONO_KEY,
        "client_secret": settings.SOCIAL_AUTH_DRCHRONO_SECRET,
        "redirect_uri": settings.LOGIN_REDIRECT_URL, 
        "refresh_token": user.refresh_token
    }
    return _get_token(data)

