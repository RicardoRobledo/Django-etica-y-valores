const base_url = 'https://django-etica-y-valores.onrender.com';
//const base_url = 'http://127.0.0.1:8000';
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


$('#btn-comments').on('click', async function(event){

    const code = $('#code').text();

    const response = await fetch(`${base_url}/complaint/comments/${code}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    $('#offcanvas-body').html('');

    if(response['comments'].length === 0){
        $('#offcanvas-body').append(`<h6 class="text-center mb-0">No hay comentarios</h6>`);
    }else{
        response['comments'].forEach(comment => {
            $('#offcanvas-body').append(`
                <div class="card column mb-3 rounded-0">
                  <div class="card-header bg-primary text-white rounded-0">
                    <h6 class="mb-0">Fecha: ${comment['date']}</h6>
                  </div>
                  <div class="card-body">
                    <p class="text-white">${comment['comment']}</p>
                  </div>
                </div>`);
            });
    }

});
