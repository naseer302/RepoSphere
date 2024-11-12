 // Load repositories when the page loads
 window.onload = loadRepositories;

 // Logout functionality
 document.getElementById("logoutButton").onclick = function () {
     // Prompt the user for confirmation
     if (confirm("Are you sure you want to log out?")) {
         fetch('/logout', { method: 'POST' })
             .then(response => response.json())
             .then(data => {
                 alert(data.message);
                 window.location.href = '/'; // Redirect to landing page
             })
             .catch(error => {
                 alert("Logout failed: " + error.message); // Show error if the logout fails
             });
     } else {
         // User canceled the logout action
         console.log("Logout canceled");
     }
 };

// Add repository functionality
 document.getElementById("addRepoButton").onclick = function () {
     const name = document.getElementById("repoName").value;
     const description = document.getElementById("repoDescription").value;
     const fileInput = document.getElementById("repoFile");

     if (!name || !description || !fileInput.files.length) {
         alert("Please fill all the fields and select a folder");
         return;
     }

     const formData = new FormData();
     formData.append('name', name);
     formData.append('description', description);

     Array.from(fileInput.files).forEach(file => {
         formData.append('files[]', file);
     });

     fetch('/repos', {
         method: 'POST',
         body: formData
     })
         .then(response => response.json())
         .then(data => {
             alert(data.message);
             loadRepositories();

             document.getElementById("repoName").value = '';
             document.getElementById("repoDescription").value = '';
             fileInput.value = '';
         })
         .catch(error => {
             console.error('Error:', error);
             alert('An error occurred while adding the repository.');
         });
 };


 // Update repository
 function updateRepo(id) {
     const name = prompt("Enter new name:");
     const description = prompt("Enter new description:");
     if (name) {
         fetch(`/repos/${id}`, {
             method: 'PUT',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ name, description })
         })
             .then(response => response.json())
             .then(data => {
                 alert(data.message);
                 loadRepositories();
             });
     }
 }
 /// Handle User Profile Section

document.addEventListener('DOMContentLoaded', function () {
    const profileButton = document.getElementById('profileButton');
    const profileModal = document.getElementById('profileModal');
    const closeModal = document.querySelector('.close');
    const updateProfileButton = document.getElementById('updateProfileButton');
    const deleteAccountButton = document.getElementById('deleteAccountButton');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    // Open profile modal
    profileButton.addEventListener('click', () => {
        fetchProfileData();
        profileModal.style.display = 'block';
    });

    // Close profile modal
    closeModal.addEventListener('click', () => {
        profileModal.style.display = 'none';
    });

    // Fetch and display profile data
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

    // Update profile data
    updateProfileButton.addEventListener('click', () => {
        const email = emailInput.value;
        const password = passwordInput.value;

        // Only include fields with values
        const updateData = {};
        if (email) updateData.email = email;
        if (password) updateData.password = password;

        // Check if there's anything to update
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

   
 // Delete repository
 function deleteRepo(id) {
     if (confirm("Are you sure you want to Delete this Repo?")){
     fetch(`/repos/${id}`, { method: 'DELETE' })
         .then(response => response.json())
         .then(data => {
             alert(data.message);
             loadRepositories();
         });
     }
     else{
         console.log("Canceled");
     }
 }

    // Delete account
    deleteAccountButton.addEventListener('click', () => {
        if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
            fetch('/profile', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = '/'; // Redirect to the homepage after deletion
            })
            .catch(error => console.error('Error deleting account:', error));
        }
    });
});
