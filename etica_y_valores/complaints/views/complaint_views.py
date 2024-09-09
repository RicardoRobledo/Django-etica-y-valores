from http import HTTPStatus

from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings

from ..models import (
    ComplaintModel,
    EmailModel,
    PhoneModel,
    FileModel,
    PriorityCategoryModel,
    StatusCategoryModel,
    ClassificationCategoryModel,
    ChannelCategoryModel,
    CityCategoryModel,
    PhoneTypeCategoryModel,
    RelationCategoryModel
)


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


@require_POST
def create_complaint(request):
    """
    This function validates the form and creates a Complaint.
    """

    enterprise_relation = request.POST.get('enterprise_relation')
    city = request.POST.get('city')
    business_unit = request.POST.get('business_unit')
    place = request.POST.get('place')
    date = request.POST.get('date')
    time = request.POST.get('time')
    names_involved = request.POST.get('names_involved')
    report_classification = request.POST.get('report_classification')
    detailed_description = request.POST.get('detailed_description')
    name = request.POST.get('name')
    communication_channel = request.POST.get('communication_channel')

    emails = request.POST.getlist('emails')
    phone_numbers = request.POST.getlist('phone_numbers')
    phone_types = request.POST.getlist('phone_types')
    files = request.FILES.getlist('files')

    # --------------- Validations ----------------

    if not all([enterprise_relation, date, time, names_involved, report_classification,
                detailed_description, place, business_unit, city, communication_channel]):
        return JsonResponse(data={"msg": "There are empty required fields"}, status=HTTPStatus.BAD_REQUEST)

    date = parse_date(date)

    if date > timezone.now().date():
        return JsonResponse(data={"msg": "Date can't be in the future"}, status=HTTPStatus.BAD_REQUEST)

    time = parse_time(time)
    if time is None:
        return JsonResponse(data={"msg": "Invalid time"}, status=HTTPStatus.BAD_REQUEST)

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

    if phone_type.count() != len(phone_types):
        return JsonResponse(data={"msg": "Nonexistent phone type"}, status=HTTPStatus.BAD_REQUEST)

    # --------------- Inserts ----------------

    complaint = ComplaintModel.objects.create(
        business_unit=business_unit,
        place=place,
        date=date,
        time=time,
        names_involved=names_involved,
        detailed_description=detailed_description,
        name=name,
        classification_id=classification,
        relation_id=relation,
        city_id=city,
        channel_id=channel,
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

    url = reverse('app_complaints:complaint_created', args=[complaint.id])

    return JsonResponse(data={'url': url}, status=HTTPStatus.CREATED)


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


class StatusComplaintView(View):

    template_name = 'complaints/status_complaint.html'

    def get(self, request, code, *args, **kwargs):
        """
        This method return our status complaint view
        """

        complaint = ComplaintModel.objects.filter(id=code)

        context = {
            'code': ''
        }

        if complaint.exists():
            context['code'] = code

        return render(request, self.template_name, context)
