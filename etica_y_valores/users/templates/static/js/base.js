const url = 'https://django-etica-y-valores.onrender.com';
//const url = 'http://127.0.0.1:8000';


async function getComplaintsByMenuOption(path, status){

    path = path.replace('placeholder', status);
    window.location.href=`${url}${path}`;

};


$('#menu-button').on('click', async function () {

    $('.loader-wrapper').show();
    $('.list-container').hide();
    
    const id = $('#user-id').text();

    const responseComplaintCount = await fetch(`${url}/complaint/count/`, {
        method: 'GET',
    }).then(async (response) => {
        return response.json();
    }).then(async (data) => {
        console.log(data)
        return data;
    });

    const responsePermissions = await fetch(`${url}/users/staff/users/user/${id}/`, {
        method: 'GET',
    }).then(async (response) => {
        return response.json();
    }).then(async (data) => {
        console.log(data)
        return data;
    });

    sideBarListContainer = `<ul class="list-unstyled ps-0">
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button" href="{{home_staff_path}}">
                            <i class="bi bi-file-earmark-text-fill"></i>
                            Denuncias abiertas (<strong class="text-info" id="complaints-opened-count">{{all_complaints_opened_count}}</strong>)
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button" href="{{table_complaints_ended_staff_path}}">
                            <i class="bi bi-file-earmark-text-fill" ></i>
                            Denuncias finalizadas (<strong class="text-info" id="complaints-closed-count">{{all_complaints_closed_count}}</strong>)
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button" href="{{table_complaints_staff_path}}">
                            <i class="bi bi-file-earmark-text-fill"></i>
                            Denuncias en tabla
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text-fill"></i>
                            Estatus vs Clasificación de denuncia abiertas
                        </a>
                      </li>
                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" role="button">
                            <i class="bi bi-file-earmark-text-fill"></i>
                            Prioridad vs Estatus abiertas
                        </a>
                      </li>

                      <li class="border-top my-3"></li>

                      <li class="nav-item p-2 custom-hover">
                        <a class="nav-link" data-bs-toggle="collapse" href="#estatusMenu" role="button" aria-expanded="false" aria-controls="estatusMenu">
                            <i class="bi bi-folder-fill"></i>
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
                            <i class="bi bi-folder-fill"></i>
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
                            <i class="bi bi-folder-fill"></i>
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
                            <i class="bi bi-folder-fill"></i>
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
                            <i class="bi bi-folder-fill"></i>
                            Por qué canal te enteraste (abiertas)
                        </a>
                        <div class="collapse" id="canalMenu">
                            <ul class="nav flex-column ms-3" id="channel-list">
                                {{all_complaints_by_channel}}
                            </ul>
                        </div>
                    </li>`;

    const all_complaints_opened_count = responseComplaintCount['all_complaints_opened_count'];
    const all_complaints_closed_count = responseComplaintCount['all_complaints_closed_count'];
    const list_user_staff_path = responseComplaintCount['list_user_staff_path'];
    let all_complaints_by_status = '';
    let all_complaints_by_city = '';
    let all_complaints_by_priority = '';
    let all_complaints_by_classification = '';
    let all_complaints_by_channel = '';

    for(const element of responseComplaintCount['all_complaints_by_status']){
        all_complaints_by_status+=`<li class="nav-item">
                                    <a class="nav-link" role="button" onclick="getComplaintsByMenuOption('${responseComplaintCount['status_staff_path']}', '${element.status}')">${element.status} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of responseComplaintCount['all_complaints_by_city']){
        all_complaints_by_city+=`<li class="nav-item">
                                    <a class="nav-link" role="button" onclick="getComplaintsByMenuOption('${responseComplaintCount['city_staff_path']}', '${element.city}')">${element.city} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of responseComplaintCount['all_complaints_by_priority']){
        all_complaints_by_priority+=`<li class="nav-item">
                                    <a class="nav-link" role="button" onclick="getComplaintsByMenuOption('${responseComplaintCount['priority_staff_path']}', '${element.priority}')">${element.priority} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of responseComplaintCount['all_complaints_by_classification']){
        all_complaints_by_classification+=`<li class="nav-item">
                                    <a class="nav-link" role="button" onclick="getComplaintsByMenuOption('${responseComplaintCount['classification_staff_path']}', '${element.classification}')">${element.classification} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    for(const element of responseComplaintCount['all_complaints_by_channel']){
        all_complaints_by_channel+=`<li class="nav-item">
                                    <a class="nav-link" role="button" onclick="getComplaintsByMenuOption('${responseComplaintCount['channel_staff_path']}', '${element.channel}')">${element.channel} (<strong class="text-info">${element.count}</strong>)</a>
                                </li>`;
    }

    sideBarListContainer = sideBarListContainer.replace(
        '{{all_complaints_opened_count}}', all_complaints_opened_count
    ).replace(
        '{{home_staff_path}}', responseComplaintCount['home_staff_path']
    ).replace(
        '{{table_complaints_ended_staff_path}}', responseComplaintCount['table_complaints_ended_staff_path']
    ).replace(
        '{{all_complaints_closed_count}}', all_complaints_closed_count
    ).replace(
        '{{table_complaints_staff_path}}', responseComplaintCount['table_complaints_staff_path']
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

    if(responsePermissions['permissions']==='all' || responsePermissions['permissions']['tasks'].includes('Usuarios')){
            sideBarListContainer+=`<li class="border-top my-3"></li>
                <li class="nav-item p-2 custom-hover">
                <a href="${list_user_staff_path}" class="nav-link" role="button">
                    <i class="bi bi-person-fill"></i>
                    Administrar Usuarios
                </a></li>`;
    }

    $('.list-container').html(sideBarListContainer+`</ul>`);

    $('.loader-wrapper').hide();
    $('.list-container').show();

});