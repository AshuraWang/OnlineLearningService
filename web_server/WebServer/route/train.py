import os.path
import uuid
import datetime
from django.http import HttpResponse
from PIL import Image
import urllib.request
import io
import json

from WebServer.database.prediction import insert
from ml_model import ip_classifier

GOOD_DICT = {0: "NG", 1: "OK"}


def train(request):
    print(request.POST)
    print(request)
    new_data = request.POST.get("data")
    print(new_data)
    return HttpResponse("")


def save(json_data, save_path='../data_cache/dataset'):
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)
    ok_path = os.path.join(save_path, 'OK')
    ng_path = os.path.join(save_path, 'NG')
    if os.path.exists(ok_path):
        os.system(f"rm -rf {ok_path}")
    if os.path.exists(ng_path):
        os.system(f"rm -rf {ng_path}")
    os.makedirs(ok_path)
    os.makedirs(ng_path)

    data = json_data['data']
    ok_list, ng_list = data['ok'], data['ng']

    for url in ok_list:
        try:
            response = urllib.request.urlopen(url)
            image_name = url.split('/')[-1]
            image_path = os.path.join(ok_path, image_name)
            if (response.getcode() == 200):
                with open(image_path, "wb") as f:
                    f.write(response.read())
        except:
            print(f"{url} Data Broken!!!")
            continue

    for url in ng_list:
        try:
            response = urllib.request.urlopen(url)
            image_name = url.split('/')[-1]
            image_path = os.path.join(ng_path, image_name)
            if (response.getcode() == 200):
                with open(image_path, "wb") as f:
                    f.write(response.read())
        except:
            print(f"{url} Data Broken!!!")
            continue
    return len(ok_list), len(ng_list)


