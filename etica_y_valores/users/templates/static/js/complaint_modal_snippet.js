let fileId = 0;
let filesQuantity = 0; 

let emailId = 0;
let emailsQuantity = 0; 

let phoneId = 0;
let phonesQuantity = 0;

let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$/;
let phonePattern = /^[0-9]{10}$/;

$(document).ready(function() {
    $('body').css('display', 'none');
    $('body').fadeIn(1000);

    $('#modalComplaint .modal-body .container').hide();
});


// -------------------Events------------------

$('#search-complaint').on('click', async function(event){

    const code = $('#code');

    // Remueve la clase is-invalid si existe antes de la validación
    code.removeClass('is-invalid');

    // Realiza la solicitud al servidor
    const response = await fetch(base_url+`/search_complaint/${code.val()}/`, {
        method: 'GET',
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data['url'] && data['url'] !== '') {
            // Redirige si se recibe una URL válida
            window.location.href = data['url'];
        } else {
            // Si no hay una URL válida, muestra el mensaje de feedback
            code.addClass('is-invalid');
        }
    }).catch(error => {
        // Manejo de errores de la solicitud, muestra el feedback en caso de error
        code.addClass('is-invalid');
        console.error('Error:', error);
    });

});

$('#btn-update-complaint').on('click', async function(event){
    event.preventDefault();

    const relation = $('#relation');
    const city = $('#city');
    const business_unit = $('#business-unit');
    const location = $('#location');
    const date_time = $('#date-time');
    const implicated = $('#implicated');
    const classification = $('#classification');
    const description = $('#description');
    const fileFields = $('#files-container input[type="file"]');
    const emailFields = $('#emails-container input[type="email"]');
    const phoneContainer = $('#phones-container .d-flex');
    const source = $('#source');
    const name = $('#name');
    const status = $('#status');

    let files = []; // Array para almacenar los archivos
    let emails = []; // Array para almacenar los correos
    let phoneTypes = []; // Array para almacenar los teléfonos
    let phoneNumbers = []; // Array para almacenar los números de teléfono

    let invalidEmails = false; // Bandera para verificar si hay correos inválidos
    let invalidInputs = false; // Bandera para verificar si hay inputs vacíos
    let invalidPhones = false; // Bandera para verificar si hay teléfonos inválidos
    let invalidFiles = false; // Bandera para verificar si hay archivos inválidos

    const validFileExtensions = ['jpg', 'jpeg', 'png', 'pdf']; // Extensiones de archivo permitidas

    function showFeedbackEmptyFields(fields){
        
        fields.forEach(function(field) {
            if($(field).val() === '') {
                $(field).addClass('is-invalid');
                invalidInputs = true;
            } else {
                $(field).removeClass('is-invalid'); // Opcional: remover la clase si no está vacío
            }
        });

    }

    showFeedbackEmptyFields([relation, city, business_unit, location, date_time, implicated, classification, description, source]);

    // Iterar sobre todos los inputs de tipo file en el contenedor
    if(fileFields.length>1){

        fileFields.each(function(index, element) {
            
            const fileValue = $(element).val();
            const fileExtension = fileValue.split('.').pop().toLowerCase();

            if (fileValue === '' || !validFileExtensions.includes(fileExtension)) {
                $(element).addClass('is-invalid');
                invalidInputs = true;
                invalidFiles = true;
            } else {
                $(element).removeClass('is-invalid');
                files.push(element.files[0]);
            }

        });

    }else{

        fileFields.each(function(index, element) {
            const fileName = $(element).val();
            const fileValues = fileName.split('.');
            const fileExtension = fileValues[fileValues.length-1];

            if (!validFileExtensions.includes(fileExtension) && fileName!=='') {
                $(element).addClass('is-invalid');
                invalidInputs = true;
                invalidFiles = true;
            } else {
                $(element).removeClass('is-invalid');
                files.push(element.files[0]);
            }
        });
    }

    if (invalidInputs || invalidFiles) {
        $('#file-container .invalid-feedback').show();
    }else{
        $('#file-container .invalid-feedback').hide();
    }

    if(emailFields.length>1){
        // Iterar sobre todos los inputs de tipo email en el contenedor
        emailFields.each(function(index, element) {

            // Obtener el valor del input de email
            let emailValue = $(element).val();

            // Agregar el valor al array si no está vacío y si tiene errores
            if (!emailPattern.test(emailValue) || emailValue === '') {
                invalidEmails = true;
                $(element).addClass('is-invalid');
            }else{
                $(element).removeClass('is-invalid');
                emails.push(emailValue);
            }

        });
    }else{
        emailFields.each(function(index, element) {

            const emailValue = $(element).val();

            if (!emailPattern.test(emailValue)  && $(element).val()!==''){
                invalidEmails = true;
                $(element).addClass('is-invalid');
            }else{
                $(element).removeClass('is-invalid');
                emails.push(emailValue);
            }

        });
    }

    if(invalidEmails){
        $('#email-container .invalid-feedback').show();
    }else{
        $('#email-container .invalid-feedback').hide();
    }

    if(phoneContainer.length>1){

        phoneContainer.each(function(index, element) {

            // Obtener el valor del input de phone
            const phoneType = $(element).find('select[name="phone_type"]').val(); // Obtener el tipo de teléfono seleccionado
            const phoneNumber = $(element).find('input[name="phone"]').val(); // Obtener el número de teléfono

            // Agregar el valor cl array si no está vacío y si tiene errores
            if (!phonePattern.test(phoneNumber) || phoneNumber === '') {
                invalidPhones = true;
                $(element).addClass('is-invalid');
            }else{
                $(element).removeClass('is-invalid');
                phoneTypes.push(phoneType);
                phoneNumbers.push(phoneNumber);
            }
    
        });

    }else{

        phoneContainer.each(function(index, element) {

            const phoneType = $(element).find('select[name="phone_type"]').val();
            const phoneNumber = $(element).find('input[name="phone"]').val();

            if (!phonePattern.test(phoneNumber) && phoneNumber!=='') {
                invalidPhones = true;
                $(element).addClass('is-invalid');
            }else{
                $(element).removeClass('is-invalid');
                phoneTypes.push(phoneType);
                phoneNumbers.push(phoneNumber);
            }

        });
    }

    if(invalidPhones){
        $('#phone-container .invalid-feedback').show();
    }else{
        $('#phone-container .invalid-feedback').hide();
    }

    const formData = new FormData();

    if(files[0]!==undefined){
        files.forEach((file, index) => {
            formData.append('files', file); 
        });
    }

    if(emails[0]!==''){
        emails.forEach((email, index) => {
            formData.append('emails', email); 
        });
    }

    phoneNumbers.forEach((phoneNumber, index) => {
        formData.append('phone_numbers', phoneNumber); 
    });

    if (phoneNumbers[0]!==''){
        phoneTypes.forEach((phoneType, index) => {
            formData.append('phone_types', phoneType); 
        });
    }

    formData.append('relation', relation.val());
    formData.append('city', city.val());
    formData.append('business_unit', business_unit.val());
    formData.append('place', location.val());
    formData.append('date_time', date_time.val());
    formData.append('names_involved', implicated.val());
    formData.append('report_classification', classification.val());
    formData.append('detailed_description', description.val());
    formData.append('name', name.val());
    formData.append('communication_channel', source.val());
    formData.append('status', status.val());

    if(!invalidEmails && !invalidInputs && !invalidPhones && !invalidFiles){

        const code = $('#complaint-information label').attr('id');

        const response = await fetch(`${base_url}/complaint/update_complaint/${code}/`, {
            method: 'PUT',
            mode: 'same-origin',
            headers: {
              'X-CSRFToken': csrftoken
            },
            body: formData
        }).then(response => {
            if (response.status===201) {
                return response.json();
            }
        }).then(data=>{
            console.log(data);
        });

    }

});

$('#add-file').on('click', function(event){

    let inputs = $('#files-container input[type="file"]');

    emptyFields = false;

    // Iterar sobre cada input para realizar las validaciones
    inputs.each(function(index, element) {

        // Validar si el input está vacío
        if ($(element).val() === '') {
            emptyFields = true;
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }

    });

    if(emptyFields){
        $('#modal h1').text('No puedes agregar archivos');
        $('#modal p').text('Para agregar más archivos primero debes de llenar el registro.');
        $('#modal').modal('show');
    }else{
        $('#files-container').append(`
        <div class="mb-2 d-flex align-items-start" id="file-container-${fileId}">
            <input type="file" class="form-control rounded-0" name="files">
            <button type="button" class="btn btn-secondary px-2 rounded-0 remove-element" onclick="removeFile('file-container-${fileId++}')">x</button>
        </div>`);
    }

    filesQuantity++;

});

$('#add-email').on('click', function(event){

    let inputs = $('#emails-container input[type="email"]');

    emptyFields = false;
    invalidEmails= false;

    // Iterar sobre cada input para realizar las validaciones
    inputs.each(function(index, element) {

        let emailValue = $(this).val();

        // Validar si el input está vacío
        if ($(element).val() === '') {
            emptyFields = true;
        } else {
            console.log(`El archivo en el campo ${index + 1} está seleccionado.`);
        }

        if (!emailPattern.test(emailValue)) {
            $(this).addClass('is-invalid'); // Marcar como inválido si no cumple con la expresión
            invalidEmails= true;
        } else {
            $(this).removeClass('is-invalid'); // Remover la marca de inválido si es correcto
        }

    });

    if(emptyFields){
        $('#modal h1').text('No puedes agregar correos');
        $('#modal p').text('Para agregar más correos primero debes de llenar el registro.');
        $('#modal').modal('show');
    }else if(invalidEmails){
        $('#modal h1').text('Correo inválido');
        $('#modal p').text('Por favor, revisa los correos que ingresaste.');
        $('#modal').modal('show');
    }else{
        $('#emails-container').append(`
        <div class="mb-2 d-flex align-items-start" id="email-container-${emailId}">
            <input type="email" id="email" class="form-control rounded-0" placeholder="Correo" name="email">
            <button type="button" class="btn btn-secondary px-2 rounded-0 remove-element" onclick="removeEmail('email-container-${emailId++}')">x</button>
        </div>`);
    }

    emailsQuantity++;

});

$('#add-phone').on('click', function(event){

    let inputs = $('#phones-container input[type="tel"]');
    let emptyFields = false;
    let invalidPhones = false;

    inputs.each(function(index, element) {

        let phoneValue = $(element).val();

        // Validar si el input está vacío
        if (phoneValue === '') {
            $(element).addClass('is-invalid'); // Marca el campo como inválido
            emptyFields = true;
        } else {
            $(element).removeClass('is-invalid'); // Limpia la clase si es válido
        }

        // Validar si el campo coincide con el patrón
        if (!phonePattern.test(phoneValue)) {
            invalidPhones = true;
            $(element).addClass('is-invalid');
        } else {
            $(element).removeClass('is-invalid');
        }

    });

    if(emptyFields){
        $('#modal h1').text('No puedes agregar teléfonos');
        $('#modal p').text('Para agregar más teléfonos primero debes de llenar el registro.');
        $('#modal').modal('show');
    }else if(invalidPhones){
        $('#modal h1').text('Teléfono inválido');
        $('#modal p').text('Por favor, revisa los teléfonos que ingresaste.');
        $('#modal').modal('show');
    }else{
        $('#phones-container').append(`
            <div class="d-flex my-2" id="phone-container-${phoneId}">
                <select id="phone_type" class="form-select me-2 rounded-0" name="phone_type">
                    <option value="Celular">Celular</option>
                    <option value="Casa">Casa</option>
                    <option value="Oficina">Oficina</option>
                    <option value="Otro">Otro</option>
                </select>
                <input type="tel" id="phone" class="form-control rounded-0" placeholder="Teléfono" name="phone" pattern="^[0-9]{10}$" minlength="10" maxlength="10">
                <button type="button" class="btn btn-secondary px-2 rounded-0 remove-element" onclick="removePhone('phone-container-${phoneId++}')">x</button>
            </div>`);
    }
    phonesQuantity++;
});

$('#btn-comments').on('click', async function(event){

    const code = $('#complaint-information label').attr('id');
    $('#offcanvasComplaintComments .offcanvas-body .loader-wrapper').show();

    const response = await fetch(`${base_url}/complaint/comments/${code}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    $('#offcanvasComplaintComments .offcanvas-body .complaint-comment-list').empty();
    $('#offcanvasComplaintComments .offcanvas-body .loader-wrapper').hide();

    if(response['comments'].length === 0){
        $('#offcanvasComplaintComments .offcanvas-body .complaint-comment-list').append(`<h6 class="text-center mb-0">No hay comentarios</h6>`);
    }else{
        response['comments'].forEach(comment => {
            $('#offcanvasComplaintComments .offcanvas-body .complaint-comment-list').append(`
                <div class="card column mb-3 rounded-0">
                  <div class="card-header bg-danger text-white rounded-0">
                    <h6 class="mb-0">Fecha: ${comment['date']}</h6>
                  </div>
                  <div class="card-body">
                    ${comment['comment']}
                  </div>
                  <div class="card-footer">
                    Escrito por: <i>${comment['user']}</i>
                  </div>
                </div>`);
            });
    }

});

$('#btn-logs').on('click', async function(event){

    const code = $('#complaint-information label').attr('id');
    $('#offcanvasComplaintLogs .offcanvas-body .loader-wrapper').show();

    const response = await fetch(`${base_url}/complaint/logs/${code}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    $('#offcanvasComplaintLogs .offcanvas-body .complaint-log-list').empty();
    $('#offcanvasComplaintLogs .offcanvas-body .loader-wrapper').hide();

    if(response['logs'].length === 0){
        $('#offcanvasComplaintLogs .offcanvas-body .complaint-log-list').append(`<h6 class="text-center mb-0">No hay comentarios</h6>`);
    }else{
        response['logs'].forEach(log => {
            $('#offcanvasComplaintLogs .offcanvas-body .complaint-log-list').append(`
                <div class="card column mb-3 rounded-0">
                  <div class="card-header bg-warning text-white rounded-0">
                    <h6 class="mb-0">Fecha: ${log['date']}</h6>
                  </div>
                  <div class="card-body">
                    <p class="">${log['movement']}</p>
                  </div>
                </div>`);
            });
    }

});

$('#btn-send-comment').on('click', async function(event){

    const code = $('#complaint-information label').attr('id');
    const comment = $('#comment-text-area').val();

    const response = await fetch(`${base_url}/complaint/comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: new URLSearchParams({
            code,
            comment
        })
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    $('#offcanvasComplaintNewComment .btn-close').click();
    $('#btn-comments').click();

});


// ---------------Functions----------------

function removeFile(id){
    $(`#${id}`).remove();
    filesQuantity--;
}

function removeEmail(id){
    $(`#${id}`).remove();
    emailsQuantity--;
}

function removePhone(id){
    $(`#${id}`).remove();
    phonesQuantity--;
}

async function complaintDetail(id){

    $('#old-files-container ul').empty();
    $('#old-emails-container ul').empty();
    $('#old-phones-container ul').empty();
    $('#assigned-user').empty();
    $('#assigned-user').append(`<option value="">Selecciona un usuario</option>`);

    const complaintResponse = await fetch(`${base_url}/complaint/${id}/`, {
    }).then(response => {
        return response.json()
    }).then(data => {
        return data;
    });

    const usersResponse = await fetch(`${base_url}/users/staff/users/`, {
    }).then(response => {
        return response.json()
    }).then(data => {
        return data;
    });

    const complaint = complaintResponse['complaint'];
    const files = complaintResponse['files'];
    const emails = complaintResponse['emails'];
    const phones = complaintResponse['phones'];
    const users = usersResponse['users'];

    $('#modalComplaint .modal-body .container').show();
    $('#modalComplaint .modal-body .loader-wrapper').hide();

    $('#modalComplaint .modal-body #complaint-information').html(`<label id=${complaint['id']}>${complaint['id']}</label>`);
    $('#modalComplaint .modal-body #complaint-information label').attr('id', complaint['id']);

    $('#modalComplaint .modal-body #business-unit').val(complaint['business_unit']);
    $('#modalComplaint .modal-body #location').val(complaint['place']);
    $('#modalComplaint .modal-body #date-time').val(complaint['date_time']);
    $('#modalComplaint .modal-body #close_date').val(complaint['close_date']);
    $('#modalComplaint .modal-body #implicated').val(complaint['names_involved']);
    $('#modalComplaint .modal-body #description').val(complaint['detailed_description']);
    $('#modalComplaint .modal-body #name').val(complaint['name']);
    $('#modalComplaint .modal-body #classification').val(complaint['classification']);
    $('#modalComplaint .modal-body #relation').val(complaint['relation']);
    $('#modalComplaint .modal-body #city').val(complaint['city']);
    $('#modalComplaint .modal-body #channel').val(complaint['channel']);
    $('#modalComplaint .modal-body #priority').val(complaint['priority']);
    $('#modalComplaint .modal-body #status').val(complaint['status']);
    $('#modalComplaint .modal-body #enterprise').val(complaint['enterprise']);
    $('#modalComplaint .modal-body #source').val(complaint['channel']);
    $('#modalComplaint .modal-body #complaint-created-at').html(`<label>Fecha recibida: ${complaint['created_at']}</label>`);

    files.forEach(file => {
        $('#old-files-container ul').append(`
            <li>
            <div class="mb-2 d-flex align-items-start" id="old-file-container-${fileId}">
                <a href="${file['file_url']}" target="_blank" class="me-2" style="text-decoration: underline;">${file['file_name']}</a>
            </div>
            </li>`);
    });

    emails.forEach(email => {
        $('#old-emails-container ul').append(`
            <li>
            <div class="mb-2 d-flex align-items-start" id="old-email-container-${emailId}">
                <label class="me-2" style="text-decoration: underline;">${email['email']}</label>
            </div>
            </li>`);
    });

    phones.forEach(phone => {
        $('#old-phones-container ul').append(`
            <li>
            <div class="d-flex my-2" id="old-phone-container-${phoneId}">
                <label class="me-2" style="text-decoration: underline;">${phone['phone_type']}</label>
                <label class="me-2" style="text-decoration: underline;">${phone['phone_number']}</label>
            </div>
            </li>`);
    });

    users.forEach(user => {
        $('#assigned-user').append(`
            <option value="${user['id']}">${user['username']}</option>
        `);
    });

    if(complaint['assigned_user']!==''){
        $('#assigned-user').val(complaint['assigned_user']['id']);
    }

}
