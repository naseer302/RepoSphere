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
