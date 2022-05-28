import uuid
import datetime
from django.http import HttpResponse
from PIL import Image
import urllib.request
import io
from multiprocessing import Pool

from WebServer.database.prediction import insert
from WebServer.database.model import get_last_two_models
from ml_model import ip_classifier

GOOD_DICT = {0: "NG", 1: "OK"}


def predict(request):
    image_url = request.POST.get("image_url")
    try:
        with urllib.request.urlopen(image_url) as url:
            f = io.BytesIO(url.read())
        image = Image.open(f)
    except:
        return HttpResponse(f"Image Not Found!\n")


    model1_meta, model2_meta = get_last_two_models()

    model1_id, model1_arch, model1_path = model1_meta
    model2_id, model2_arch, model2_path = model2_meta

    if model1_id == -1 and model2_id == -1:
        return HttpResponse(f"No Availabel Model!!!\n")
    if model2_id == -1:
        ip_classifier.switch_model(model1_arch)
        request_id = uuid.uuid4()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
        confidence, good, cost_time = ip_classifier.predict(image, model1_path)

        # insert(request_id, model1_id, confidence, good, cost_time, timestamp, image_url)
        return HttpResponse(f"Only one model availabel."
                            f"This image is {GOOD_DICT[good]} wiht conf {confidence}\n")
    else:
        pool = Pool(processes=2)
        model1_result = pool.apply_async(model_infer, (model1_arch, model1_path, image))
        model2_result = pool.apply_async(model_infer, (model2_arch, model2_path, image))
        pool.close()
        pool.join()
        model1_result = model1_result.get()
        model2_result = model2_result.get()
        # return HttpResponse("123")
        return HttpResponse(f"Latest model result: "
                            f"This image is {GOOD_DICT[model1_result[3]]} with conf {model1_result[2]}\n"
                            f"Second to last model result: "
                            f"This image is {GOOD_DICT[model2_result[3]]} with conf {model2_result[2]}\n")


def model_infer(model_arch, model_path, image):
    request_id = uuid.uuid4()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    ip_classifier.switch_model(model_arch)
    confidence, good, cost_time = ip_classifier.predict(image, model_path)
    return [request_id, timestamp, confidence, good, cost_time]




