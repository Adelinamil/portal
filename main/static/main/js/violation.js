const getViolation = async (violationId) => {
    const response = await fetch(`/violation/${violationId}/`, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {"X-CSRFToken": Cookies.get('csrftoken')},
    });
    if (response.status !== 200) {
        return {
            id: null,
            created: null,
            vehicle_number: null,
            description: null,
            status: null,
            proof_url: null
        }
    }
    return await response.json();
};

const descModal = document.getElementById('violationDesc');
descModal.addEventListener('hidden.bs.modal', event => {
    document.getElementById('violationText').innerText = '...';
    document.getElementById('violationInfo').innerText = '...';
    document.getElementById('violationDescription').innerText = '...';
    document.getElementById('violationUrl').style.display = 'none';
});
descModal.addEventListener('show.bs.modal', async event => {
    const violation = await getViolation(
        event.relatedTarget.attributes.getNamedItem('data-id').value
    );
    document.getElementById('violationText').innerText = `Заявление №${violation.id}`;
    document.getElementById('violationInfo').innerText = `Регистрационный номер автомобиля: ${violation.vehicle_number}`;
    if (violation.proof_url !== null) {
        const violationUrl = document.getElementById('violationUrl');
        document.getElementById("linkViolationUrl").href = violation.proof_url;
        violationUrl.style.display = 'block';
    }
    document.getElementById('violationDescription').innerText = violation.description;
});

window.addEventListener('DOMContentLoaded', function () {
    function checkScreenSize() {
        const violationsTable = document.getElementById('violationsTable');
        if (window.innerWidth < 768) {
            violationsTable.classList.add('table-sm');
        } else {
            violationsTable.classList.remove('table-sm');
        }
    }

    checkScreenSize();
    window.addEventListener('resize', function () {
        checkScreenSize();
    });
});