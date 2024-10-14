import json
from http import HTTPStatus

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.http.multipartparser import MultiPartParser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.http import require_GET, require_http_methods
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from etica_y_valores.enterprises.models import EnterpriseModel
from etica_y_valores.complaints.models import (
    ComplaintModel,
    StatusCategoryModel,
    CityCategoryModel,
    PriorityCategoryModel,
    ClassificationCategoryModel,
    ChannelCategoryModel,
    FileModel
)
from ..models import UserModel, UserLevelCategory
from ..utils.user_handlers import get_grouped_user_permissions


class UserStaffView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        """
        This method return users in the enterprise.
        """

        user = request.user
        user_level = user.user_level_id.user_level

        users = UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host()).values('id', 'username')

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            return JsonResponse(data={'users': list(users)})

        else:

            user_permissions = get_grouped_user_permissions(user, user_level)

            if not 'Usuarios' in user_permissions['tasks']:
                return JsonResponse(data={'msg': 'Without enough permissions to get users'}, status=HTTPStatus.FORBIDDEN)

            return JsonResponse(data={'users': list(users)})


@require_http_methods(["GET"])
@login_required
def get_user_permissions(request, id):

    user = request.user
    user_level = user.user_level_id.user_level

    if not UserModel.objects.filter(id=id).exists():
        return JsonResponse(data={"msg": "User not found"}, status=HTTPStatus.NOT_FOUND)

    if user_level == 'Superusuario' or user_level == 'Supervisor':
        return JsonResponse(data={'permissions': 'all'}, status=HTTPStatus.FOUND)

    else:
        return JsonResponse(data={'permissions': get_grouped_user_permissions(user, user_level)}, status=HTTPStatus.FOUND)


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
    paginate_by = 10 # Si quieres paginación, puedes ajustarlo o quitarlo

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
            user_permissions = get_grouped_user_permissions(user, user_level)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
            ).exclude(
                status_id__status__in=['Desestimados', 'Resolución']
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class StatusKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level
        status = self.kwargs.get('status', None)

        status_gotten = StatusCategoryModel.objects.filter(status=status)

        if not status_gotten.exists():
            return JsonResponse(data={"msg": "Nonexistent status"}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                status_id__status=status,
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            if not status in user_permissions['statuses']:
                return JsonResponse(data={"msg": "Status not allowed"}, status=HTTPStatus.FORBIDDEN)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
                status_id__status=status
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class CityKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user in base of a city.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level
        city = self.kwargs.get('city', None)

        city_gotten = CityCategoryModel.objects.filter(city=city)

        if not city_gotten.exists():
            return JsonResponse(data={"msg": "Nonexistent city"}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                city_id__city=city,
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            if not city in user_permissions['cities']:
                return JsonResponse(data={"msg": "City not allowed"}, status=HTTPStatus.FORBIDDEN)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city=city,
                priority_id__priority__in=user_permissions['priorities'],
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class PriorityKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user in base of a city.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level
        priority = self.kwargs.get('priority', None)

        priority_gotten = PriorityCategoryModel.objects.filter(
            priority=priority)

        if not priority_gotten.exists():
            return JsonResponse(data={"msg": "Nonexistent priority"}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                priority_id__priority=priority,
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            if not priority in user_permissions['priorities']:
                return JsonResponse(data={"msg": "Priority not allowed"}, status=HTTPStatus.FORBIDDEN)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                priority_id__priority=priority,
                city_id__city__in=user_permissions['cities'],
            ).exclude(
                status_id__status__in=['Desestimados', 'Resolución']
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class ClassificationKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user in base of a classification.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level
        classification = self.kwargs.get('classification', None)

        classification_gotten = ClassificationCategoryModel.objects.filter(
            classification=classification)

        if not classification_gotten.exists():
            return JsonResponse(data={"msg": "Nonexistent classification"}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                classification_id__classification=classification,
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                classification_id__classification=classification,
                priority_id__priority__in=user_permissions['priorities'],
                city_id__city__in=user_permissions['cities'],
                status_id__status__in=user_permissions['statuses'],
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class ChannelKanbanStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns our home kanban staff view.
    It lists complaints related to the authenticated user in base of a channel.
    """

    model = ComplaintModel
    template_name = 'users/home_kanban_staff.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level
        channel = self.kwargs.get('channel', None)

        channel_gotten = ChannelCategoryModel.objects.filter(
            channel=channel)

        if not channel_gotten.exists():
            return JsonResponse(data={"msg": "Nonexistent channel"}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                channel_id__channel=channel,
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                channel_id__channel=channel,
                priority_id__priority__in=user_permissions['priorities'],
                city_id__city__in=user_permissions['cities'],
                status_id__status__in=user_permissions['statuses'],
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
    paginate_by = 12

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
            ).order_by('-created_at')

        return response


@method_decorator(require_GET, name='dispatch')
class TableComplaintsEndedStaffView(LoginRequiredMixin, ListView):
    """
    This class-based view returns a table with complaints ended and related to the authenticated user.
    """

    model = ComplaintModel
    template_name = 'users/table_complaints.html'
    context_object_name = 'complaints'
    paginate_by = 12

    def get_queryset(self):
        """
        Override this method to return complaints ordered by creation date.
        """

        user_level = self.request.user.user_level_id.user_level

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                status_id__status='Resolución'
            ).order_by('-created_at')

        else:

            user = self.request.user
            user_permissions = get_grouped_user_permissions(user, user_level)

            response = ComplaintModel.objects.filter(
                enterprise_id__subdomain=self.request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
                status_id__status='Resolución'
            ).order_by('-created_at')

        return response


class UserListView(LoginRequiredMixin, ListView):

    model = UserModel
    template_name = 'users/list_users.html'
    context_object_name = 'objects'
    paginate_by = 15

    def get_queryset(self):
        """
        Override this method to return users ordered by creation date.
        """

        user = self.request.user
        user_level = user.user_level_id.user_level

        queryset = super().get_queryset().filter(
            enterprise_id__subdomain=self.request.get_host())
        query = self.request.GET.get('q', '')

        print(user_level)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            if query:
                response = queryset.filter(
                    Q(id__icontains=query) |
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(middle_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(email__icontains=query)
                ).order_by('-created_at')

            else:
                response = queryset.order_by('-created_at')

        else:

            user_permissions = get_grouped_user_permissions(user, user_level)

            if not 'Usuarios' in user_permissions['tasks']:
                return JsonResponse(data={"msg": "Without enough permissions to get users"}, status=HTTPStatus.FORBIDDEN)

            if query:
                response = queryset.filter(
                    Q(id__icontains=query) |
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(middle_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(email__icontains=query)
                ).exclude(
                    user_level_id__user_level__in=[
                        'Superusuario', 'Supervisor']
                ).order_by('-created_at')

            else:
                response = queryset.exclude(
                    user_level_id__user_level__in=[
                        'Superusuario', 'Supervisor']
                ).order_by('-created_at')

        return response


class AddUserView(LoginRequiredMixin, View):

    model = UserModel
    template_name = 'users/add_user.html'
    context_object_name = 'objects'

    def get(self, request, *args, **kwargs):
        """
        This method return users in the enterprise.
        """

        return render(request, self.template_name)


class InteractiveKanbanComplaintView(LoginRequiredMixin, View):

    template_name = 'users/interactive_kanban.html'

    def get(self, request, *args, **kwargs):
        """
        This method return our interactive kanban view
        """

        return render(request, self.template_name)


@require_http_methods(["PUT"])
@login_required
def update_user_state(request, id):
    """
    This function update the 'is_active' attribute 
    """

    status = json.loads(request.body).get('status', '')

    if not isinstance(status, bool):
        return JsonResponse(data={"msg": "Invalid status"}, status=HTTPStatus.BAD_REQUEST)

    user = request.user
    user_level = user.user_level_id.user_level

    if user_level == 'Superusuario' or user_level == 'Supervisor':

        UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            id=id
        ).update(is_active=status)

        return JsonResponse(data={'msg': 'User state updated'}, status=HTTPStatus.OK)

    else:

        user_permissions = get_grouped_user_permissions(user, user_level)

        if not 'Usuarios' in user_permissions['tasks']:
            return JsonResponse(data={"msg": "Without enough permissions to update user state"}, status=HTTPStatus.FORBIDDEN)

        UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            id=id
        ).update(is_active=status)

        return JsonResponse(data={'msg': 'User state updated'}, status=HTTPStatus.OK)


@require_http_methods(["GET"])
@login_required
def get_supervisors(request):
    """
    This function returns the supervisors of the enterprise
    """

    user = request.user
    user_level = user.user_level_id.user_level

    user_permissions = get_grouped_user_permissions(user, user_level)

    if user_level in ['Superusuario', 'Supervisor']:
        supervisors = UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            user_level_id__user_level='Supervisor'
        )

        return JsonResponse(data={
            "supervisors": list(supervisors.values('id', 'first_name', 'middle_name', 'last_name'))}, status=HTTPStatus.OK)

    if not 'Usuarios' in user_permissions['tasks']:
        return JsonResponse(data={"msg": "Without enough permissions to get supervisors"}, status=HTTPStatus.FORBIDDEN)

    else:
        supervisors = UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            user_level_id__user_level='Supervisor'
        )

        return JsonResponse(data={
            "supervisors": list(supervisors.values('id', 'first_name', 'middle_name', 'last_name'))}, status=HTTPStatus.OK)


@require_http_methods(["POST"])
@login_required
def create_user(request):
    """
    This function creates a new user
    """

    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    first_name = request.POST.get('name')
    middle_name = request.POST.get('middle-name')
    last_name = request.POST.get('last-name')
    user_level_add = request.POST.get('user-level')
    supervisor_id = request.POST.get('supervisor')
    permissions = request.POST.getlist('permissions')

    if not all([username, password, first_name, middle_name, last_name, email, user_level_add]):
        return JsonResponse(data={"msg": "Empty fields"}, status=HTTPStatus.BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"msg": "Invalid email"}, status=HTTPStatus.BAD_REQUEST)

    if not supervisor_id and user_level_add == 'Operador':
        return JsonResponse(data={"msg": "Supervisor was not found"}, status=HTTPStatus.NOT_FOUND)

    user_level_gotten = UserLevelCategory.objects.filter(
        user_level=user_level_add)

    if not user_level_gotten.exists():
        return JsonResponse(data={"msg": "Nonexistent user level"}, status=HTTPStatus.BAD_REQUEST)

    if permissions:
        permissions_gotten = Group.objects.filter(name__in=permissions)

        if not len(permissions) == permissions_gotten.count():
            return JsonResponse(data={"msg": "Nonexistent permissions"}, status=HTTPStatus.BAD_REQUEST)

    if UserModel.objects.filter(username=username, enterprise_id__subdomain=request.get_host(),).exists():
        return JsonResponse(data={"msg": "Username already exists"}, status=HTTPStatus.BAD_REQUEST)

    if UserModel.objects.filter(email=email, enterprise_id__subdomain=request.get_host(),).exists():
        return JsonResponse(data={"msg": "Email already exists"}, status=HTTPStatus.BAD_REQUEST)

    user = request.user
    user_level = user.user_level_id.user_level

    if user_level == 'Operador':

        user_permissions = get_grouped_user_permissions(user, user_level)

        if not 'Usuarios' in user_permissions['tasks']:
            return JsonResponse(data={"msg": "Without enough permissions to get supervisors"}, status=HTTPStatus.FORBIDDEN)

    if user_level_add == 'Operador':

        try:
            supervisor_id = int(supervisor_id)
        except (ValueError, TypeError):
            return JsonResponse({"msg": "Supervisor value not is valid"}, status=400)

        supervisor = UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            id=supervisor_id,
            user_level_id__user_level='Supervisor'
        )

        if not supervisor.exists():
            return JsonResponse(data={"msg": "Supervisor not found"}, status=HTTPStatus.NOT_FOUND)

        user_obj = UserModel.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            supervisor=supervisor.first(),
            user_level_id=user_level_gotten.first(),
            enterprise_id=EnterpriseModel.objects.get(
                subdomain=request.get_host())
        )

    else:

        user_obj = UserModel.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            user_level_id=user_level_gotten.first(),
            enterprise_id=EnterpriseModel.objects.get(
                subdomain=request.get_host())
        )

    # No correo igual

    if permissions:
        user_obj.groups.add(*permissions_gotten)

    return JsonResponse(data={'msg': 'User created'}, status=HTTPStatus.OK)


@require_http_methods(["GET"])
@login_required
def get_user(request, id):
    """
    This function returns the user data
    """

    user = request.user
    user_level = request.user.user_level_id.user_level

    if user_level == 'Operador':

        user_permissions = get_grouped_user_permissions(user, user_level)

        if 'Usuarios' not in user_permissions['tasks']:
            return JsonResponse(data={"msg": "Without enough permissions to get user"}, status=HTTPStatus.FORBIDDEN)

    user_obj = UserModel.objects.filter(
        enterprise_id__subdomain=request.get_host(),
        id=id
    )

    if not user_obj.exists():
        return JsonResponse(data={"msg": "User not found"}, status=HTTPStatus.NOT_FOUND)

    user_obj = user_obj.first()

    permissions = [
        permission.name for permission in user_obj.groups.all()]

    return JsonResponse(data={'user': {
        'id': user_obj.id,
        'username': user_obj.username,
        'first_name': user_obj.first_name,
        'middle_name': user_obj.middle_name,
        'last_name': user_obj.last_name,
        'email': user_obj.email,
        'user_level': user_obj.user_level_id.user_level,
        'supervisor': user_obj.supervisor.id if user_obj.supervisor else '',
        'permissions': permissions
    }}, status=HTTPStatus.OK)


@require_http_methods(["PUT"])
@login_required
def update_user_password(request, id):
    """
    This function update the user password
    """

    user = request.user
    user_level = request.user.user_level_id.user_level

    password = json.loads(request.body)['password']

    if user_level == 'Operador':

        user_permissions = get_grouped_user_permissions(user, user_level)

        if 'Usuarios' not in user_permissions['tasks']:
            return JsonResponse(data={"msg": "Without enough permissions to get user"}, status=HTTPStatus.FORBIDDEN)

    try:
        validate_password(password=password)
    except ValidationError as e:
        return JsonResponse({'valid': False, 'message': e.messages}, status=HTTPStatus.BAD_REQUEST)

    user_gotten = UserModel.objects.filter(
        enterprise_id__subdomain=request.get_host(),
        id=id)

    if not user_gotten.exists():
        return JsonResponse(data={"msg": "User not found"}, status=HTTPStatus.NOT_FOUND)

    user_gotten = user_gotten.first()
    user_gotten.set_password(password)
    user_gotten.save()

    return JsonResponse(data={'msg': 'User password updated'}, status=HTTPStatus.OK)


@require_http_methods(["PUT"])
@login_required
def update_user(request, id):
    """
    This function update an user
    """

    user = request.user
    user_level = request.user.user_level_id.user_level

    parser = MultiPartParser(request.META, request,
                             request.upload_handlers, request.encoding)
    data, files = parser.parse()

    username = data.get('username')
    first_name = data.get('name')
    middle_name = data.get('middle-name')
    last_name = data.get('last-name')
    email = data.get('email')
    user_level = data.get('user-level')
    supervisor_id = data.get('supervisor')
    permissions = data.getlist('permissions')

    if not all([username, first_name, middle_name, last_name, email, user_level]):
        return JsonResponse(data={"msg": "Empty fields"}, status=HTTPStatus.BAD_REQUEST)

    if user_level == 'Operador':

        user_permissions = get_grouped_user_permissions(user, user_level)

        if 'Usuarios' not in user_permissions['tasks']:
            return JsonResponse(data={"msg": "Without enough permissions to update user"}, status=HTTPStatus.FORBIDDEN)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"msg": "Invalid email"}, status=HTTPStatus.BAD_REQUEST)

    if not supervisor_id and user_level == 'Operador':
        return JsonResponse(data={"msg": "Supervisor was not found"}, status=HTTPStatus.NOT_FOUND)

    user_level_gotten = UserLevelCategory.objects.filter(
        user_level=user_level)

    if not user_level_gotten.exists():
        return JsonResponse(data={"msg": "Nonexistent user level"}, status=HTTPStatus.BAD_REQUEST)

    if permissions:

        permissions_gotten = Group.objects.filter(name__in=permissions)

        if not len(permissions) == permissions_gotten.count():
            return JsonResponse(data={"msg": "Nonexistent permissions"}, status=HTTPStatus.BAD_REQUEST)

        user_permissions_given = Group.objects.filter(name__in=permissions)
        user_permissions_not_given = Group.objects.exclude(
            name__in=permissions)

    user_excluded = UserModel.objects.exclude(id=id)

    if user_excluded.filter(username=username, enterprise_id__subdomain=request.get_host(),).exists():
        return JsonResponse(data={"msg": "Username already exists"}, status=HTTPStatus.BAD_REQUEST)

    if user_excluded.filter(email=email, enterprise_id__subdomain=request.get_host()).exists():
        return JsonResponse(data={"msg": "Email already exists"}, status=HTTPStatus.BAD_REQUEST)

    user_gotten = UserModel.objects.filter(
        enterprise_id__subdomain=request.get_host(),
        id=id)

    if not user_gotten.exists():
        return JsonResponse(data={"msg": "User not found"}, status=HTTPStatus.NOT_FOUND)

    if user_level == 'Operador':

        try:
            supervisor_id = int(supervisor_id)
        except (ValueError, TypeError):
            return JsonResponse({"msg": "Supervisor value not is valid"}, status=400)

        supervisor = UserModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            id=supervisor_id,
            user_level_id__user_level='Supervisor'
        )

        if not supervisor.exists():
            return JsonResponse(data={"msg": "Supervisor not found"}, status=HTTPStatus.NOT_FOUND)

        user_gotten.update(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            user_level_id=user_level_gotten.first(),
            supervisor=supervisor.first(),
        )

    else:

        user_gotten.update(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            user_level_id=user_level_gotten.first(),
        )

    if permissions:
        user_gotten = user_gotten.first()
        user_gotten.groups.remove(*user_permissions_not_given)
        user_gotten.groups.add(*user_permissions_given)

    return JsonResponse(data={'msg': 'User updated'}, status=HTTPStatus.OK)


@login_required
def view_pdf(request, file_id):

    file = FileModel.objects.filter(id=file_id)
    user = request.user
    user_level = request.user.user_level_id.user_level

    if not file.exists():
        return JsonResponse(data={"msg": "Nonexistent file"}, status=HTTPStatus.NOT_FOUND)

    file = file.first()

    if user_level == 'Superusuario' or user_level == 'Supervisor':

        complaint = ComplaintModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            user_id__id=user.id,
            id=file.complaint_id,
        )
    else:

        user_permissions = get_grouped_user_permissions(user, user_level)

        complaint = ComplaintModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            user_id__id=user.id,
            id=file.complaint_id,
            city_id__city__in=user_permissions['cities'],
            priority_id__priority__in=user_permissions['priorities'],
            status_id__status__in=user_permissions['statuses']
        )

    if not complaint.exists():
        return JsonResponse(data={"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    decrypted_content = file.decrypted_file

    response = HttpResponse(decrypted_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{file.file.name}"'

    return response
