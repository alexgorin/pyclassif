
from mongoengine import Document
from mongoengine import ListField
from mongoengine import StringField
from mongoengine import IntField

import numpy as np
import cPickle as pickle
from sklearn import svm


class User(Document):
    email = StringField(required=True, max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    def __unicode__(self):
        return self.email


class Classifier(Document):
    name = StringField(primary_key=True, max_length=50)
    last_training_set_length = IntField(default=0)

    #created_by = ReferenceField(User) #TODO: create this field

    classes = ListField(StringField(required=True, max_length=50))
    classifier = StringField()

    X = ListField(ListField())
    Y = ListField()

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        if self.classifier:
            self.clf = pickle.loads(str(self.classifier))
        else:
            self.clf = None

    def __unicode__(self):
        return self.name

    def classify(self, data):
        if not self.clf:
            self.train()

        self.clf.probability = True
        return self.clf.predict(data)

    def train(self):
        x = self.X
        y = self.Y

        if not len(x):
            #TODO: raise and process an exception
            return

        x, y = map(np.array, (x, y))
        clf = svm.SVC(probability=True)
        clf.fit(x, y)
        self.classifier = pickle.dumps(clf)
        self.last_training_set_length = len(self.X)
        self.save()


    def is_trained_recently(self):
        return self.additions_since_last_training() == 0

    def additions_since_last_training(self):
        return len(self.X) - self.last_training_set_length