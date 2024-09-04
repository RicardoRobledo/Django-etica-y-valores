let fileId = 0;
let filesQuantity = 0; 

let emailId = 0;
let emailsQuantity = 0; 

let phoneId = 0;
let phonesQuantity = 0;

let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$/;
let phonePattern = /^[0-9]{10}$/;

const base_url = 'https://django-etica-y-valores.onrender.com';
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


$(document).ready(function() {
    $('body').css('display', 'none');
    $('body').fadeIn(1000);
});


// -------------------Events------------------

$('#search-complaint').on('click', async function(event){

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
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

$('#send-complaint').on('click', async function(event){
    event.preventDefault();
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const relation = $('#relation');
    const city = $('#city');
    const business_unit = $('#business-unit');
    const location = $('#location');
    const date = $('#date');
    const time = $('#time');
    const implicated = $('#implicated');
    const classification = $('#classification');
    const description = $('#description');
    const fileFields = $('#files-container input[type="file"]');
    const emailFields = $('#emails-container input[type="email"]');
    const phoneContainer = $('#phones-container .d-flex');
    const source = $('#source');
    const name = $('#name');

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

    showFeedbackEmptyFields([relation, city, business_unit, location, date, time, implicated, classification, description, source]);

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
            $(element).removeClass('is-invalid');

            if ($(element).val()!==''){
                emails.push($(element).val());
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
            console.log(file);
            formData.append('files', file); 
        });
    }

    if(emails.length!==0){
        emails.forEach((email, index) => {
            formData.append('emails', email); 
        });
    }else{
        formData.append('emails', '');
    }

    phoneNumbers.forEach((phoneNumber, index) => {
        formData.append('phone_numbers', phoneNumber); 
    });

    if (phoneNumbers[0]!==''){
        phoneTypes.forEach((phoneType, index) => {
            formData.append('phone_types', phoneType); 
        });
    }else{
        formData.append('phone_types', ''); 
    }

    formData.append('enterprise_relation', relation.val());
    formData.append('city', city.val());
    formData.append('business_unit', business_unit.val());
    formData.append('place', location.val());
    formData.append('date', date.val());
    formData.append('time', time.val());
    formData.append('names_involved', implicated.val());
    formData.append('report_classification', classification.val());
    formData.append('detailed_description', description.val());
    formData.append('name', name.val());
    formData.append('communication_channel', source.val());

    if(!invalidEmails && !invalidInputs && !invalidPhones && !invalidFiles){

        const response = await fetch(base_url+'/complaint/', {
            method: 'POST',
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
            window.location.href = data['url'];
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
        $('#modal p').text('Para agregar más archivos primero de llenar el registro.');
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
        $('#modal p').text('Para agregar más correos primero de llenar el registro.');
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
        $('#modal p').text('Para agregar más teléfonos primero de llenar el registro.');
        $('#modal').modal('show');
    }else if(invalidPhones){
        $('#modal h1').text('Teléfono inválido');
        $('#modal p').text('Por favor, revisa los teléfonos que ingresaste.');
        $('#modal').modal('show');
    }else{
        $('#phones-container').append(`
            <div class="d-flex my-2" id="phone-container-${phoneId}">
                <select id="phone_type" class="form-select me-2 rounded-0" name="phone_type">
                    <option value="celular">Celular</option>
                    <option value="casa">Casa</option>
                    <option value="oficina">Oficina</option>
                    <option value="otro">Otro</option>
                </select>
                <input type="tel" id="phone" class="form-control rounded-0" placeholder="Teléfono" name="phone" pattern="^[0-9]{10}$" minlength="10" maxlength="10">
                <button type="button" class="btn btn-secondary px-2 rounded-0 remove-element" onclick="removePhone('phone-container-${phoneId++}')">x</button>
            </div>`);
    }
    phonesQuantity++;
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