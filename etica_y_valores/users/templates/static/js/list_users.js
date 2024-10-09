const base_url = 'http://127.0.0.1:8000';

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


async function changeActiveState(id){

    const status = $(`#checkbox-user-state-${id}`).prop('checked');

    const response = await fetch(`${base_url}/users/staff/users/user-status/${id}/`, {
        method: 'PUT',
        mode: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({status})
    }).then(response => {
        if (response.status===201) {
            return response.json();
        }
    }).then(data=>{
        console.log(data);
    });

}