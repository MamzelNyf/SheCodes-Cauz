from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('events/',views.EventList.as_view()),
    path('events/<slug:slug>', views.EventDetail.as_view(), name='event_detail'),
    path('pledges/',views.PledgeList.as_view()),
    path('pledges/<int:pk>', views.PledgeDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<slug:slug>', views.CategoryDetail.as_view(),name='categories_detail'),
    path('regions/', views.RegionList.as_view()),
    path('regions/<slug:slug>', views.RegionDetail.as_view(),name='region_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)