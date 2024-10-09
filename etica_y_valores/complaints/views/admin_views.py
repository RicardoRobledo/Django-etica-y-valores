from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from ..models import (
    FileModel,
)


@login_required
@staff_member_required
def view_pdf(request, file_id):

    obj = FileModel.objects.get(id=file_id)

    decrypted_content = obj.decrypted_file

    response = HttpResponse(decrypted_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{obj.file.name}"'

    return response
