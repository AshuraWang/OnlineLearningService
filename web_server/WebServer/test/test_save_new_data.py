import json
from django.http import HttpResponse

from WebServer.route.train import save


def test_save_new_data(request):
    jsonfile = '../data_utils/new_labeled_data.json'
    with open(jsonfile, 'r') as f:
        jsondata = json.load(f)
    oknum, ngnum = save(jsondata)
    return HttpResponse(f"Saved {oknum} OK images, {ngnum} NG images!!!\n")