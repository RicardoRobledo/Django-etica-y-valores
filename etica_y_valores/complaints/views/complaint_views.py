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

from ..models import Complaint, Email, Phone, File


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

    complaint = Complaint.objects.filter(id=code)

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

    if not all([enterprise_relation, date, time, names_involved, report_classification,
                detailed_description, place, business_unit, city, communication_channel]):
        return JsonResponse(data={"msg": "There are empty required fields"}, status=HTTPStatus.BAD_REQUEST)

    date = parse_date(date)

    if date > timezone.now().date():
        return JsonResponse(data={"msg": "Date can't be in the future"}, status=HTTPStatus.BAD_REQUEST)

    time = parse_time(time)
    if time is None:
        return JsonResponse(data={"msg": "Invalid time"}, status=HTTPStatus.BAD_REQUEST)

    complaint = Complaint.objects.create(
        enterprise_relation=enterprise_relation,
        date=date,
        time=time,
        names_involved=names_involved,
        report_classification=report_classification,
        detailed_description=detailed_description,
        place=place,
        business_unit=business_unit,
        city=city,
        name=name,
        communication_channel=communication_channel,
    )

    for email in emails:
        Email.objects.create(
            email=email,
            complaint_id=complaint,
        )

    for phone_type, phone_number in zip(phone_types, phone_numbers):
        Phone.objects.create(
            phone_type=phone_type,
            phone_number=phone_number,
            complaint_id=complaint,
        )

    for file in files:
        File.objects.create(
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

        complaint = Complaint.objects.filter(id=code)

        context = {
            'url': ''
        }

        if complaint.exists():
            url = reverse('app_complaints:status_complaint', args=[code])
            context['url'] = url

        return render(request, self.template_name, context)


class StatusComplaintView(View):

    template_name = 'complaints/status_complaint.html'

    def get(self, request, code, *args, **kwargs):
        """
        This method return our status complaint view
        """

        complaint = Complaint.objects.filter(id=code)

        context = {
            'code': ''
        }

        if complaint.exists():
            context['code'] = code

        return render(request, self.template_name, context)
