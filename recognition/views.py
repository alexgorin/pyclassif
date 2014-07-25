from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

import cairosvg
from PIL import Image
import numpy as np
import scipy

from . import settings
from .core import fwindow
from .models import Classifier

import logging

logging.basicConfig(logging=logging.DEBUG,
                            format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
logging.getLogger("").setLevel(settings.DEBUG_LEVEL)

def raise_404_if_no_object(fn):
    """
    get_object_or_404 doesn't work with mongoengine,
    so this is needed for similar purpose
    """
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if not e.__class__.__name__ == "DoesNotExist":
                raise
            raise Http404
    return wrapper


class Classifiers(ListView):
    model = Classifier
    template_name = "recognition/index.html"

    def get_queryset(self):
        return Classifier.objects.all()

@raise_404_if_no_object
def show_classifier(request, name):
    return render(request, "recognition/classifier.html", {
            "classifier": Classifier.objects.get(pk=name) #get_object_or_404(Classifier, pk=name)
        })

"""
#Does not work with mongoengine
class ClassifierView(DetailView):
    model = Classifier
    template_name = "recognition/classifier.html"
"""


def new_classifier(request):
    if request.method == 'GET':
        return render(request, "recognition/new_classifier.html")

    if request.method == 'POST':
        classes = sorted([str(val) for key, val in request.POST.iteritems() if key.startswith("class_")])
        Classifier(name=request.POST["name"], classes=classes).save()
        return redirect("/")

@raise_404_if_no_object
def remove_classifier(request, name):
    if request.method == 'POST':
        Classifier.objects.get(pk=name).delete()
        return redirect("/")

@raise_404_if_no_object
def add_training_examples(request, name):
    if request.method == 'GET':
        return render(request, "recognition/train.html", {
            "classifier": Classifier.objects.get(pk=name), #get_object_or_404(Classifier, pk=name)
            "X": settings.UI_PICTURE_SIZE[0],
            "Y": settings.UI_PICTURE_SIZE[1],
        })

    if request.method == 'POST':
        classifier = Classifier.objects.get(pk=name) #get_object_or_404(Classifier, pk=name)
        classifier.X.append(process_image(create_image(request.POST["data"])))
        classifier.Y.append(request.POST["class_number"])
        classifier.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@raise_404_if_no_object
def train(request, name):
    if request.method == 'POST':
        classifier = Classifier.objects.get(pk=name) #get_object_or_404(Classifier, pk=name)
        classifier.train()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@raise_404_if_no_object
def classify(request, name):
    if request.method == 'GET':
        return render(request, "recognition/classify.html", {
            "classifier": Classifier.objects.get(pk=name), #get_object_or_404(Classifier, pk=name)
            "X": settings.UI_PICTURE_SIZE[0],
            "Y": settings.UI_PICTURE_SIZE[1],
        })

    if request.method == 'POST':
        classifier = Classifier.objects.get(pk=name) #get_object_or_404(Classifier, pk=name)
        image = create_image(request.POST["data"])
        response = HttpResponse(recognize_data(classifier, process_image(image)))

        """
        #For multiple objects recognition. Uncomment later.
        for frame in fwindow.squared_floating_window(image):
            prediction, probability = recognize_data_prob(classifier, process_image(frame))
            if probability > 0.6:
                logging.debug("Frame: ", frame)
                frame.save("./pictures2/%s_%d.bmp" % (str(prediction), int(probability*100)))
                logging.debug((prediction, probability))
        """
        return response


def _argmax(data):
    return max(range(len(data)), key=lambda i: data[i])


def recognize_data_prob(classifier, data):
    probabilities =  classifier.clf.predict_proba(data)[0]
    prediction = _argmax(probabilities)
    return classifier.classes[prediction], probabilities[prediction]


def recognize_data(classifier, data):
    data = np.array([1 if e > 0 else 0 for e in data])
    if settings.DEBUG_LEVEL == logging.DEBUG:
        scipy.misc.imsave('file.jpg', data.reshape(28, 28)) #for debug

    prediction = classifier.classify(data)
    return classifier.classes[prediction]


def create_image(svg):
    filename = "new.ps"
    with open(filename, "w") as f:
        cairosvg.svg2ps(bytestring=svg, write_to=f)

    image = Image.open(filename)
    image_full_size = max(image.size) * 3/2
    white_image = Image.new("RGB", (image_full_size, image_full_size), "white")
    top_left = ((image_full_size - image.size[0]) / 2, (image_full_size - image.size[1]) / 2)
    white_image.paste(image, box=top_left)
    return white_image


def process_image(image):
    image = image.resize(settings.COMPRESS_IMAGE_TO, resample=Image.ANTIALIAS)
    image = image.convert("L")

    pixmap = image.load()
    array_size = settings.COMPRESS_IMAGE_TO[0] * settings.COMPRESS_IMAGE_TO[1]
    image_data = np.array([0.]*array_size)
    limit = 0.1

    index = 0
    for i in range(image.size[1]):
        for j in range(image.size[0]):
            pixel_value = 1 - float(pixmap[j, i]) / 255
            if pixel_value < limit:
                pixel_value = 0

            image_data[index] = pixel_value
            index += 1

    if settings.DEBUG_LEVEL == logging.DEBUG:
        logging.debug(image_data.reshape(*settings.COMPRESS_IMAGE_TO))
        binary_image = np.array([1 if e > 0 else 0 for e in image_data])
        logging.debug(binary_image.reshape(*settings.COMPRESS_IMAGE_TO))

    return image_data.tolist()
