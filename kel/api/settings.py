import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = os.environ["SECRET_KEY"]

ROOT_URLCONF = "kel.api.urls"

WSGI_APPLICATION = "kel.api.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost/kel")
}

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware"
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",

    "pinax.api",

    "kel.api"
]

AUTH_USER_MODEL = "api.User"

KEL = {
    "IDENTITY_URL": os.environ["KEL_IDENTITY_URL"],
    "BLOBSTORE": {
        "BACKEND": "gcp",
        "BUCKET": "kel-test",
        "SERVICE_ACCOUNT": "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiYnJpYW5jYXJlLTEyNzgiLAogICJwcml2YXRlX2tleV9pZCI6ICJmMjUyMjliM2JiY2U5YTFhZDkwMjQxODhkYzE4OWNhZjc2YmM1ZmMyIiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUUNjYnkydi84ZzZQbHJLXG5mdVZ4NTh0bjJlRThEUmRoQ2lHR0NzTk5vMU5SaGFWeGVyNVBHQWY3OGcyc1B1WnFqVWlOaVhiV1NXY2ZSZWlDXG5YczFnR1VWK0d3YUFiK2lUT3BBd3ludHZUVlA2V3NBZG5TUVBPNzlzdnpIaTA3UmxrVFdKZWtSdmJBb01UNDVYXG5xbGtybGNLaUhDVzRtNi93NFQvTk1oSmJaMjNvUU1xdjI1NEJabFIzQXBoczF5Q3FSME1iUjRLNnc2eWpmdTNTXG5SMG1JSUliT3ZPL2s0bHU1aFdLK3NuNHB2SmpRekRLSzVBeDVVOGo2Ky9wZGRDc1ppTlVydHg2T2hpbUJrSGtTXG5qWDFKRzcvaUVkWlNCNDZhcGFva1M2Qzg0MzY5SzNHNXBwUWxQUUNmN1lRbXp4cWtPaXUrS09ERFFVNUtKV29zXG5qSmpTTnZDM0FnTUJBQUVDZ2dFQWQyTitpZUQ3amtBQ2lLTGFOOW1BNnF4bGNyQkhGSDluNEdZY2NnZGhVa2xlXG5YOElldGp5UDgxL2p3WDVyMmd3andDbVdjYXFwc2p0blhRQS9XOFZOdlJXaEc2ck01SGlBalV3cmNtR2c0dVFaXG4xVUFWd2k2R1JOZVNtaHVhaFIyU3IyNktCa045VTdIdjM4WVpzZUxsSFZYQUVDbDUyS3dBUm5tZGV2YnY4WjB6XG5KbDhQN2ptcnhwMnFNWitzclU0THhlelBCTEptQzlaendtM2pVaTlrYlJaWTBQQ3RwczZBK0VXMUVZMUJyOWt4XG56Unp3eVZaVTB0SzRFWDZMOWpJdlB4Ykk4ak5ZOUVpMzZnSmRmcTdEWlpkMUs1RGoxUVRWNUpMU0RERGZpdDJCXG5POCtraDhRR2dGa09LQjdDdUVOZ0U3QldmT1RkYTRLQXNUellrWWc3MFFLQmdRRHVneWtuaHpTUGtXN1FjdUhIXG5yTFA3cUpYT2M0QkNyWWUyUklFWnN3YXFEYm8wYmdsUXd5VHRZZENPK2p4TlJXM1dybU5oSWVuNFhjU1BVcjV4XG4zc25CaWdkUHFIZFNYOUxiQ1RVMFc2UWVaN2YrcG1LRDBycWR1S01yNm5rNnltT0hrZ2VZdHpCK0hXU2d3RFNhXG5mQ0pmWDBzQmlJM3BCM05mUDBuUEduc3ZEd0tCZ1FDbjUyenVBS2lEUTQwbmE1Uk55cmpCTFAyZnA0RkU5djN0XG4yZm9ELzlCNmpDVTBTaDgzWEY5bnZUbW5pS0Q5UStTSDJ6Z2c4OWpqK3hmREl1QUlxOXFrTUxpeXpLdCtnRE1wXG5pb3N0b3dWWmtJZHoxcldjN1oybjRCYjAxYTBEbG12ekEwclExQmxZVkJMTUZoSy85S0lzZ2FzeCtFdHVqYW04XG5GaUh2VWRNajJRS0JnUUNTSlVJcFcxcGtnaXVSaEdNK00xK1JXMnAzdHlRbk55ZEtFczI4VG90TjFkMTcxTlRXXG5iTXlLdS8zTUxoNlhCbXpZTjhEak9xR2ZzdTBIR1I5aXJLMlpicGN1UXo3aDlaOUE0WEo5WTQyN3A3Z0JURGhmXG5KOWQ3WHpCMGIxYmJKRG82VHN0aTB4VGVvZW9QNmRZUnR2QmsyZ0llcldxdkdBYWtuU1gveGUwbkZ3S0JnRlJIXG4vY3ptZGJBV080ZWJIOEdBemdiaHo1blJtamtGQm1mYmIvMkw3cGxsT2RPcWxVclR5bXduZHdaYXRmMExsRzZCXG5vd1lmZ1RMSE9xRlFJMGNYQk5SQVJLWXp5SzNpS2t4aTZBUUxmY2I4bnBHT0tISFNjTDN3NVhVV3dSYzQ3WXo1XG5qUmVRTC95L2p3UDAzSXFRZ010NGQzZkkzQXh0ZmRNVkJRbTllQS9aQW9HQWN4WGVJTjZrb0VseVdRSTFxdEpDXG5DUHpqdlNSWE0wRjF6bzlCdGVycmVUZE5pL25TVkJveUVvTkxTOCtPVlRaNWVRR2RPRlhLVWFxYVBOZG8wZWdDXG5yc0tJZHkwc090NFg5QkdBTmF3S1lYSkpUVVlFQ0oxQXl0Y0tqWHB3cjkvdUpOVDlUdktSQ0swbWVBSlBEeUY3XG5aejh2bE5jdHBqa0VrTnpYQ2pjUE8wQT1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJrZWwtOTEwQGJyaWFuY2FyZS0xMjc4LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjEwMjU5MTI5NDEzNDEwMDEyNTU5NyIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi90b2tlbiIsCiAgImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLAogICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L2tlbC05MTAlNDBicmlhbmNhcmUtMTI3OC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIKfQo="
    }
}
