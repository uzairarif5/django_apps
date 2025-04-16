from .models import Sources
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, HttpResponseBadRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import environ
import requests

env = environ.Env()
environ.Env.read_env()
studyNotesSiteLink = "https://uzair-study-notes.vercel.app/"

def getOrderedLis(sourcesColor, sourcesOrder, sourcesObjs):
  output = ""
  for sourceNum in sourcesOrder:
    if (sourcesColor[str(sourceNum)]):
      output += "<li data-num=\"" + str(sourceNum) +"\"><span class=\"colorContainer\" style=\"background-color:" + sourcesColor[str(sourceNum)] + ";\"></span>"+sourcesObjs[sourceNum]+"</li>"
    else:
      output += "<li data-num=\"" + str(sourceNum) +"\">"+sourcesObjs[sourceNum]+"</li>"
  return output

def getUnorderedLis(sourcesColor, sourcesObjs):
  output = ""
  for sources in sourcesObjs:
    if (sourcesColor[str(sources.id)]):
      output += "<li data-num=\"" + str(sources.id) + "\"><span class=\"colorContainer\" style=\"background-color:" + sourcesColor[str(sources.id)] + ";\"></span>" + sources.content + "</li>"
    else:
      output += "<li data-num=\"" + str(sources.id) + "\">" + sources.content + "</li>"
  return output

@csrf_exempt
def getList(request: HttpRequest):
  try:
    input = json.loads(request.body)
    sourcesColor = input["sourcesColor"]
  except:
    raise SuspiciousOperation
  #either the study notes site or localhost can use this function.
  #For localhost, the password has to be set.
  if ((request.META.get("HTTP_REFERER") != studyNotesSiteLink) or (input["password"] != env("PASS_FOR_LOCAL"))):
    raise PermissionDenied
  try:
    sourcesObjs = Sources.objects.filter(id__in=tuple(sourcesColor.keys()))
  except:
    return HttpResponseServerError("Encountered a problem with querying the database.")
  try:
    output = "<ol id=\"sources\">"
    if ("sourcesOrder" in input):
      sourcesObjsReformatted = {d.id: d.content for d in sourcesObjs}
      output += getOrderedLis(sourcesColor, input["sourcesOrder"], sourcesObjsReformatted)
    else:
      output += getUnorderedLis(sourcesColor, sourcesObjs)
    output += "</ol>"
    return HttpResponse(output)
  except:
    return HttpResponseServerError("Successfully Extracted data from database, but the server wasn't able to process it.")

@csrf_exempt
def getAllList(request: HttpRequest):
  if (request.META.get("HTTP_REFERER") != studyNotesSiteLink):
    raise PermissionDenied
  try:
    sourcesObjs = Sources.objects.all()
  except:
    return HttpResponseServerError("Encountered a problem with querying the database.")
  try:
    topicWithSource = {}
    for source in list(sourcesObjs):
      for topic in source.topic:
        if(topic not in topicWithSource):
          topicWithSource[topic] = []
        topicWithSource[topic].append(source.content)
    return JsonResponse(topicWithSource)
  except:
    return HttpResponseServerError("Database queries successfully but there was a problem in the server.")

@csrf_exempt
def handleStudyNotesForm(request: HttpRequest):
  print(request.META.get("HTTP_REFERER"))
  if (request.META.get("HTTP_REFERER") != studyNotesSiteLink):
    raise PermissionDenied
  try:
    inputJSON = json.loads(request.body)
  except:
    raise SuspiciousOperation
  res = requests.post(env("STUDY_NOTES_GOOGLE_SHEET_API_LINK"), json=inputJSON)
  if(res.ok):
    return HttpResponse("Success") 
  else:
    return HttpResponseServerError("Encountered a problem with submitting the form.")

