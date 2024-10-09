$(document).ready(async function () {

    $('#supervisor').prop('disabled', true);
    disablePermissions();

    const response = await fetch(`${url}/users/staff/users/supervisors/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            $('#message').show().delay(3000).fadeOut();
        }
    }).then(data=>{
        return data;
    });

    $('#supervisor').html('<option value="">Selecciona una opción</option>');

    response['supervisors'].forEach(supervisor => {
        $('#supervisor').append(`<option value="${supervisor['id']}">${supervisor['first_name']} ${supervisor['middle_name']} ${supervisor['last_name']}</option>`);
    });

    // Function to move selected items from available to selected
    $('#moveToSelected').click(function () {
        $('#availableGroups option:selected:visible').each(function () {
            $(this).remove().appendTo('#selectedGroups');
        });
    });

    // Function to move selected items from selected to available
    $('#moveToAvailable').click(function () {
        $('#selectedGroups option:selected:visible').each(function () {
            $(this).remove().appendTo('#availableGroups');
        });
    });

    // Select all items in availableGroups
    $('#selectAll').click(function () {
        if ($('#availableGroups option:visible').length > 0) {
            $('#availableGroups option:visible').prop('selected', true).appendTo('#selectedGroups');
            filterGroups(); // Update filters after selecting all
        }
    });

    // Remove all items from selectedGroups
    $('#removeAll').click(function () {
        if ($('#selectedGroups option:visible').length > 0) {
            $('#selectedGroups option:visible').prop('selected', true).appendTo('#availableGroups');
            filterGroups(); // Update filters after removing all
        }
    });

    // Filter for available groups
    $('#filterAvailable').on('input', function () {
        filterGroups();
    });

    // Filter for selected groups
    $('#filterSelected').on('input', function () {
        filterGroups();
    });

    // Function to filter available and selected groups
    function filterGroups() {
        var filterAvailable = $('#filterAvailable').val().toLowerCase();
        var filterSelected = $('#filterSelected').val().toLowerCase();

        $('#availableGroups option').each(function () {
            if ($(this).text().toLowerCase().includes(filterAvailable)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });

        $('#selectedGroups option').each(function () {
            if ($(this).text().toLowerCase().includes(filterSelected)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});

function enablePermissions(){
    $('#availableGroups').prop('disabled', false);
    $('#selectedGroups').prop('disabled', false);
    $('#moveToSelected').prop('disabled', false);
    $('#moveToAvailable').prop('disabled', false);
    $('#selectAll').prop('disabled', false);
    $('#removeAll').prop('disabled', false);
    $('#filterAvailable').prop('disabled', false);
    $('#filterSelected').prop('disabled', false);
}

function disablePermissions(){

    $('#availableGroups').prop('disabled', true);
    $('#selectedGroups').prop('disabled', true);
    $('#moveToSelected').prop('disabled', true);
    $('#moveToAvailable').prop('disabled', true);
    $('#selectAll').prop('disabled', true);
    $('#removeAll').prop('disabled', true);
    $('#filterAvailable').prop('disabled', true);
    $('#filterSelected').prop('disabled', true);

    $('#removeAll').click();

}

$('#user-level').on('change', function () {
    let userLevel = $(this).val();

    if (userLevel === "Operador") {
        $('#supervisor').prop('disabled', false);
        enablePermissions();
    } else {
        $('#supervisor').prop('disabled', true);
        $('#supervisor').val('');
        disablePermissions();
    }
});

$('#create-user-button').click(async function (event) {
    let isValid = true;

    // Expresión regular que permite solo letras sin espacios (para nombre de usuario y nombre)
    let onlyLetters = /^[a-zA-Z]+$/;
    
    // Expresión regular que permite solo letras y espacios (para apellidos)
    let lettersAndSpaces = /^[a-zA-Z]+(?:\s[a-zA-Z]+)*$/;

    let passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$/;

    // Validar Nombre
    let name = $('#name');
    if (!onlyLetters.test(name.val())) {
        name.addClass('is-invalid');
        isValid = false;
    } else {
        name.removeClass('is-invalid');
    }

    // Validar Primer apellido (permite letras y espacios)
    let middleName = $('#middle-name');
    if (!lettersAndSpaces.test(middleName.val())) {
        middleName.addClass('is-invalid');
        isValid = false;
    } else {
        middleName.removeClass('is-invalid');
    }

    // Validar Segundo apellido (permite letras y espacios)
    let lastName = $('#last-name');
    if (!lettersAndSpaces.test(lastName.val())) {
        lastName.addClass('is-invalid');
        isValid = false;
    } else {
        lastName.removeClass('is-invalid');
    }

    let username = $('#add-username');
    if (username.val() === '') {
        username.addClass('is-invalid');
        isValid = false;
    }else{
        username.removeClass('is-invalid');
    }

    let password = $('#password');
    let confirmPassword = $('#add-confirm-password');

    if (password.val() === '' || confirmPassword.val() === '') {
        confirmPassword.addClass('is-invalid');
        password.addClass('is-invalid');
        isValid = false;
    }else{
        confirmPassword.removeClass('is-invalid');
        password.removeClass('is-invalid');
    }

    if (password.val() !== confirmPassword.val()) {
        isValid = false;
        confirmPassword.addClass('is-invalid');
        password.addClass('is-invalid');
    } else {
        confirmPassword.removeClass('is-invalid');
        password.removeClass('is-invalid');
    }

    if (!passwordRegex.test(password.val())) {
        password.addClass('is-invalid');
        isValid = false;
    } else {
        password.removeClass('is-invalid');
    }

    if (!passwordRegex.test(confirmPassword.val())) {
        confirmPassword.addClass('is-invalid');
        isValid = false;
    } else {
        confirmPassword.removeClass('is-invalid');
    }

    let email = $('#add-email');
    let emailValue = email.val();

    if (!emailPattern.test(emailValue) || emailValue===''){
        isValid = false;
        email.addClass('is-invalid');
    }else{
        email.removeClass('is-invalid');
    }

    let userLevel = $('#user-level');
    let supervisor = $('#supervisor');
    if (userLevel.val() === "") {
        userLevel.addClass('is-invalid');
        isValid = false;
    } else if (userLevel.val() === 'Operador') {
        if (supervisor.val() === "") {
            supervisor.addClass('is-invalid');
            isValid = false;
        } else {
            supervisor.removeClass('is-invalid');
        }
        userLevel.removeClass('is-invalid');
    } else {
        userLevel.removeClass('is-invalid');
    }

    let selectedGroups = $('#selectedGroups option').map(function() {
        return $(this).val();
    }).get();

    let formData = new URLSearchParams({
        'username': username.val(),
        'password': password.val(),
        'name': name.val(),
        'middle-name': middleName.val(),
        'last-name': lastName.val(),
        'user-level': userLevel.val(),
        'supervisor': supervisor.val(),
        'email': emailValue
    });

    selectedGroups.forEach(function(permission) {
        formData.append('permissions', permission);  // Aquí el [] indica que es un array
    });

    // Si el formulario no es válido, evitar el envío
    if (!isValid) {
        event.preventDefault();
        event.stopPropagation();
    }else{

        await fetch(`${url}/users/staff/users/user/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            body: formData
        }).then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                $('#message').show().delay(3000).fadeOut();
            }
        }).then(data => {
            console.log('Success');
        }).catch(error => {
            console.error('Error:', error);
        });

    }
});
