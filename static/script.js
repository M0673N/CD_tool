function handleFormSubmission(formId, endpoint) {
    document.getElementById(formId).addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        const errorMessageDiv = document.getElementById('error-message');
        const successMessageDiv = document.getElementById('success-message');

        if (data.message.includes("successfully")) {
            errorMessageDiv.style.display = 'none';
            successMessageDiv.innerText = data.message;
            successMessageDiv.style.display = 'block';
            setTimeout(() => {
                successMessageDiv.style.display = 'none';
            }, 8000);
            this.reset();
        } else {
            successMessageDiv.style.display = 'none';
            errorMessageDiv.innerText = data.message;
            errorMessageDiv.style.display = 'block';
            setTimeout(() => {
                errorMessageDiv.style.display = 'none';
            }, 8000);
        }
    });
}

handleFormSubmission('add-user-form', '/add_user');
handleFormSubmission('delete-user-form', '/delete_user');
