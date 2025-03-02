document.getElementById('add-user-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/add_user', {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();

    const errorMessageDiv = document.getElementById('error-message');

    if (data.message === "User added successfully") {
        alert("User added successfully");
        errorMessageDiv.style.display = 'none';
        this.reset();
    } else {
        errorMessageDiv.innerText = data.message;
        errorMessageDiv.style.display = 'block';
    }
});

document.getElementById('delete-user-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/delete_user', {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();

    const errorMessageDiv = document.getElementById('error-message');

    if (data.message === "User deleted successfully") {
        alert("User deleted successfully");
        errorMessageDiv.style.display = 'none';
        this.reset();
    } else {
        errorMessageDiv.innerText = data.message;
        errorMessageDiv.style.display = 'block';
    }
});
