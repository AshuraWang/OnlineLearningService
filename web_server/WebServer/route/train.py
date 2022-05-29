import os.path
import uuid
import datetime
from django.http import HttpResponse
import urllib.request
import json

from WebServer.database.model import insert
from ml_model import ip_classifier

def train(request):
    params = ""
    # Parse and save new data.
    try:
        request_body = request.body.decode('UTF-8')
        json_par = request_body.split('&')
        new_data = json_par[0]
        if len(json_par) == 2:
            params = json_par[1]
        json_data = json.loads(new_data)
    except:
        return HttpResponse("Data Broken!!!\n")

    ok_num, ng_num = save(json_data)
    if ok_num < 1 or ng_num < 1:
        return HttpResponse("Not enough data!!!\n")

    # Parse params
    try:
        pars = json.loads(params)
        if 'epoch' in pars:
            epoch = pars['epoch']
            if isinstance(epoch, int):
                ip_classifier.epoch = pars['epoch']
        arc = pars['model_arc']
        if 'model_arc' in pars:
            # print(arc)
            if arc in ['mobilenet_v3', 'resnet18']:
                ip_classifier.switch_model(arc)
    except:
        print("No valid params")
        pass

    model_path = ip_classifier.train()
    architecture = ip_classifier.arc
    epoch = ip_classifier.epoch
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    insert(architecture, timestamp, epoch, model_path)
    ip_classifier.reset()
    return HttpResponse(f"Saved at {model_path}\n")


def save(json_data, save_path='../data_cache/dataset'):
    ok_path = os.path.join(save_path, 'OK')
    ng_path = os.path.join(save_path, 'NG')

    # Remove previous data
    if os.path.exists(ok_path):
        os.system(f"rm -rf {ok_path}")
    if os.path.exists(ng_path):
        os.system(f"rm -rf {ng_path}")
    os.makedirs(ok_path)
    os.makedirs(ng_path)

    data = json_data['data']
    ok_list, ng_list = data['ok'], data['ng']

    # Save data to local path
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


