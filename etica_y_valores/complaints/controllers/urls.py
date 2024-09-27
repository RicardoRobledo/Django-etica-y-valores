from django.urls import path

from ..views import complaint_views


app_name = 'app_complaints'


urlpatterns = [

    # ------------------ Complaints views -------------------

    path('', complaint_views.home_view, name='home'),
    path('search_complaint/<str:code>/', complaint_views.search_complaint,
         name='search_complaint'),
    path('complaint_created/<str:code>/', complaint_views.ComplaintCreatedView.as_view(),
         name='complaint_created'),
    path('status_complaint/<str:code>/', complaint_views.StatusComplaintView.as_view(),
         name='status_complaint'),

    # ------------------ Complaints paths -------------------

    path('complaint/', complaint_views.create_complaint,
         name='create_complaint'),
    path('complaint/count/', complaint_views.complaints_count,
         name="complaint_count"),
    path('close_complaint/<str:code>/', complaint_views.close_complaint,
         name="close_complaint"),
    path('complaint/<str:code>/', complaint_views.delete_complaint,
         name='delete_complaint'),
    path('complaint/complaint_priority/<str:code>/', complaint_views.update_complaint_priority,
         name='update_complaint_priority'),
    path('complaint/comments/<str:code>/', complaint_views.CommentsView.as_view(),
         name='search_comments'),
]
