from django.http import HttpRequest, HttpResponse
from .models import Sources
from django.http import Http404

def detail(request: HttpRequest):
  ids_tuple = tuple(int(id) for id in request.GET.get("ids").split(","))
  output = "<li>"
  try:
    sources_objs = Sources.objects.filter(id__in=ids_tuple)
    output = "<ul>"
    for sources_obj in sources_objs:
      output += "<li>" + sources_obj.content + "</li>"
    return HttpResponse(output + "</ul>")
  except Sources.DoesNotExist:
      raise Http404("Sources does not exist")