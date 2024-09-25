from http import HTTPStatus

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator

from etica_y_valores.enterprises.models import EnterpriseModel
from etica_y_valores.complaints.models import ComplaintModel
from ..models import UserModel
from ..utils.user_handlers import get_grouped_user_permissions


class UserLoginView(View):

    template_name = 'users/user_login.html'
    success_url = reverse_lazy('app_users:home_staff')

    def get(self, request, *args, **kwargs):
        """
        This method return our login view
        """

        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        """
        This method log in the user
        """

        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))

        if not user:
            return HttpResponse(content='Error, user not found', status=HTTPStatus.NOT_FOUND)

        login(request, user)

        return JsonResponse(data={'redirect_url': self.success_url}, status=HTTPStatus.OK)


@method_decorator(require_GET, name='dispatch')
class HomeKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'  # Nombre del contexto para la lista de quejas
    paginate_by = 10  # Si quieres paginación, puedes ajustarlo o quitarlo

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
            ).exclude(
                status_id__status__in=['Desestimados', 'Resolución']
            ).order_by('-created_at')

        else:

            user = self.request.user

            user_permissions = get_grouped_user_permissions(user)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class TableComplaintsStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns a table with complaints related to the authenticated user.
    """

    model = ComplaintModel
    template_name = 'users/table_complaints.html'
    context_object_name = 'complaints'
    paginate_by = 10
