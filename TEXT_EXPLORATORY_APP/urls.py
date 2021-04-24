from django.urls import path

from . import views 


urlpatterns = [

    path("",views.index,name="index"),
    path("persist_results",views.persist_results,name="persist_results")
]