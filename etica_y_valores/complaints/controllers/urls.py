from django.urls import path

from ..views import complaint_views, admin_views


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
    path('view-pdf/<int:file_id>/', admin_views.view_pdf, name='view_pdf'),

    # ------------------ Complaints paths -------------------

    path('complaint/', complaint_views.create_complaint,
         name='create_complaint'),
    path('complaint/comment/', complaint_views.create_comment,
         name='create_comment'),
    path('complaint/count/', complaint_views.complaints_count,
         name="complaint_count"),
    path('complaint/update_complaint/<str:code>/', complaint_views.update_complaint,
         name='update_complaint'),
    path('complaint/<str:code>/',
         complaint_views.ComplaintView.as_view(), name='get_complaint'),
    path('close_complaint/<str:code>/', complaint_views.close_complaint,
         name="close_complaint"),
    path('complaint/<str:code>/', complaint_views.delete_complaint,
         name='delete_complaint'),
    path('complaint/complaint_priority/<str:code>/', complaint_views.update_complaint_priority,
         name='update_complaint_priority'),
    path('complaint/comments/<str:code>/', complaint_views.CommentsView.as_view(),
         name='search_comments'),
    path('complaint/logs/<str:code>/', complaint_views.LogsView.as_view(),
         name='search_logs'),
]
