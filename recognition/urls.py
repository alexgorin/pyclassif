from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    #Index page - list of classifiers
    url(r'^$', views.Classifiers.as_view(), name='index'),

    #Show a particular classifier
    #url(r'^classifier/(?P<name>[\w]+)$', views.ClassifierView.as_view(), name='classifier'),
    url(r'^classifier/(?P<name>[\w]+)$', views.show_classifier, name='classifier'),

    #Create a new classifier
    url(r'^new_classifier$', views.new_classifier, name='new_classifier'),

    #Remove classifier
    url(r'^remove_classifier/(?P<name>[\w]+)$', views.remove_classifier, name='remove'),

    #Add training example
    url(r'^add_example/(?P<name>[\w]+)$', views.add_training_examples, name='add_example'),

    #Train classifier
    url(r'^train/(?P<name>[\w]+)$', views.train, name='train'),

    #Classify data with particular classifier
    url(r'^classify/(?P<name>[\w]+)$', views.classify, name='classify'),
)