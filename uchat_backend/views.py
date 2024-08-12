from django.http import JsonResponse, HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import google_auth_oauthlib.flow
import googleapiclient.discovery
import environ
import json

env = environ.Env()
environ.Env.read_env()
statesStorage = []

def get_flow(state = None):
  flow = google_auth_oauthlib.flow.Flow.from_client_config(
    client_config={ 'web': {
      'client_id':env('client_id'),
      'project_id':env('project_id'),
      'auth_uri':env('auth_uri'),
      'token_uri':env('token_uri'),
      'auth_provider_x509_cert_url':env('auth_provider_x509_cert_url'),
      'client_secret':env('client_secret'),
      'redirect_uris':env('redirect_uri'),
    }},
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/youtube.readonly'],
    state=state
  )
  flow.redirect_uri = env('redirect_uri')
  return flow

def authorize(request):
  global statesStorage

  flow = get_flow()
  authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='select_account'
  )

  statesStorage.append(state)
  
  return JsonResponse({
    "authorization_url": authorization_url,
  })

@csrf_exempt
def get_token(req):
  global statesStorage

  data = json.loads(req.body.decode("utf-8"))
  try:
    statesStorage.remove(data["state"])
    flow = get_flow(data["state"])
    flow.fetch_token(code=data["code"])
    credentials = flow.credentials
    return JsonResponse({
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'expiry': credentials.expiry
    })  
  except Exception as e:
    print(e)
    return HttpResponseServerError("Something went wrong.")  
  
