from django.views.decorators.csrf import csrf_exempt
import json

from datetime import datetime
from http import HTTPStatus

from django.utils import timezone
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, F, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.conf import settings

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser

from etica_y_valores.enterprises.models import EnterpriseModel
from ..models import (
    ComplaintModel,
    CommentModel,
    EmailModel,
    PhoneModel,
    FileModel,
    LogModel,
    PriorityCategoryModel,
    StatusCategoryModel,
    ClassificationCategoryModel,
    ChannelCategoryModel,
    CityCategoryModel,
    PhoneTypeCategoryModel,
    RelationCategoryModel
)
from etica_y_valores.users.utils.user_handlers import get_grouped_user_permissions


@require_GET
def home_view(request):
    """
    This function returns our home view
    """

    template_name = 'complaints/home.html'

    return render(request, template_name)


@require_GET
def search_complaint(request, code):
    """
    This method verify if a complaint exists and return the url
    """

    complaint = ComplaintModel.objects.filter(id=code)

    data = {
        'url': ''
    }

    if complaint.exists():
        url = reverse('app_complaints:complaint_created', args=[code])
        data['url'] = url

        return JsonResponse(data=data, status=HTTPStatus.FOUND)
    else:
        return JsonResponse(data=data, status=HTTPStatus.NOT_FOUND)


@login_required
@require_http_methods(["DELETE"])
def delete_complaint(request, code):

    complaint = ComplaintModel.objects.filter(id=code)

    if not complaint.exists():
        return JsonResponse(data={"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    complaint.update(
        status_id=StatusCategoryModel.objects.get(status='Desestimados'))

    return JsonResponse({'msg': 'complaint not proceeded'}, status=HTTPStatus.OK)


@login_required
@require_http_methods(["PUT"])
def close_complaint(request, code):
    """
    This view closes a complaint
    """

    complaint = ComplaintModel.objects.filter(id=code)

    if not complaint.exists():
        return JsonResponse({'msg': 'complaint not found'}, status=HTTPStatus.NOT_FOUND)

    status = StatusCategoryModel.objects.filter(status='Resolución')

    if not status.exists():
        return JsonResponse({'msg': 'status not found'}, status=HTTPStatus.NOT_FOUND)

    complaint.update(
        status_id=status.first(),
        close_date=timezone.now()
    )

    return JsonResponse({'msg': 'complaint closed'}, status=HTTPStatus.OK)


@login_required
@require_GET
def complaints_count(request):
    """
    This function returns the count of complaints
    """

    # user
    user = request.user

    # user level
    user_level = user.user_level_id.user_level

    table_complaints_staff_path = reverse('app_users:table_complaints_staff')
    home_staff_path = reverse('app_users:home_staff')
    table_complaints_ended_staff_path = reverse(
        'app_users:table_complaints_ended_staff')
    status_staff_path = reverse(
        'app_users:status_staff', args=['placeholder'])
    city_staff_path = reverse(
        'app_users:city_staff', args=['placeholder'])
    priority_staff_path = reverse(
        'app_users:priority_staff', args=['placeholder'])
    classification_staff_path = reverse(
        'app_users:classification_staff', args=['placeholder'])
    channel_staff_path = reverse(
        'app_users:channel_staff', args=['placeholder'])

    if user_level == 'Superusuario':

        # all complaints
        all_complaints = ComplaintModel.objects.filter(
            enterprise_id__subdomain=request.get_host())

        # all complaints opened
        all_complaints_opened = all_complaints.exclude(
            status_id__status__in=['Desestimados', 'Resolución'])

        # all complaints opened count
        all_complaints_opened_count = all_complaints_opened.count()

        # all complaints closed count
        all_complaints_closed_count = all_complaints.filter(
            status_id__status='Resolución').count()

        # all complaints by status
        all_complaints_by_status = list(
            all_complaints_opened.values(
                status=F('status_id__status')
            ).annotate(
                count=Count('id')
            ))

        # all complaints by city
        all_complaints_by_city = list(all_complaints_opened.values(
            city=F('city_id__city')
        ).annotate(
            count=Count('city')
        ))

        # all complaints by priority
        all_complaints_by_priority = list(all_complaints_opened.values(
            priority=F('priority_id__priority')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by classification
        all_complaints_by_classification = list(all_complaints_opened.values(
            classification=F('classification_id__classification')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by communication channel
        all_complaints_by_channel = list(all_complaints_opened.values(
            channel=F('channel_id__channel')
        ).annotate(
            count=Count('id')
        ))

        response = JsonResponse(data={
            'all_complaints_opened_count': all_complaints_opened_count,
            'all_complaints_closed_count': all_complaints_closed_count,
            'all_complaints_by_status': all_complaints_by_status,
            'all_complaints_by_city': all_complaints_by_city,
            'all_complaints_by_priority': all_complaints_by_priority,
            'all_complaints_by_classification': all_complaints_by_classification,
            'all_complaints_by_channel': all_complaints_by_channel,
            'home_staff_path': home_staff_path,
            'table_complaints_staff_path': table_complaints_staff_path,
            'table_complaints_ended_staff_path': table_complaints_ended_staff_path,
            'status_staff_path': status_staff_path,
            'city_staff_path': city_staff_path,
            'priority_staff_path': priority_staff_path,
            'classification_staff_path': classification_staff_path,
            'channel_staff_path': channel_staff_path,
            'list_user_staff_path': reverse('app_users:list_user_staff')
        }, status=HTTPStatus.OK)

    elif user_level == 'Supervisor':

        # all complaints
        all_complaints = ComplaintModel.objects.filter(
            enterprise_id__subdomain=request.get_host())

        # all complaints opened
        all_complaints_opened = all_complaints.exclude(
            status_id__status__in=['Desestimados', 'Resolución'])

        # all complaints opened count
        all_complaints_opened_count = all_complaints_opened.count()

        # all complaints closed count
        all_complaints_closed_count = all_complaints.filter(
            status_id__status='Resolución').count()

        # all complaints by status
        all_complaints_by_status = list(
            all_complaints_opened.values(
                status=F('status_id__status')
            ).annotate(
                count=Count('id')
            ))

        # all complaints by city
        all_complaints_by_city = list(all_complaints_opened.values(
            city=F('city_id__city')
        ).annotate(
            count=Count('city')
        ))

        # all complaints by priority
        all_complaints_by_priority = list(all_complaints_opened.values(
            priority=F('priority_id__priority')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by classification
        all_complaints_by_classification = list(all_complaints_opened.values(
            classification=F('classification_id__classification')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by communication channel
        all_complaints_by_channel = list(all_complaints_opened.values(
            channel=F('channel_id__channel')
        ).annotate(
            count=Count('id')
        ))

        response = JsonResponse(data={
            'all_complaints_opened_count': all_complaints_opened_count,
            'all_complaints_closed_count': all_complaints_closed_count,
            'all_complaints_by_status': all_complaints_by_status,
            'all_complaints_by_city': all_complaints_by_city,
            'all_complaints_by_priority': all_complaints_by_priority,
            'all_complaints_by_classification': all_complaints_by_classification,
            'all_complaints_by_channel': all_complaints_by_channel,
            'home_staff_path': home_staff_path,
            'table_complaints_staff_path': table_complaints_staff_path,
            'table_complaints_ended_staff_path': table_complaints_ended_staff_path,
            'status_staff_path': status_staff_path,
            'city_staff_path': city_staff_path,
            'priority_staff_path': priority_staff_path,
            'classification_staff_path': classification_staff_path,
            'channel_staff_path': channel_staff_path,
            'list_user_staff_path': reverse('app_users:list_user_staff')
        }, status=HTTPStatus.OK)

    else:

        # all user groups (permissions)
        user_permissions = get_grouped_user_permissions(user, user_level)

        # all user complaints
        all_user_complaints = ComplaintModel.objects.filter(
            enterprise_id__subdomain=request.get_host(),
            user_id__id=user.id,
            city_id__city__in=user_permissions['cities'],
            priority_id__priority__in=user_permissions['priorities'],)

        # all user complaints opened
        all_complaints_opened = all_user_complaints.exclude(
            status_id__status__in=['Desestimados', 'Resolución'])

        # all user complaints opened count
        all_complaints_opened_count = all_complaints_opened.count()

        # all user complaints closed count
        all_complaints_closed_count = all_user_complaints.filter(
            status_id__status='Resolución').count()

        # all user complaints by status
        all_complaints_by_status = list(
            all_complaints_opened.values(
                status=F('status_id__status')
            ).annotate(
                count=Count('id')
            ))

        # all user complaints by city
        all_complaints_by_city = list(all_complaints_opened.values(
            city=F('city_id__city')
        ).annotate(
            count=Count('city')
        ))

        # all complaints by priority
        all_complaints_by_priority = list(all_complaints_opened.values(
            priority=F('priority_id__priority')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by classification
        all_complaints_by_classification = list(all_complaints_opened.values(
            classification=F('classification_id__classification')
        ).annotate(
            count=Count('id')
        ))

        # all complaints by communication channel
        all_complaints_by_channel = list(all_complaints_opened.values(
            channel=F('channel_id__channel')
        ).annotate(
            count=Count('id')
        ))

        response = JsonResponse(data={
            'all_complaints_opened_count': all_complaints_opened_count,
            'all_complaints_closed_count': all_complaints_closed_count,
            'all_complaints_by_status': all_complaints_by_status,
            'all_complaints_by_city': all_complaints_by_city,
            'all_complaints_by_priority': all_complaints_by_priority,
            'all_complaints_by_classification': all_complaints_by_classification,
            'all_complaints_by_channel': all_complaints_by_channel,
            'home_staff_path': home_staff_path,
            'table_complaints_staff_path': table_complaints_staff_path,
            'table_complaints_ended_staff_path': table_complaints_ended_staff_path,
            'status_staff_path': status_staff_path,
            'city_staff_path': city_staff_path,
            'priority_staff_path': priority_staff_path,
            'classification_staff_path': classification_staff_path,
            'channel_staff_path': channel_staff_path,
            'list_user_staff_path': reverse('app_users:list_user_staff') if 'Usuarios' in user_permissions['tasks'] else ''
        }, status=HTTPStatus.OK)

    return response


@require_GET
@login_required
def get_classification_types(request):
    """
    This function returns the classification types
    """

    return JsonResponse(data={
        'classification_types': list(ClassificationCategoryModel.objects.values('id', 'classification'))
    }, status=HTTPStatus.OK)


@require_GET
@login_required
def get_priority_types(request):
    """
    This function returns the priority types
    """

    user = request.user
    user_level = user.user_level_id.user_level

    if user_level == 'Superusuario' or user_level == 'Supervisor':

        return JsonResponse(data={
            'priority_types': list(PriorityCategoryModel.objects.values('id', 'priority'))
        }, status=HTTPStatus.OK)

    else:

        user_permissions = get_grouped_user_permissions(user, user_level)

        return JsonResponse(data={
            'priority_types': list(PriorityCategoryModel.objects.filter(
                priority__in=user_permissions['priorities']).values('id', 'priority'))
        }, status=HTTPStatus.OK)


@require_GET
@login_required
def get_status_types(request):
    """
    This function returns the status types
    """

    user = request.user
    user_level = user.user_level_id.user_level

    if user_level == 'Superusuario' or user_level == 'Supervisor':

        return JsonResponse(data={
            'status_types': list(StatusCategoryModel.objects.values('id', 'status'))
        }, status=HTTPStatus.OK)

    else:

        user_permissions = get_grouped_user_permissions(user, user_level)

        return JsonResponse(data={
            'status_types': list(StatusCategoryModel.objects.filter(
                status__in=user_permissions['statuses']).values('id', 'status'))
        }, status=HTTPStatus.OK)


@require_GET
@login_required
def complaints_paginator(request):
    """
    This function returns the complaints by page
    """

    complaints = ComplaintModel.objects.all()
    page_number = request.GET.get('page', 1)

    # Pagination
    paginator = Paginator(complaints, 2)
    page_obj = paginator.get_page(page_number)

    complaints_paginated = list(page_obj.object_list.annotate(
        city=F('city_id__city'),
        priority=F('priority_id__priority'),
        status=F('status_id__status'),
        classification=F('classification_id__classification'),
        first_name=Coalesce(F('user_id__first_name'), Value(''))
    ).values('id', 'city', 'priority', 'status', 'classification', 'first_name', 'created_at'))

    pagination_data = {
        'current_page': page_obj.number,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'total_pages': paginator.num_pages,
        'first_page': 1,
        'last_page': paginator.num_pages
    }

    return JsonResponse({'complaints': complaints_paginated, 'pagination': pagination_data}, status=HTTPStatus.OK)


@require_http_methods(["POST"])
def create_complaint(request):
    """
    This function validates the form and creates a Complaint.
    """

    enterprise_relation = request.POST.get('enterprise_relation')
    city = request.POST.get('city')
    business_unit = request.POST.get('business_unit')
    place = request.POST.get('place')
    date_time = request.POST.get('date_time')
    names_involved = request.POST.get('names_involved')
    report_classification = request.POST.get('report_classification')
    detailed_description = request.POST.get('detailed_description')
    name = request.POST.get('name')
    communication_channel = request.POST.get('communication_channel')

    emails = request.POST.getlist('emails', '')
    phone_numbers = request.POST.getlist('phone_numbers', '')
    phone_types = request.POST.getlist('phone_types', '')
    files = request.FILES.getlist('files')

    # --------------- Validations ----------------

    if not all([enterprise_relation, date_time, names_involved, report_classification,
                detailed_description, place, business_unit, city, communication_channel]):
        return JsonResponse(data={"msg": "There are empty required fields"}, status=HTTPStatus.BAD_REQUEST)

    try:
        # Become the string into a datetime object
        date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')

        # Validate that the date and time are not in the future
        if date_time > datetime.now():
            raise ValidationError(
                'Date and time cannot be in the future')

    except ValueError:
        return JsonResponse(data={"msg": "Invalid date format"}, status=HTTPStatus.BAD_REQUEST)
    except ValidationError as e:
        return JsonResponse(data={"msg": str(e)}, status=HTTPStatus.BAD_REQUEST)

    city = CityCategoryModel.objects.filter(city=city)

    if not city.exists():
        return JsonResponse(data={"msg": "Nonexistent city"}, status=HTTPStatus.BAD_REQUEST)

    classification = ClassificationCategoryModel.objects.filter(
        classification=report_classification)

    if not classification.exists():
        return JsonResponse(data={"msg": "Nonexistent classification"}, status=HTTPStatus.BAD_REQUEST)

    relation = RelationCategoryModel.objects.filter(
        relation=enterprise_relation)

    if not relation.exists():
        return JsonResponse(data={"msg": "Nonexistent relation"}, status=HTTPStatus.BAD_REQUEST)

    channel = ChannelCategoryModel.objects.filter(
        channel=communication_channel)

    if not channel.exists():
        return JsonResponse(data={"msg": "Nonexistent channel"}, status=HTTPStatus.BAD_REQUEST)

    phone_types = PhoneTypeCategoryModel.objects.filter(
        phone_type__in=phone_types)

    if phone_types.count() != len(phone_types):
        return JsonResponse(data={"msg": "Nonexistent phone type"}, status=HTTPStatus.BAD_REQUEST)

    city = city.first()
    relation = relation.first()
    classification = classification.first()
    channel = channel.first()

    # --------------- Inserts ----------------

    complaint = ComplaintModel.objects.create(
        business_unit=business_unit,
        place=place,
        date_time=timezone.make_aware(date_time),
        names_involved=names_involved,
        detailed_description=detailed_description,
        name=name,
        classification_id=classification,
        relation_id=relation,
        city_id=city,
        channel_id=channel,
        priority_id=PriorityCategoryModel.objects.get(priority='Sin asignar'),
        status_id=StatusCategoryModel.objects.get(
            status='Pendiente de Asignar'),
        enterprise_id=EnterpriseModel.objects.get(subdomain=request.get_host())
    )

    for email in emails:
        EmailModel.objects.create(
            email=email,
            complaint_id=complaint,
        )

    for phone_type, phone_number in zip(phone_types, phone_numbers):
        PhoneModel.objects.create(
            phone_type=phone_type,
            phone_number=phone_number,
            complaint_id=complaint,
        )

    for file in files:
        FileModel.objects.create(
            file=file,
            complaint_id=complaint,
        )

    LogModel.objects.create(
        complaint_id=complaint,
        movement='Denuncia creada',
    )

    url = reverse('app_complaints:complaint_created', args=[complaint.id])

    return JsonResponse(data={'url': url}, status=HTTPStatus.CREATED)


@require_http_methods(["PUT"])
def update_complaint(request, code):

    request.upload_handlers = [TemporaryFileUploadHandler()]

    parser = MultiPartParser(request.META, request,
                             request.upload_handlers, request.encoding)
    data, files = parser.parse()

    # Ahora puedes acceder a los campos de formulario y archivos
    relation = data.get('relation', '')
    city = data.get('city', '')
    business_unit = data.get('business_unit', '')
    place = data.get('place', '')
    date_time = data.get('date_time', '')
    names_involved = data.get('names_involved', '')
    classification = data.get('report_classification', '')
    detailed_description = data.get('detailed_description', '')
    name = data.get('name', '')
    channel = data.get('communication_channel', '')
    status = data.get('status', '')

    emails = data.getlist('emails')
    phone_numbers = data.getlist('phone_numbers')
    phone_types = data.getlist('phone_types')
    files = files.getlist('files')

    # --------------- Validations ----------------

    if not all([relation, date_time, names_involved, classification,
                detailed_description, place, business_unit, city, channel]):
        return JsonResponse(data={"msg": "There are empty required fields"}, status=HTTPStatus.BAD_REQUEST)

    try:
        # Become the string into a datetime object
        date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')

        # Validate that the date and time are not in the future
        if date_time > datetime.now():
            raise ValidationError(
                'Date and time cannot be in the future')

    except ValueError:
        return JsonResponse(data={"msg": "Invalid date format"}, status=HTTPStatus.BAD_REQUEST)
    except ValidationError as e:
        return JsonResponse(data={"msg": str(e)}, status=HTTPStatus.BAD_REQUEST)

    city = CityCategoryModel.objects.filter(city=city)

    if not city.exists():
        print('city not found')
        return JsonResponse(data={"msg": "Nonexistent city"}, status=HTTPStatus.BAD_REQUEST)

    classification = ClassificationCategoryModel.objects.filter(
        classification=classification)

    if not classification.exists():
        print('classification not found')
        return JsonResponse(data={"msg": "Nonexistent classification"}, status=HTTPStatus.BAD_REQUEST)

    relation = RelationCategoryModel.objects.filter(
        relation=relation)

    if not relation.exists():
        print('relation not found')
        return JsonResponse(data={"msg": "Nonexistent relation"}, status=HTTPStatus.BAD_REQUEST)

    channel = ChannelCategoryModel.objects.filter(
        channel=channel)

    if not channel.exists():
        print('channel not found')
        return JsonResponse(data={"msg": "Nonexistent channel"}, status=HTTPStatus.BAD_REQUEST)

    phone_types_gotten = PhoneTypeCategoryModel.objects.filter(
        phone_type__in=phone_types)

    if phone_types_gotten.count() != len(phone_types):
        print('phone type not found')
        return JsonResponse(data={"msg": "Nonexistent phone type"}, status=HTTPStatus.BAD_REQUEST)

    status = StatusCategoryModel.objects.filter(status=status)

    if not status.exists():
        print('status not found')
        return JsonResponse(data={"msg": "Nonexistent status"}, status=HTTPStatus.BAD_REQUEST)

    city = city.first()
    relation = relation.first()
    classification = classification.first()
    channel = channel.first()
    status = status.first()

    # --------------- Updates ----------------

    complaint = ComplaintModel.objects.filter(
        id=code,
        enterprise_id__subdomain=request.get_host()
    )

    if not complaint.exists():
        print('complaint not found')
        return JsonResponse(data={"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    complaint.update(
        business_unit=business_unit,
        place=place,
        date_time=timezone.make_aware(date_time),
        names_involved=names_involved,
        detailed_description=detailed_description,
        name=name,
        classification_id=classification,
        relation_id=relation,
        city_id=city,
        channel_id=channel,
        status_id=status,
        enterprise_id=EnterpriseModel.objects.get(subdomain=request.get_host())
    )

    complaint = complaint.first()

    LogModel.objects.create(
        complaint_id=complaint,
        movement='Se han actualizado los datos de la denuncia',
    )

    for email in emails:
        EmailModel.objects.create(
            email=email,
            complaint_id=complaint,
        )

        LogModel.objects.create(
            complaint_id=complaint,
            movement='Se han agregado nuevos correos a la denuncia',
        )

    for phone_type, phone_number in zip(phone_types_gotten, phone_numbers):
        PhoneModel.objects.create(
            phone_type=phone_type,
            phone_number=phone_number,
            complaint_id=complaint,
        )

        LogModel.objects.create(
            complaint_id=complaint,
            movement='Se han agregado nuevos número de teléfono a la denuncia',
        )

    for file in files:
        print(file)
        FileModel.objects.create(
            file=file,
            complaint_id=complaint,
        )

        LogModel.objects.create(
            complaint_id=complaint,
            movement='Se han agregado nuevos archivos a la denuncia',
        )

    return JsonResponse(data={"msg": "Complaint updated successfully"}, status=200)


@require_http_methods(["PUT"])
def update_complaint_priority(request, code):
    """
    This function updates the priority of a complaint
    """

    new_priority = json.loads(request.body).get('new_priority', '')

    if not new_priority:
        return JsonResponse(data={"msg": "new priority is required"}, status=HTTPStatus.BAD_REQUEST)

    complaint = ComplaintModel.objects.filter(id=code)

    if not complaint.exists():
        return JsonResponse(data={"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    priority = PriorityCategoryModel.objects.filter(id=new_priority)

    if not priority.exists():
        return JsonResponse(data={"msg": "Priority not found"}, status=HTTPStatus.NOT_FOUND)

    priority_object = priority.first()
    complaint.update(priority_id=priority_object)

    LogModel.objects.create(
        complaint_id=complaint.first(),
        user_id=request.user,
        movement=f'Prioridad de denuncia actualizada a {priority_object.priority}',
    )

    return JsonResponse({'msg': 'complaint status updated'}, status=HTTPStatus.OK)


@require_http_methods(["PUT"])
# @login_required
@csrf_exempt
def update_dynamic_complaint(request, code):
    """
    This view updates the complaint given 2 values
    """

    try:
        data = json.loads(request.body)

        first_param = data.get('first_param', '')
        second_param = data.get('second_param', '')

        if not first_param or not second_param:
            return JsonResponse({"msg": "Empty required fields"}, status=HTTPStatus.BAD_REQUEST)

        if not 'field' in first_param or not 'value' in first_param or not 'field' in second_param or not 'value' in second_param:
            return JsonResponse({"msg": "Invalid JSON format"}, status=HTTPStatus.BAD_REQUEST)

    except json.JSONDecodeError:
        return JsonResponse({"msg": "Invalid JSON format"}, status=HTTPStatus.BAD_REQUEST)

    available_related_fields_to_update = {
        'classification': ClassificationCategoryModel,
        'priority': PriorityCategoryModel,
        'status': StatusCategoryModel,
    }

    if first_param['field'] not in available_related_fields_to_update or second_param['field'] not in available_related_fields_to_update:
        return JsonResponse({"msg": "Invalid field to update"}, status=HTTPStatus.BAD_REQUEST)

    first_model = available_related_fields_to_update[first_param['field']]
    second_model = available_related_fields_to_update[second_param['field']]

    try:
        first_model._meta.get_field(first_param['field'])
        second_model._meta.get_field(second_param['field'])
    except:
        return JsonResponse({"msg": "Nonexistent fields"}, status=HTTPStatus.BAD_REQUEST)

    first_instance = first_model.objects.filter(
        **{first_param['field']: first_param['value']})
    second_instance = second_model.objects.filter(
        **{second_param['field']: second_param['value']})

    if not first_instance.exists() or not second_instance.exists():
        return JsonResponse({"msg": "Instances for params not found"}, status=HTTPStatus.NOT_FOUND)

    first_instance = first_instance.first()
    second_instance = second_instance.first()

    complaint = ComplaintModel.objects.filter(id=code)

    if not complaint.exists():
        return JsonResponse({"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    complaint.update(**{f"{first_param['field']}_id": first_instance,
                     f"{second_param['field']}_id": second_instance})

    return JsonResponse(data={"msg": "Complaint updated successfully"}, status=HTTPStatus.OK)


class ComplaintCreatedView(View):

    template_name = 'complaints/complaint_created.html'

    def get(self, request, code, *args, **kwargs):
        """
        This method return our complaint created view
        """

        complaint = ComplaintModel.objects.filter(id=code)

        context = {
            'url': ''
        }

        if complaint.exists():
            url = reverse('app_complaints:status_complaint', args=[code])
            context['url'] = f'{settings.BASE_URL}{url}'

        return render(request, self.template_name, context)


class StatusComplaintView(ListView):

    model = LogModel
    template_name = 'complaints/status_complaint.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_queryset(self):
        """
        This method ensures that the results are ordered
        """
        code = self.kwargs.get('code', None)
        queryset = LogModel.objects.filter(
            complaint_id=code).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add the complaint code to the context
        """
        context = super().get_context_data(**kwargs)

        code = self.kwargs.get('code', None)
        complaint = ComplaintModel.objects.filter(id=code).first()

        context['code'] = code if complaint else ''

        return context


class CommentsView(View, LoginRequiredMixin):

    template_name = 'complaints/comments.html'

    def get(self, request, code, *args, **kwargs):
        """
        This method return our comments from a complaint
        """

        complaint = ComplaintModel.objects.filter(
            id=code, enterprise_id__subdomain=request.get_host())

        if complaint.exists():

            data = {
                'comments': []
            }

            comments = CommentModel.objects.filter(
                complaint_id=code).order_by('-created_at')
            data['comments'] = [
                {
                    'user': comment.user_id.username if comment.user_id else 'Anónimo',
                    'comment': comment.comment,
                    'date': timezone.localtime(comment.created_at).strftime('%d-%m-%Y'),
                }
                for comment in comments
            ]

            return JsonResponse(data=data, status=HTTPStatus.FOUND)

        return JsonResponse(data={'msg': 'Complaint not found'}, status=HTTPStatus.NOT_FOUND)


@login_required
@require_http_methods(["POST"])
def create_comment(request):
    """
    This view creates a comment
    """

    code = request.POST.get('code')
    comment = request.POST.get('comment')

    complaint = ComplaintModel.objects.filter(
        enterprise_id__subdomain=request.get_host(),
        id=code)

    if not complaint.exists():
        return JsonResponse(data={"msg": "Complaint not found"}, status=HTTPStatus.NOT_FOUND)

    user = request.user
    user_level = user.user_level_id.user_level

    if user_level == 'Superusuario' or user_level == 'Supervisor':

        CommentModel.objects.create(
            complaint_id=complaint.first(),
            user_id=user,
            comment=comment
        )

        return JsonResponse(data={'msg': 'comment created'}, status=HTTPStatus.CREATED)

    else:
        user_permissions = get_grouped_user_permissions(user, user_level)

        complaint = complaint.filter(
            city_id__city__in=user_permissions['cities'],
            priority_id__priority__in=user_permissions['priorities'],
            status_id__status__in=user_permissions['statuses']
        )

        if not complaint.exists():
            return JsonResponse(data={'msg': 'Without enough permissions to access to the complaint'}, status=HTTPStatus.FORBIDDEN)

        if not 'Comentarios' in user_permissions['tasks']:
            return JsonResponse(data={'msg': 'Without enough permissions to add comment'}, status=HTTPStatus.FORBIDDEN)

        CommentModel.objects.create(
            complaint_id=complaint.first(),
            user_id=user,
            comment=comment
        )

        return JsonResponse(data={'msg': 'Without enough permissions to add comment'}, status=HTTPStatus.FORBIDDEN)


class LogsView(View, LoginRequiredMixin):

    def get(self, request, code, *args, **kwargs):
        """
        This method return our logs from a complaint
        """

        complaint = ComplaintModel.objects.filter(
            id=code, enterprise_id__subdomain=request.get_host())

        if complaint.exists():

            data = {
                'logs': []
            }

            logs = LogModel.objects.filter(
                complaint_id=complaint.first()).order_by('-created_at')

            data['logs'] = [
                {
                    'movement': log.movement,
                    'date': timezone.localtime(log.created_at).strftime('%d-%m-%Y'),
                }
                for log in logs
            ]

            return JsonResponse(data=data, status=HTTPStatus.FOUND)

        return JsonResponse(data={'msg': 'Complaint not found'}, status=HTTPStatus.NOT_FOUND)


class ComplaintView(View, LoginRequiredMixin):

    def get_complaint_info(self, complaint):
        """
        This method returns the complaint info
        """

        files = [
            {
                'id': file_obj.id,
                'file_name': file_obj.file.name.split('/')[-1],
                'file_url': reverse('app_users:staff_view_pdf', args=[file_obj.id])
            }
            for file_obj in FileModel.objects.filter(complaint_id=complaint)
        ]

        emails = [
            {
                'id': email_obj.id,
                'email': email_obj.email
            }
            for email_obj in EmailModel.objects.filter(complaint_id=complaint)
        ]

        phones = [
            {
                'id': phone_obj.id,
                'phone_type': phone_obj.phone_type.phone_type,
                'phone_number': phone_obj.phone_number
            }
            for phone_obj in PhoneModel.objects.filter(complaint_id=complaint)
        ]

        assigned_user = complaint.user_id

        complaint_data = {
            'files': files,
            'emails': emails,
            'phones': phones,
            'complaint': {
                'id': complaint.id,
                'business_unit': complaint.decrypted_business_unit,
                'place': complaint.decrypted_place,
                'date_time': timezone.localtime(complaint.date_time).strftime('%Y-%m-%dT%H:%M'),
                'close_date': timezone.localtime(complaint.close_date).strftime('%Y-%m-%dT%H:%M') if complaint.close_date else '',
                'names_involved': complaint.decrypted_names_involved,
                'detailed_description': complaint.decrypted_detailed_description,
                'name': complaint.decrypted_name,
                'classification': complaint.classification_id.classification,
                'relation': complaint.relation_id.relation,
                'city': complaint.city_id.city,
                'channel': complaint.channel_id.channel,
                'priority': complaint.priority_id.priority,
                'status': complaint.status_id.status,
                'enterprise': complaint.enterprise_id.enterprise_name,
                'created_at': timezone.localtime(complaint.created_at).strftime('%d-%m-%Y'),
                'assigned_user': {'id': assigned_user.id, 'username': assigned_user.username} if assigned_user else ''
            }}

        return complaint_data

    def get(self, request, code, *args, **kwargs):
        """
        This method return a complaint
        """

        user = request.user
        user_level = user.user_level_id.user_level

        complaint = ComplaintModel.objects.filter(id=code)

        if not complaint.exists():
            return JsonResponse(data={'msg': 'Complaint not found'}, status=HTTPStatus.NOT_FOUND)

        if user_level == 'Superusuario' or user_level == 'Supervisor':

            return JsonResponse(data=self.get_complaint_info(complaint.first()), status=HTTPStatus.OK)

        else:

            user_permissions = get_grouped_user_permissions(user, user_level)

            if not complaint.filter(
                enterprise_id__subdomain=request.get_host(),
                user_id__id=user.id,
                city_id__city__in=user_permissions['cities'],
                priority_id__priority__in=user_permissions['priorities'],
                status_id__status__in=user_permissions['statuses']
            ).exists():
                return JsonResponse(data={'msg': 'without enough permissions to get complaint'}, status=HTTPStatus.FORBIDDEN)

            return JsonResponse(data=self.get_complaint_info(complaint.first()), status=HTTPStatus.OK)
