 // this will Show modals
 document.getElementById("loginButton").onclick = function() {
    document.getElementById("loginModal").style.display = "block";
};

document.getElementById("signupButton").onclick = function() {
    document.getElementById("signupModal").style.display = "block";
    document.getElementById("loginModal").style.display = "none";
};

// this will Close modals
const closeButtons = document.getElementsByClassName("close");
for (let button of closeButtons) {
    button.onclick = function() {
        this.parentElement.parentElement.style.display = "none"; 
    };
}

// this is my Login functionality
document.getElementById("loginSubmit").onclick = function() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        return response.json().then(data => {
            if (response.status === 200) {
                alert(data.message);
                window.location.href = '/repos-page'; 
            } else {
                alert(data.message);
            }
        });
    });
};

// this is my Signup functionality
document.getElementById("signupSubmit").onclick = function() {
    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        return response.json().then(data => {
            if (response.status === 201) {
                alert(data.message);
                document.getElementById("signupModal").style.display = "none";
            } else {
                alert(data.message);
            }
        });
    });
};