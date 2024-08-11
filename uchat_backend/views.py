from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import google_auth_oauthlib.flow
import googleapiclient.discovery
import environ
import json

env = environ.Env()
environ.Env.read_env()

authorization_url = None
flow = None

def get_flow():
  global flow

  if flow:
    return flow
  flow = google_auth_oauthlib.flow.Flow.from_client_config(
      client_config={ 'web': {
        'client_id':env('client_id'),
        'project_id':env('project_id'),
        'auth_uri':env('auth_uri'),
        'token_uri':env('token_uri'),
        'auth_provider_x509_cert_url':env('auth_provider_x509_cert_url'),
        'client_secret':env('client_secret'),
        'redirect_uris':env('redirect_uris'),
      }},
      scopes=['https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube.readonly']
  )
  return flow

def authorize(request):
  global authorization_url
  
  if not authorization_url:
    flow = get_flow()
    flow.redirect_uri = env('redirect_uris')
    authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true'
    )
  
  return JsonResponse({
    "authorization_url": authorization_url,
  })

@csrf_exempt
def get_token(req):
  try:
    flow.fetch_token(code=req.body.decode("utf-8"))
    credentials = flow.credentials
    return JsonResponse({
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'expiry': credentials.expiry
    })  
  except:
    print("Something went wrong. This is the request:")
    print(req)
    print("This is the request body:")
    print(req.body)
    return HttpResponseServerError("Something went wrong.")  
  

@csrf_exempt
def send_message(request):
  data = json.loads(request.body.decode("utf-8"))

  credentials = flow.credentials
  youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
  request = youtube.liveChatMessages().insert(
    part = "snippet",
    access_token = data['token'],
    body={
      "snippet": {
        "liveChatId": data['liveChatId'],
        "type": "textMessageEvent",
        "textMessageDetails": {
          "messageText": data['message']
        }
      }
    }
  )
  request.execute()
  
  return JsonResponse({})
