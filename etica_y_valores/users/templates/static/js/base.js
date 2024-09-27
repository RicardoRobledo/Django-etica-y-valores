//const url = 'https://django-etica-y-valores.onrender.com';
//const url = 'http://127.0.0.1:8000';


$('#menu-button').on('click', async function () {

    $('.loader-wrapper').show();
    $('.list-container').hide();

    const response = await fetch(`${url}/complaint/count/`, {
        method: 'GET',
    }).then(async (response) => {
        return response.json();
    }).then(async (data) => {
        return data;
    });

    sideBarListContainer = `<ul class="list-unstyled ps-0">
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text"></i>
                            Denuncias abiertas (<strong class="text-info" id="complaints-opened-count">{{all_complaints_opened_count}}</strong>)
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text"></i>
                            Denuncias finalizadas (<strong class="text-info" id="complaints-closed-count">{{all_complaints_closed_count}}</strong>)
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text"></i>
                            Denuncias en tabla
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text"></i>
                            Estatus vs Clasificación de denuncia abiertas
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text"></i>
                            Prioridad vs Estatus abiertas
                        </a>
                      </li>

                      <li class="border-top my-3"></li>

                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#estatusMenu" role="button" aria-expanded="false" aria-controls="estatusMenu">
                            <i class="bi bi-folder"></i>
                            Estatus (abiertas)
                        </a>
                        <div class="collapse" id="estatusMenu">
                            <ul class="nav flex-column ms-3" id="status-list">
                                {{all_complaints_by_status}}
                            </ul>
                        </div>
                    </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#ciudadMenu" role="button" aria-expanded="false" aria-controls="ciudadMenu">
                            <i class="bi bi-folder"></i>
                            Ciudad en la que ocurrieron los hechos (abiertas)
                        </a>
                        <div class="collapse" id="ciudadMenu">
                            <ul class="nav flex-column ms-3" id="city-list">
                                {{all_complaints_by_city}}
                            </ul>
                        </div>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#prioridadMenu" role="button" aria-expanded="false" aria-controls="prioridadMenu">
                            <i class="bi bi-folder"></i>
                            Prioridad de la denuncia (abiertas)
                        </a>
                        <div class="collapse" id="prioridadMenu">
                            <ul class="nav flex-column ms-3" id="priority-list">
                                {{all_complaints_by_priority}}
                            </ul>
                        </div>
                    </li>
                    <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#clasificacionMenu" role="button" aria-expanded="false" aria-controls="clasificacionMenu">
                            <i class="bi bi-folder"></i>
                            Clasificación del reporte (abiertas)
                        </a>
                        <div class="collapse" id="clasificacionMenu">
                            <ul class="nav flex-column ms-3" id="classification-list">
                                {{all_complaints_by_classification}}
                            </ul>
                        </div>
                    </li>
                    <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#canalMenu" role="button" aria-expanded="false" aria-controls="canalMenu">
                            <i class="bi bi-folder"></i>
                            Por qué canal te enteraste (abiertas)
                        </a>
                        <div class="collapse" id="canalMenu">
                            <ul class="nav flex-column ms-3" id="channel-list">
                                {{all_complaints_by_channel}}
                            </ul>
                        </div>
                    </li>
                    </ul>`;

    const all_complaints_opened_count = response['all_complaints_opened_count'];
    const all_complaints_closed_count = response['all_complaints_closed_count'];
    let all_complaints_by_status = '';
    let all_complaints_by_city = '';
    let all_complaints_by_priority = '';
    let all_complaints_by_classification = '';
    let all_complaints_by_channel = '';

    for(const element of response['all_complaints_by_status']){
        all_complaints_by_status+=`<li class="nav-item">
                                    <a class="nav-link">${element.status} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of response['all_complaints_by_city']){
        all_complaints_by_city+=`<li class="nav-item">
                                    <a class="nav-link">${element.city} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of response['all_complaints_by_priority']){
        all_complaints_by_priority+=`<li class="nav-item">
                                    <a class="nav-link">${element.priority} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of response['all_complaints_by_classification']){
        all_complaints_by_classification+=`<li class="nav-item">
                                    <a class="nav-link">${element.classification} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of response['all_complaints_by_channel']){
        all_complaints_by_channel+=`<li class="nav-item">
                                    <a class="nav-link">${element.channel} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    sideBarListContainer = sideBarListContainer.replace(
        '{{all_complaints_opened_count}}', all_complaints_opened_count
    ).replace(
        '{{all_complaints_closed_count}}', all_complaints_closed_count
    ).replace(
        '{{all_complaints_by_status}}', all_complaints_by_status
    ).replace(
        '{{all_complaints_by_city}}', all_complaints_by_city
    ).replace(
        '{{all_complaints_by_priority}}', all_complaints_by_priority
    ).replace(
        '{{all_complaints_by_classification}}', all_complaints_by_classification
    ).replace(
        '{{all_complaints_by_channel}}', all_complaints_by_channel
    );

    $('.list-container').html(sideBarListContainer);

    $('.loader-wrapper').hide();
    $('.list-container').show();

});