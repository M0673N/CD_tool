function handleFormSubmission(formId, method, endpoint) {
    document.getElementById(formId).addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const response = await fetch(endpoint, {
            method,
            body: formData,
        });

        const data = await response.json();
        const errorMessageDiv = document.getElementById('error-message');
        const successMessageDiv = document.getElementById('success-message');

        if (response.ok) {
            errorMessageDiv.style.display = 'none';
            successMessageDiv.innerText = data.detail;
            successMessageDiv.style.display = 'block';
            setTimeout(() => {
                successMessageDiv.style.display = 'none';
            }, 8000);
            this.reset();
        } else {
            successMessageDiv.style.display = 'none';
            errorMessageDiv.innerText = data.detail;
            errorMessageDiv.style.display = 'block';
            setTimeout(() => {
                errorMessageDiv.style.display = 'none';
            }, 8000);
        }
    });
}

handleFormSubmission('add-user-form', 'POST', '/users/add');
handleFormSubmission('delete-user-form', 'DELETE', '/users/delete');
