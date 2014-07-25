from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client

from . import settings
from .models import Classifier


def name(template_name):
    return "".join(("recognition/", template_name))


class TestRecognition(TestCase):

    def _save_classifiers(self):
        for classifier in self.classifiers:
            classifier.save()

    def _delete_classifiers(self):
        for classifier in self.classifiers:
            classifier.delete()

    def setUp(self):
        self.client = Client()
        self.classifiers = []

        self.digits = Classifier(name="digits", classes=["0", "1"])
        self.shapes = Classifier(name="shapes", classes=["rect", "circle"])

        self.classifiers.append(self.digits)
        self.classifiers.append(self.shapes)
        self._save_classifiers()

    def tearDown(self):
        self._delete_classifiers()

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, name("main.html"))
        self.assertTemplateUsed(response, name("index.html"))
        self.assertListEqual(list(response.context["object_list"]), self.classifiers)

    def test_new_classifier_page(self):
        response = self.client.get(reverse("new_classifier"))
        self.assertTemplateUsed(response, name("main.html"))
        self.assertTemplateUsed(response, name("new_classifier.html"))

    def test_create_new_classifier(self):
        response = self.client.post(reverse("new_classifier"), {
            "name": "signs",
            "class_1": "plus",
            "class_2": "minus",
            "class_3": "mul",
            "class_4": "div",
        })

        self.assertRedirects(response, "/")

        signs = Classifier.objects.get(name="signs")
        self.classifiers.append(signs)
        self.assertListEqual(sorted(signs.classes), sorted([u"plus", u"minus", u"mul", u"div"]))

    def test_remove_classifier(self):
        response = self.client.post(reverse("remove", args=("digits",)))
        self.assertRedirects(response, "/")
        self.assertListEqual(list(Classifier.objects.all()), [self.shapes])

    def test_classifier_page(self):
        response = self.client.get(reverse("classifier", args=("digits",)))
        self.assertTemplateUsed(response, name("main.html"))
        self.assertTemplateUsed(response, name("classifier.html"))
        self.assertEqual(response.context["classifier"], self.digits)

    def test_train_page(self):
        response = self.client.get(reverse("add_example", args=("digits",)))
        self.assertTemplateUsed(response, name("main.html"))
        self.assertTemplateUsed(response, name("train.html"))

        self.assertEqual(response.context["classifier"], self.digits)
        self.assertEqual(response.context["X"], settings.UI_PICTURE_SIZE[0])
        self.assertEqual(response.context["Y"], settings.UI_PICTURE_SIZE[1])

    def test_classify_page(self):
        response = self.client.get(reverse("classify", args=("digits",)))
        self.assertTemplateUsed(response, name("main.html"))
        self.assertTemplateUsed(response, name("classify.html"))

        self.assertEqual(response.context["classifier"], self.digits)
        self.assertEqual(response.context["X"], settings.UI_PICTURE_SIZE[0])
        self.assertEqual(response.context["Y"], settings.UI_PICTURE_SIZE[1])


