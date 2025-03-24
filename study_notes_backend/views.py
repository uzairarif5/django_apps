from django.http import HttpRequest
from .models import Sources
from django.http import Http404
from django.shortcuts import render

def detail(request: HttpRequest):
  try:
    ids_tuple = tuple(int(id) for id in request.GET.get("ids").split(","))
    sources_objs = Sources.objects.filter(id__in=ids_tuple)
    return render(request, "study_notes_backend/list.html", {"sources_objs":sources_objs})
  except:
      raise Http404("There was a problem.")