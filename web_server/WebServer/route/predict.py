import uuid
import datetime
from django.http import HttpResponse
from PIL import Image
import urllib.request
import io

from WebServer.database.prediction import insert
from WebServer.database.model import get_latest_model_id
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

    request_id = uuid.uuid4()
    model_id, model_arch, model_path = get_latest_model_id()

    if model_id == 1:
        return HttpResponse(f"No Availabel Model!!!\n")
    ip_classifier.switch_model(model_arch)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    confidence, good, cost_time = ip_classifier.predict(image, model_path)

    insert(request_id, model_id, confidence, good, cost_time, timestamp, image_url)
    return HttpResponse(f"This image is {GOOD_DICT[good]}\n")
