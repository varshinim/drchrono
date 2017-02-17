# -*- coding: utf-8 -*-
"""
    Contains utility functions
"""
import requests
import datetime

from django.utils import timezone

from models import User
import oauth
import settings

def get_user(user_id):
    return User.objects.get(user_id=user_id)


def is_token_fresh(user):
    return user.expires >= timezone.now()


def save_token(token, user=None):
    if not user:
        user = User()
    user.access_token = token.get("access_token")
    user.refresh_token = token.get("refresh_token")
    try:
        user.expires = datetime.datetime.now() +\
                datetime.timedelta(seconds=token.get("expires_in"))
    except (TypeError, ValueError) as e:
        print "Error converting expries_in value"
    user.save()
    return user


def get_patients(user):
    if not is_token_fresh(user):
        response = oauth.referesh_token(user)
        user = save_token(response, user)

    headers = {
        'Authorization': "Bearer " + user.access_token
    }
    response = requests.get(settings.DRCHRONO_BASE_URL + '/api/patients',
                            headers=headers)
    patients = response.json().get("results")
    return patients


def get_patients_with_today_birthday(patients):
    filtered_patients = []
    today = datetime.datetime.today()
    for patient in patients:
        try:
            dob = datetime.datetime.strptime(patient.get('date_of_birth'),
                                             '%Y-%m-%d')
            if dob.day == today.day and dob.month == today.month:
                filtered_patients.append(patient)
        except TypeError:
            print "Date of Birth unknown or wrong format"
    return filtered_patients
