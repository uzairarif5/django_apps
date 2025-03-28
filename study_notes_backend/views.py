from .models import Sources, topicsList
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import environ

env = environ.Env()
environ.Env.read_env()

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
      output += "<li><span class=\"colorContainer\" style=\"background-color:" + sourcesColor[str(sources.id)] + ";\"></span>" + sources.content + "</li>"
    else:
      output += "<li data-num=\"" + str(sources.id) + "\">" + sources.content + "</li>"
  return output

@csrf_exempt
def getList(request: HttpRequest):
  try:
    input = json.loads(request.body)
    sourcesColor = input["sourcesColor"]
  except:
    raise HttpResponseBadRequest("There is a problem with the request.")
  if ((request.META.get("HTTP_REFERER")=="http://localhost:3000/") and (input["password"] != env("PASS_FOR_LOCAL"))):
    raise HttpResponseForbidden("Not allowed.")
  try:
    sourcesObjs = Sources.objects.filter(id__in=tuple(sourcesColor.keys()))
  except:
    raise HttpResponseServerError("Encountered a problem with querying the database.")
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
    raise HttpResponseServerError("Successfully Extracted data from database, but the server wasn't able to process it.")
  

@csrf_exempt
def getAllList(request: HttpRequest):
  try:
    sourcesObjs = Sources.objects.all()
  except:
    raise HttpResponseServerError("Encountered a problem with querying the database.")
  try:
    topicWithSource = {}
    for source in list(sourcesObjs):
      for topic in source.topic:
        if(topic not in topicWithSource):
          topicWithSource[topic] = []
        topicWithSource[topic].append(source.content)
    return JsonResponse(topicWithSource)
  except:
    raise HttpResponseServerError("Database queries successfully but there was a problem in the server.")

