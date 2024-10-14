const base_url = 'https://django-etica-y-valores.onrender.com';
//const base_url = 'http://127.0.0.1:8000';

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

$(document).ready(async function() {

    await buildPaginationKanban(1);
    $('#interactive-kanban-loader').hide();

});

$('#main-option-select').on('change', async function() {

    let selectedValue = $(this).val();

    if (selectedValue === $('#sub-option-select').val()) {
    
        $('#kanban-message').show();
        $('#kanban-container').hide();
    
    } else {
        
        const actualPageNumber = $('#actual-page').text()
        $('#interactive-kanban-loader').show();

        $('#kanban-message').hide();
        $('#kanban-container').hide();
        await getOptionSelectedValue('#main-option-select');
        await buildPaginationKanban(actualPageNumber);
        $('#kanban-container').show();

        $('#interactive-kanban-loader').hide();

    }
});

$('#sub-option-select').on('change', async function() {

    let selectedValue = $(this).val();

    if (selectedValue === $('#main-option-select').val()) {

        $('#kanban-message').show();
        $('#kanban-container').hide();
    
    } else {

        const actualPageNumber = $('#actual-page').text();
        $('#interactive-kanban-loader').show();

        $('#kanban-message').hide();
        $('#kanban-container').hide();
        await getOptionSelectedValue('#sub-option-select');
        await buildPaginationKanban(actualPageNumber);
        $('#kanban-container').show();

        $('#interactive-kanban-loader').hide();

    }

});

$('#pagination').on('click', '.page-link', async function(){

    $('#interactive-kanban-loader').show();
    pageNumber = $(this).data('value');

    // actual page number is undefined
    if(pageNumber!==undefined){

        await buildPaginationKanban(pageNumber);
        $('#interactive-kanban-loader').hide();

    }

});

async function buildPaginationKanban(pageNumber){

    const paginator = await getPaginatorData(pageNumber);
    const selectedValue = $('#main-option-select').val();

    const complaintsGroupedByMainSelector = paginator['complaints'].reduce((acc, element) => {
        const key = element[selectedValue];

        if (!acc[key]) {
            acc[key] = [];
        }

        acc[key].push({'complaint':element, 'card':buildKanbanCard(element)});

        return acc;
    }, {});

    buildPagination(paginator);
    await buildKanban(complaintsGroupedByMainSelector);
    initializeDragula();

}

async function buildPagination(paginator) {
    // Limpiar la paginación anterior
    $('#pagination').empty();
    paginatorData = paginator['pagination'];

    // Botón de Primera Página
    if (paginatorData.has_previous) {
        $('#pagination').append(`
            <li class="page-item">
                <button type="button" class="page-link" data-value="1" aria-label="Primera">Primera</button>
            </li>
            <li class="page-item">
                <button type="button" class="page-link" data-value="${paginatorData.previous_page_number}" aria-label="Anterior">Anterior</button>
            </li>
        `);
    } else {
        $('#pagination').append(`
            <li class="page-item disabled">
                <span class="page-link">Primera</span>
            </li>
            <li class="page-item disabled">
                <span class="page-link">Anterior</span>
            </li>
        `);
    }

    // Números de Página (rango de +/- 3 páginas alrededor de la actual)
    const currentPage = paginatorData.current_page;
    const totalPages = paginatorData.total_pages;

    for (let num = Math.max(1, currentPage - 3); num <= Math.min(totalPages, currentPage + 3); num++) {
        if (num === currentPage) {
            $('#pagination').append(`
                <li class="page-item active">
                    <span class="page-link" id="actual-page">${num}</span>
                </li>
            `);
        } else {
            $('#pagination').append(`
                <li class="page-item">
                    <button type="button" class="page-link" data-value="${num}">${num}</button>
                </li>
            `);
        }
    }

    // Botón de Página Siguiente y Última
    if (paginatorData.has_next) {
        $('#pagination').append(`
            <li class="page-item">
                <button type="button" class="page-link" data-value="${paginatorData.next_page_number}" aria-label="Siguiente">Siguiente</button>
            </li>
            <li class="page-item">
                <button type="button" class="page-link" data-value="${totalPages}" aria-label="Última">Última</button>
            </li>
        `);
    } else {
        $('#pagination').append(`
            <li class="page-item disabled">
                <span class="page-link">Siguiente</span>
            </li>
            <li class="page-item disabled">
                <span class="page-link">Última</span>
            </li>
        `);
    }
}

async function getOptionSelectedValue(selector){

    const optionSelected = $(selector).val();
    let data = null;

    if(optionSelected==='priority'){
        data = await getPriorityTypes();
    }else if(optionSelected==='classification'){
        data = await getClassificationTypes();
    }else if(optionSelected==='status'){
        data = await getStatusTypes();
    }

    return data;

}

async function getPriorityTypes(){

    const response = await fetch(`${base_url}/complaint/priority_types/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    return response['priority_types'];

}

async function getStatusTypes(){

    const response = await fetch(`${base_url}/complaint/status_types/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    return response['status_types'];

}

async function getClassificationTypes(){

    const response = await fetch(`${base_url}/complaint/classification_types/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    return response['classification_types'];

}

// Función para construir el tablero Kanban agrupado por ciudades y distribuido por prioridad
async function buildKanban(complaints) {
    const kanbanContainer = $('#kanban-container');
    kanbanContainer.empty(); // Limpiar el contenedor antes de añadir nuevas filas

    const mainData = await getOptionSelectedValue('#main-option-select');
    const subData = await getOptionSelectedValue('#sub-option-select');

    for (const mainObject of mainData){

        let complaintsSelected = complaints[mainObject[$('#main-option-select').val()]];
        let kanbanColumns = '';

        if(complaintsSelected !== undefined){
            complaintsSelected.forEach(complaint => {
                kanbanColumns = subData.reduce((acc, subCategory) => {
                    let cards = '';
                    complaints[mainObject[$('#main-option-select').val()]].forEach(complaint => {
                        if(complaints[mainObject[$('#main-option-select').val()]] && subCategory[$('#sub-option-select').val()]===complaint['complaint'][$('#sub-option-select').val()]){
                            cards+=complaint['card'];
                        }
                    });
                    acc += `<div class="kanban-column rounded-0">
                            <h6 class="rounded-0 text-center">${subCategory[$('#sub-option-select').val()]}</h6>
                            <div class="kanban-cards">${cards}</div>
                        </div>`;
                    return acc;
                }, '');
            });
        }else{
            kanbanColumns = subData.reduce((acc, subCategory) => {
                acc += `<div class="kanban-column rounded-0">
                        <h6 class="rounded-0 text-center">${subCategory[$('#sub-option-select').val()]}</h6>
                        <div class="kanban-cards"></div>
                    </div>`;
                return acc;
            }, '');
        }

        let kanbanRow = `<div class="kanban-row mb-4">
                <h3 class="city-title bg-info p-2">${mainObject[$('#main-option-select').val()]}</h3>
                <div class="kanban-columns-container d-flex">
                    ${kanbanColumns}
                </div>
            </div>`;

        kanbanContainer.append(kanbanRow);

    }

    // Crear una fila para cada ciudad
    /*for (const mainCategory in complaints) {

        let kanbanColumns = subData.reduce((acc, subCategory) => {
            let cards = '';
            complaints[mainCategory].forEach(complaint => {
                if(subCategory[$('#sub-option-select').val()]===complaint['complaint'][$('#sub-option-select').val()]){
                    cards+=complaint['card'];
                }
            });
            acc += `<div class="kanban-column rounded-0">
                    <h6 class="rounded-0 text-center">${subCategory[$('#sub-option-select').val()]}</h6>
                    <div class="kanban-cards">${cards}</div>
                </div>`;
            return acc; // Devolver el acumulador con el nuevo valor añadido
        }, '');

        let kanbanRow = `
            <div class="kanban-row mb-4">
                <h3 class="city-title bg-info p-2">${mainCategory}</h3>
                <div class="kanban-columns-container d-flex">
                    ${kanbanColumns}
                </div>
            </div>`;

        kanbanContainer.append(kanbanRow.replace("{{main-category}}", mainCategory));

    }*/
}

// Función para construir una tarjeta de queja
function buildKanbanCard(complaint) {

    const date = new Date(complaint.created_at);

    const formattedDate = date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });

    return `<div class="kanban-card rounded-0" id="${complaint.id}">
                <h3>Ciudad: ${complaint.city}</h3>
                <p>Prioridad: ${complaint.priority}</p>
                <p>Responsable: ${complaint.first_name || 'No asignado'}</p>
                <p>Fecha: ${formattedDate}</p>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalComplaint" onclick="complaintDetail('${complaint.id}')">Modificar</button>
                <button class="btn btn-success" onclick="closeComplaint('${complaint.id}')">Cerrar</button>
            </div>`;
}

// Función para inicializar Dragula
function initializeDragula() {
    // Seleccionar todos los contenedores de las columnas de prioridad para Dragula
    const columns = document.querySelectorAll('.kanban-cards');

    // Asegurarse de que los contenedores existen antes de inicializar Dragula
    if (columns.length === 0) {
        console.error('No se encontraron columnas para inicializar Dragula.');
        return;
    }

    const drake = dragula(Array.from(columns), {
        moves: function (el, container, handle) {
            return true; // Permite mover cualquier tarjeta
        },
        accepts: function (el, target, source, sibling) {
            return true; // Permite soltar en cualquier contenedor
        }
    });

    // Evento para manejar el desplazamiento automático mientras se arrastra
    const scrollSpeed = 20; // Velocidad de desplazamiento
    const scrollContainer = document.querySelector('.kanban-board'); // Ajustar esto al contenedor
    let scrollInterval; // Variable para almacenar el intervalo

    drake.on('drag', function (el) {
        clearInterval(scrollInterval); // Detener cualquier desplazamiento previo

        // Iniciar el desplazamiento automático mientras se arrastra
        scrollInterval = setInterval(function() {
            let rect = scrollContainer.getBoundingClientRect();
            let dragCardRect = el.getBoundingClientRect();

            // Desplazar hacia la izquierda
            if (dragCardRect.left < rect.left + 50) {
                scrollContainer.scrollLeft -= scrollSpeed; // Desplazar a la izquierda
            }

            // Desplazar hacia la derecha
            if (dragCardRect.right > rect.right - 50) {
                scrollContainer.scrollLeft += scrollSpeed; // Desplazar a la derecha
            }
        }, 100); // Ajustar el intervalo según sea necesario
    });

    // Detener el desplazamiento al soltar la tarjeta
    drake.on('drop', function (el, target, source, sibling) {
        clearInterval(scrollInterval); // Detener el desplazamiento automático

        if (!target) {
            console.error('No se encontró el contenedor de destino para soltar el elemento.');
            return;
        }

        const newRow = target.parentElement.parentElement.parentElement.querySelector('h3').innerText;
        const newColumn = target.parentElement.querySelector('h6').innerText;
        const complaintId = el.id;

        updateComplaint(complaintId, newRow, newColumn);
    });
}

// Función para actualizar la prioridad de una queja después de moverla
function updateComplaint(complaintId, newRow, newColumn) {
    // Actualizar la prioridad mediante una solicitud al servidor si es necesario
    console.log(`Actualizando queja ${complaintId} a fila: ${newRow} y columna: ${newColumn}`);

    fetch(`${base_url}/complaint/update_dynamic_complaint/${complaintId}/`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'first_param': {'field':$('#main-option-select').val(), 'value':newRow},
            'second_param': {'field':$('#sub-option-select').val(), 'value':newColumn}
        })
    })
    .then(response => response.json())
    .then(data => {
        return data;
    })
    .catch(error => console.error('Error:', error));
}

async function getPaginatorData(page) {
    const response = await fetch(`${base_url}/complaint/paginator/?page=${page}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    }).then(response => {
        return response.json();
    }).catch(error => console.error(error));

    return response;
}
