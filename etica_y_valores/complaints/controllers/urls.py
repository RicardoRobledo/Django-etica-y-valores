from django.urls import path

from ..views import complaint_views


app_name = 'app_complaints'


urlpatterns = [
    path('', complaint_views.home_view, name='home'),
    path('complaint/', complaint_views.create_complaint,
         name='create_complaint'),
    path('search_complaint/<str:code>/', complaint_views.search_complaint,
         name='search_complaint'),
    path('complaint_created/<str:code>/', complaint_views.ComplaintCreatedView.as_view(),
         name='complaint_created'),
    path('status_complaint/<str:code>/', complaint_views.StatusComplaintView.as_view(),
         name='status_complaint'),
]
