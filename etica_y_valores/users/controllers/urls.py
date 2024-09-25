from django.urls import path

from django.contrib.auth.views import LogoutView
from ..views import user_views


app_name = 'app_users'


urlpatterns = [
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='app_users:login'), name='logout'),
    path('staff/', user_views.HomeKanbanStaffView.as_view(), name='home_staff'),
    path('staff/table/', user_views.TableComplaintsStaffView.as_view(),
         name='table_complaints_staff'),
]
