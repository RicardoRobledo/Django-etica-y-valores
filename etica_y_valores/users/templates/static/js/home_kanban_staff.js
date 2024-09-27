const base_url = 'https://django-etica-y-valores.onrender.com';
//const url = 'http://127.0.0.1:8000';

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const drake = dragula([
    document.querySelector('#Sin-asignar .kanban-cards'),
    document.querySelector('#Alta .kanban-cards'),
    document.querySelector('#Media .kanban-cards'),
    document.querySelector('#Baja .kanban-cards')
], {
    moves: function (el, container, handle) {
        return true; // Allows moving any element
    },
    accepts: function (el, target, source, sibling) {
        return true; // Allows dropping in any container
    },
    invalid: function (el, handle) {
        return el.classList.contains('add-card-btn'); // Prevents dragging buttons
    }
});


// Automatic scrolling while dragging
const scrollSpeed = 20; // Scroll speed
const scrollContainer = document.querySelector('.kanban-board'); // Adjust this to your container
let scrollInterval; // Variable to store the interval


drake.on('drag', function (el) {
    clearInterval(scrollInterval); // Stop any previous scrolling

    // Start automatic scrolling while dragging
    scrollInterval = setInterval(function() {
        let rect = scrollContainer.getBoundingClientRect();
        let dragCardRect = el.getBoundingClientRect();

        // Scroll to the left
        if (dragCardRect.left < rect.left + 50) {
            scrollContainer.scrollLeft -= scrollSpeed; // Scroll left
        }

        // Scroll to the right
        if (dragCardRect.right > rect.right - 50) {
            scrollContainer.scrollLeft += scrollSpeed; // Scroll right
        }
    }, 100); // Adjust the interval as necessary
});


// Stop scrolling on drop
drake.on('drop', function (el, target, source, sibling) {
    clearInterval(scrollInterval); // Stop automatic scrolling
    
    const newPriority = target.parentElement.querySelector('h2').innerText;
    const code = el.id;

    updateComplaintPriority(el, code, newPriority);
});


// Other methods you already have...
async function updateComplaintPriority(el, code, newPriority) {

    const level_priorities = {
        'Sin asignar': '1',
        'Alta': '2',
        'Media': '3',
        'Baja': '4'
    };

    await fetch(`${url}/complaint/complaint_priority/${code}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json', // Change to JSON
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            new_priority: level_priorities[newPriority] // Wrap the new priority in an object
        })
    })
    .then(async (response) => {
        if (response.status === 200) {
            return response.json();
        } else {
            $('#message').show().delay(3000).fadeOut();
        }
    })
    .then(async (data) => {
        console.log('Success:', data);
    })
    .catch(async (error) => {
        console.error('Error:', error);
    });

    const priorityElement = el.querySelector('p:nth-child(2)');
    priorityElement.textContent = 'Prioridad: ' + newPriority;
}

async function closeComplaint(id){

    await fetch(`${url}/close_complaint/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    });

    location.reload();

}

function notProceedComplaint(code){
    $('#notProceedComplaintButtonModal').attr('onclick', 'notProceedComplaintModal("'+code+'")');
};

async function notProceedComplaintModal(code) {

    await fetch(`${url}/complaint/${code}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    });

    $(`#${code}`).remove();
    $('#notProceedComplaintModal').modal('hide');

}
