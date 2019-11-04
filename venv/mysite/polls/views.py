from django.http import HttpResponse
from django.template import loader

from .models import Shop
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance


def index(request):
    template = loader.get_template('polls/indexMobile.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

