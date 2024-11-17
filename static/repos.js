window.onload = loadRepositories;

// this is my Logout functionality
document.getElementById("logoutButton").onclick = function () {
    if (confirm("Are you sure you want to log out?")) {
        fetch('/logout', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = '/';
            })
            .catch(error => alert("Logout failed: " + error.message));
    }
};

// this is my Add repository functionality
document.getElementById("addRepoButton").onclick = function () {
    const name = document.getElementById("repoName").value;
    const description = document.getElementById("repoDescription").value;
    const fileInput = document.getElementById("repoFile");

    if (!name || !description || !fileInput.files.length) {
        alert("Please fill all the fields and select files");
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    Array.from(fileInput.files).forEach(file => formData.append('files[]', file));

    fetch('/repos', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadRepositories();
            document.getElementById("repoName").value = '';
            document.getElementById("repoDescription").value = '';
            fileInput.value = '';
        })
        .catch(error => alert('Error adding repository: ' + error.message));
};

// this is my Load repositories with sorting and searching functionality 
document.getElementById("sortButton").onclick = function () {
    const sortBy = document.getElementById("sortOption").value;
    loadRepositories(sortBy);
};

document.getElementById("searchButton").onclick = function () {
    const searchTerm = document.getElementById("searchInput").value;
    loadRepositories(undefined, searchTerm);
};

function loadRepositories(sortBy = 'id', searchTerm = '') {
    const fetchUrl = `/repos?sort_by=${sortBy}&search=${encodeURIComponent(searchTerm)}`;
    fetch(fetchUrl)
        .then(response => response.json())
        .then(repositories => {
            const tbody = document.getElementById("repoTableBody");
            tbody.innerHTML = '';

            repositories.forEach((repo, index) => {
                const filePreviews = repo.file_paths ? repo.file_paths.split(',').map(file => {
                    const fileName = file.split('/').pop();  // Get file name
                    return `<a href="/${file}" download>${fileName}</a>`;
                }).join('<br>') : '';

                tbody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${repo.name}</td>
                        <td>${repo.description}</td>
                        <td>${filePreviews}</td>
                        <td>${repo.created_at}</td>
                        <td>
                            <button class="update-button" onclick="editRepo(${repo.id})">Update</button>
                            <button class="delete-button" onclick="deleteRepo(${repo.id})">Delete</button>
                        </td>
                    </tr>`;
            });
        })
        .catch(error => alert('Error loading repositories: ' + error.message));
}

// this is my edit repo functionality 
function editRepo(repoId) {
    const name = prompt("Enter new repository name:");
    const description = prompt("Enter new repository description:");

    if (!name || !description) {
        alert("Name and description are required.");
        return;
    }

    fetch(`/repos/${repoId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadRepositories();
        })
        .catch(error => alert('Error editing repository: ' + error.message));
}

function deleteRepo(repoId) {
    if (!confirm("Are you sure you want to delete this repository?")) return;

    fetch(`/repos/${repoId}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadRepositories();
        })
        .catch(error => alert('Error deleting repository: ' + error.message));
}

// this is my profile related js
document.addEventListener('DOMContentLoaded', function () {
    const profileButton = document.getElementById('profileButton');
    const profileModal = document.getElementById('profileModal');
    const closeModal = document.querySelector('.close');
    const updateProfileButton = document.getElementById('updateProfileButton');
    const deleteAccountButton = document.getElementById('deleteAccountButton');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    // this will Open profile modal
    profileButton.addEventListener('click', () => {
        fetchProfileData();
        profileModal.style.display = 'block';
    });

    // this will Close profile modal
    closeModal.addEventListener('click', () => {
        profileModal.style.display = 'none';
    });

    // his will Fetch and display profile data
    function fetchProfileData() {
        fetch('/profile', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.email) {
                emailInput.value = data.email;
            }
        })
        .catch(error => console.error('Error fetching profile data:', error));
    }

    // this will Update profile data
    updateProfileButton.addEventListener('click', () => {
        const email = emailInput.value;
        const password = passwordInput.value;
        const updateData = {};
        if (email) updateData.email = email;
        if (password) updateData.password = password;
        if (Object.keys(updateData).length === 0) {
            alert("No updates were provided.");
            return;
        }

        fetch('/profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            profileModal.style.display = 'none';
        })
        .catch(error => console.error('Error updating profile:', error));
    });

    // this will Delete account
    deleteAccountButton.addEventListener('click', () => {
        if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
            fetch('/profile', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.text())
            .then(data => {
                console.log('Raw response:', data);
                try {
                    const jsonData = JSON.parse(data);
                    alert(jsonData.message);
                    window.location.href = '/';
                } catch (error) {
                    console.error('Error parsing JSON:', error);
                    alert('An error occurred while deleting the account. Please try again.');
                }
            })
            .catch(error => console.error('Deletion is not Allowed: Please Make Sure All The Added Repositories Must be Deleted Before Deletion of Your Account !'));
        }
    });
   
});