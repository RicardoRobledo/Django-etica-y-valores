from django.urls import path

from django.contrib.auth.views import LogoutView
from ..views import user_views


app_name = 'app_users'


urlpatterns = [
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='app_users:login'), name='logout'),
    path('staff/users/',
         user_views.UserStaffView.as_view(), name='user_staff'),
    path('staff/users/list-users/',
         user_views.UserListView.as_view(), name='list_user_staff'),
    path('staff/users/supervisors/', user_views.get_supervisors,
         name='list_user_supervisor_staff'),
    path('staff/users/add-user/',
         user_views.AddUserView.as_view(), name='add_user_staff'),
    path('staff/users/user/', user_views.create_user, name='create_user_staff'),
    path('staff/users/update-user/<int:id>/',
         user_views.update_user, name='update_user_staff'),
    path('staff/users/user-password/<int:id>/',
         user_views.update_user_password, name='update_user_password_staff'),
    path('staff/users/user-status/<int:id>/',
         user_views.update_user_state, name='user_status_staff'),
    path('staff/users/user/<int:id>/', user_views.get_user_permissions,
         name='user_permissions_staff'),
    path('staff/users/user-info/<int:id>/', user_views.get_user,
         name='user_info_staff'),
    path('staff/complaints/',
         user_views.HomeKanbanStaffView.as_view(), name='home_staff'),
    path('staff/complaints/status/<str:status>/',
         user_views.StatusKanbanStaffView.as_view(), name='status_staff'),
    path('staff/complaints/city/<str:city>/',
         user_views.CityKanbanStaffView.as_view(), name='city_staff'),
    path('staff/complaints/priority/<str:priority>/',
         user_views.PriorityKanbanStaffView.as_view(), name='priority_staff'),
    path('staff/complaints/classification/<str:classification>/',
         user_views.ClassificationKanbanStaffView.as_view(), name='classification_staff'),
    path('staff/complaints/channel/<str:channel>/',
         user_views.ChannelKanbanStaffView.as_view(), name='channel_staff'),
    path('staff/complaints/table/', user_views.TableComplaintsStaffView.as_view(),
         name='table_complaints_staff'),
    path('staff/complaints_ended/table/', user_views.TableComplaintsEndedStaffView.as_view(),
         name='table_complaints_ended_staff'),
    path('staff/view-pdf/<int:file_id>/',
         user_views.view_pdf, name='staff_view_pdf'),
]
