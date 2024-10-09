const url = 'https://django-etica-y-valores.onrender.com';
//const url = 'http://127.0.0.1:8000';

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


$(document).ready(function () {

    $('#login-form').submit(function (event) {
        event.preventDefault();
        login();
    });

    function login() {
        const username = $('#username').val();
        const password = $('#password').val();

        fetch(`${url}/users/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                username,
                password
            })
        }).then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                $('#message').show().delay(3000).fadeOut();
            }
        }).then(data => {
            console.log('Success:', data);
            window.location.href = data['redirect_url'];
        }).catch(error => {
            console.error('Error:', error);
        });
    }

});