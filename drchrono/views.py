# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings

import utils
import oauth


def home(request):
    user_id = request.session.get("user")
    if user_id:
        user = utils.get_user(user_id)
        patients = utils.get_patients_with_today_birthday(
            utils.get_patients(user)
        )
        return render(request, 'wishes.html', {'patients': patients})
    return render(request, 'index.html',
                  {'STATIC_URL': settings.STATIC_URL,
                   'CLIENT_ID': settings.SOCIAL_AUTH_DRCHRONO_KEY})


def auth(request):
    code = request.GET.get("code")
    if code:
        token = oauth.get_token(code)
        user = utils.save_token(token)
        request.session["user"] = user.user_id
        return redirect("/")
    return render(request, 'error.html')

