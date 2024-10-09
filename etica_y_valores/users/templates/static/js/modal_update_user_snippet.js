$(document).ready(async function () {

    // Function to move selected items from available to selected
    $('#editMoveToSelected').click(function () {
        $('#editAvailableGroups option:selected:visible').each(function () {
            $(this).remove().appendTo('#editSelectedGroups');
        });
    });

    // Function to move selected items from selected to available
    $('#editMoveToAvailable').click(function () {
        $('#editSelectedGroups option:selected:visible').each(function () {
            $(this).remove().appendTo('#editAvailableGroups');
        });
    });

    // Select all items in availableGroups
    $('#editSelectAll').click(function () {
        if ($('#editAvailableGroups option:visible').length > 0) {
            $('#editAvailableGroups option:visible').prop('selected', true).appendTo('#editSelectedGroups');
            filterGroups(); // Update filters after selecting all
        }
    });

    // Remove all items from selectedGroups
    $('#editRemoveAll').click(function () {
        if ($('#editSelectedGroups option:visible').length > 0) {
            $('#editSelectedGroups option:visible').prop('selected', true).appendTo('#editAvailableGroups');
            filterGroups(); // Update filters after removing all
        }
    });

    // Filter for available groups
    $('#editFilterAvailable').on('input', function () {
        filterGroups();
    });

    // Filter for selected groups
    $('#editFilterSelected').on('input', function () {
        filterGroups();
    });

    // Function to filter available and selected groups
    function filterGroups() {
        var filterAvailable = $('#editFilterAvailable').val().toLowerCase();
        var filterSelected = $('#editFilterSelected').val().toLowerCase();

        $('#editAvailableGroups option').each(function () {
            if ($(this).text().toLowerCase().includes(filterAvailable)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });

        $('#editSelectedGroups option').each(function () {
            if ($(this).text().toLowerCase().includes(filterSelected)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});

function enablePermissions(){
    $('#editAvailableGroups').prop('disabled', false);
    $('#editSelectedGroups').prop('disabled', false);
    $('#editMoveToSelected').prop('disabled', false);
    $('#editMoveToAvailable').prop('disabled', false);
    $('#editSelectAll').prop('disabled', false);
    $('#editRemoveAll').prop('disabled', false);
    $('#editFilterAvailable').prop('disabled', false);
    $('#editFilterSelected').prop('disabled', false);
}

function disablePermissions(){

    $('#editAvailableGroups').prop('disabled', true);
    $('#editSelectedGroups').prop('disabled', true);
    $('#editMoveToSelected').prop('disabled', true);
    $('#editMoveToAvailable').prop('disabled', true);
    $('#editSelectAll').prop('disabled', true);
    $('#editRemoveAll').prop('disabled', true);
    $('#editFilterAvailable').prop('disabled', true);
    $('#editFilterSelected').prop('disabled', true);

    $('#editRemoveAll').click();

}

$('#edit-user-level').on('change', function () {
    let userLevel = $(this).val();

    if (userLevel === "Operador") {
        $('#edit-supervisor').prop('disabled', false);
        enablePermissions();
    } else {
        $('#edit-supervisor').prop('disabled', true);
        $('#edit-supervisor').val('');
        disablePermissions();
    }
});

async function editUser(id) {

    $('#edit-supervisor').prop('disabled', true);
    $('#editAvailableGroups').html(`
    <option id="Comentarios" value="Comentarios">Comentarios</option>
    <option id="Alta" value="Alta">Alta</option>
    <option id="Baja" value="Baja">Baja</option>
    <option id="Guadalajara" value="Guadalajara">Guadalajara</option>
    <option id="León" value="León">León</option>
    <option id="Media" value="Media">Media</option>
    <option id="Otro" value="Otro">Otro</option>
    <option id="Playa del Carmen" value="Playa del Carmen">Playa del Carmen</option>
    <option id="Querétaro" value="Querétaro">Querétaro</option>
    <option id="Usuarios" value="Usuarios">Usuarios</option>
    <option id="Veracruz" value="Veracruz">Veracruz</option>
    `);
    $('#editSelectedGroups').empty();
    disablePermissions();

    const responseSupervisors = await fetch(`${url}/users/staff/users/supervisors/`, {
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

    const responseUserInfo = await fetch(`${url}/users/staff/users/user-info/${id}/`, {
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

    $('#edit-supervisor').html('<option value="">Selecciona una opción</option>');

    responseSupervisors['supervisors'].forEach(supervisor => {
        $('#edit-supervisor').append(`<option value="${supervisor['id']}">${supervisor['first_name']} ${supervisor['middle_name']} ${supervisor['last_name']}</option>`);
    });

    let user = responseUserInfo['user'];
    
    $('#edit-username').val(user['username']);
    $('#edit-name').val(user['first_name']);
    $('#edit-middle-name').val(user['middle_name']);
    $('#edit-last-name').val(user['last_name']);
    $('#edit-email').val(user['email']);
    $('#edit-user-level').val(user['user_level']);

    if (user['user_level'] === 'Operador') {
        $('#edit-supervisor').prop('disabled', false);
        enablePermissions();
    }
    $('#edit-supervisor').val(user['supervisor']);

    user['permissions'].forEach(permission => {
        $(`#editAvailableGroups option[value="${permission}"]`).remove();
        $('#editSelectedGroups').append(`<option id="${permission}" value="${permission}">${permission}</option>`);
    });

    $('#modalUpdateUser .modal-body #user-id').html(`<label id=${user['id']}>ID: ${user['id']}</label>`);

}

$('#update-user-button').click(async function (event) {
    let isValid = true;

    // Expresión regular que permite solo letras sin espacios (para nombre de usuario y nombre)
    let onlyLetters = /^[a-zA-Z]+$/;
    
    // Expresión regular que permite solo letras y espacios (para apellidos)
    let lettersAndSpaces = /^[a-zA-Z]+(?:\s[a-zA-Z]+)*$/;

    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$/;

    let id = $('#user-id label').attr('id');

    // Validar Nombre
    let name = $('#edit-name');
    if (!onlyLetters.test(name.val())) {
        name.addClass('is-invalid');
        isValid = false;
    } else {
        name.removeClass('is-invalid');
    }

    // Validar Primer apellido (permite letras y espacios)
    let middleName = $('#edit-middle-name');
    if (!lettersAndSpaces.test(middleName.val())) {
        middleName.addClass('is-invalid');
        isValid = false;
    } else {
        middleName.removeClass('is-invalid');
    }

    // Validar Segundo apellido (permite letras y espacios)
    let lastName = $('#edit-last-name');
    if (!lettersAndSpaces.test(lastName.val())) {
        lastName.addClass('is-invalid');
        isValid = false;
    } else {
        lastName.removeClass('is-invalid');
    }

    let username = $('#edit-username');
    if (username.val() === '') {
        username.addClass('is-invalid');
        isValid = false;
    }else{
        username.removeClass('is-invalid');
    }

    let email = $('#edit-email');
    let emailValue = email.val();

    if (!emailPattern.test(emailValue) || emailValue===''){
        isValid = false;
        email.addClass('is-invalid');
    }else{
        email.removeClass('is-invalid');
    }

    let userLevel = $('#edit-user-level');
    let supervisor = $('#edit-supervisor');
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

    let selectedGroups = $('#editSelectedGroups option').map(function() {
        return $(this).val();
    }).get();

    const formData = new FormData();

    formData.append('username', username.val());
    formData.append('name', name.val());
    formData.append('middle-name', middleName.val());
    formData.append('last-name', lastName.val());
    formData.append('user-level', userLevel.val());
    formData.append('supervisor', supervisor.val());
    formData.append('email', emailValue);

    selectedGroups.forEach(function(permission) {
        formData.append('permissions', permission);  // Aquí el [] indica que es un array
    });

    // Si el formulario no es válido, evitar el envío
    if (!isValid) {
        event.preventDefault();
        event.stopPropagation();
    }else{

        await fetch(`${url}/users/staff/users/update-user/${id}/`, {
            method: 'PUT',
            headers: {
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
