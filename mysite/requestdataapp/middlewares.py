import datetime

from django.http import HttpRequest
from django.shortcuts import render


class ThrottlingRequestMiddellware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.user_time = {}
        self.time_delay = 1

    def __call__(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR', '')
        if ip in  self.user_time:
            delta_time = datetime.datetime.now() - self.user_time[ip]

            if delta_time < datetime.timedelta(0, self.time_delay):
                return render(request, 'requestdataapp/error-page.html')

        else:
            self.user_time[ip] = datetime.datetime.now()
            print(self.user_time)
        response = self.get_response(request)

        return response
