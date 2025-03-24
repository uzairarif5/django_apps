from django.http import HttpRequest, HttpResponse
from .models import Sources
from django.http import Http404
import json
from django.views.decorators.csrf import csrf_exempt

def getOrderedLis(sourcesColor, sourcesOrder, sourcesObjs):
  output = ""
  sourcesOrder = input["sourcesOrder"]
  for sourceNum in sourcesOrder:
    if (sourcesColor[str(sourceNum)]):
      output += "<li><span class=\"colorContainer\" style=\"background-color:" + sourcesColor[str(sourceNum)] + ";\"></span>"+sourcesObjs[sourceNum]+"</li>"
    else:
      output += "<li>"+sourcesObjs[sourceNum]+"</li>"
  return output

def getUnorderedLis(sourcesColor, sourcesObjs):
  output = ""
  for sources in sourcesObjs:
    if (sourcesColor[str(sources.id)]):
      output += "<li><span class=\"colorContainer\" style=\"background-color:" + sourcesColor[str(sources.id)] + ";\"></span>"+sources.content+"</li>"
    else:
      output += "<li>"+sources.content+"</li>"
  return output

@csrf_exempt
def getList(request: HttpRequest):
  try:
    input = json.loads(request.body)
    sourcesColor = input["sourcesColor"]
    sourcesObjs = Sources.objects.filter(id__in=tuple(sourcesColor.keys()))
    output = "<ol id=\"sources\">"
    if ("sourcesOrder" in input):
      sourcesObjsReformatted = {d.id: d.content for d in sourcesObjs}
      output += getOrderedLis(sourcesColor, input["sourcesOrder"], sourcesObjsReformatted)
    else:
      output += getUnorderedLis(sourcesColor, sourcesObjs)
    output += "</ol>"
    return HttpResponse(output)
  except:
    raise Http404("There was a problem.")