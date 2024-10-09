function editUserPassword(id){
    $('#update-user-password-button').attr('onclick', 'updateUserPassword("'+id+'")');
    $('#edit-password').val('');
    $('#edit-confirm-password').val('');
};

async function updateUserPassword(id) {

    let isValid = true;

    let passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

    let password = $('#edit-password');
    let confirmPassword = $('#edit-confirm-password');

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

    if(isValid){

        let response = await fetch(`${url}/users/staff/users/user-password/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({password:password.val()})
        }).then(response => {
            return response.json()
        }).then(data=>data);

        $('#update-user-password-close-button').click();

    }

}
