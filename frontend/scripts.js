document.addEventListener('DOMContentLoaded', function () {
    const sign_in_btn = document.querySelector("#sign-in-btn");
    const sign_up_btn = document.querySelector("#sign-up-btn");
    const container = document.querySelector(".container");
    const signInForm = document.querySelector(".sign-in-form");
    const signUpForm = document.querySelector(".sign-up-form");
    const notificationElement = document.getElementById('notification');
    const loginloading = document.getElementById('login-btn');
    const signuploading = document.getElementById('signup-btn');

    loginloading.addEventListener('click', function() {
        this.style.backgroundColor = 'white';
        this.style.color = 'black';
        this.value = 'Loading...';
    });

    signuploading.addEventListener('click', function() {
        this.style.backgroundColor = 'white';
        this.style.color = 'black';
        this.value = 'Loading...';
    });

    sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
    });

    sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
    });

    function showNotification(message) {
        notificationElement.textContent = message;
        notificationElement.style.backgroundColor = '#f8d7da';
        notificationElement.style.borderColor = '#f5c6cb';
        notificationElement.style.display = 'block';

        setTimeout(function () {
            notificationElement.style.display = 'none';
        }, 2000);
    }

    function showNotificationOk(message) {
        notificationElement.textContent = message;
        notificationElement.style.backgroundColor = '#d4edda';
        notificationElement.style.borderColor = '#c3e6cb';
        notificationElement.style.color = '#155724';
        notificationElement.style.display = 'block';
        
        setTimeout(function () {
            notificationElement.style.display = 'none';
        }, 2000);
    }

    signInForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username-login").value;
        const password = document.getElementById("password-login").value;
    
        if (!username || !password) {
        showNotification("Please fill in both username and password.");
        return;
        }
    
        try {
        const response = await fetch("https://backend-tst-production.up.railway.app/token", {
            method: "POST",
            headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `username=${username}&password=${password}`,
        });
        if (response.ok) {
            showNotificationOk("Welcome to design service")
            window.location.href = "https://backend-tst-production.up.railway.app/docs";
            document.getElementById("username-login").value = "";
            document.getElementById("password-login").value = "";
            loginloading.style.backgroundColor = '';
            loginloading.style.color = '';
            loginloading.value = 'Login';
        } else {
            const errorData = await response.json();
            showNotification("Invalid username or password");
            loginloading.style.backgroundColor = '';
            loginloading.style.color = '';
            loginloading.value = 'Login';
        }
        } catch (error) {
        console.error("Error during login:", error.message);
        loginloading.style.backgroundColor = '';
        loginloading.style.color = '';
        loginloading.value = 'Login';
        }
    });

    signUpForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username-signup").value;
        const password = document.getElementById("password-signup").value;

        // Check if username and password are not empty
        if (!username || !password) {
            showNotification("Please fill in both username and password.");
            return;
        }

        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);
        try {
            const response = await fetch("https://backend-tst-production.up.railway.app/users", {
                method: "POST",
                headers: {
                    // Change Content-Type to "application/x-www-form-urlencoded"
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams(formData),
            });
            if (response.ok) {
                // User registered successfully, show success message
                showNotificationOk("User registered successfully.");
                // Redirect to sign-in page
                container.classList.remove("sign-up-mode");

                document.getElementById('signup-btn').style.backgroundColor = '';
                document.getElementById('signup-btn').style.color = '';
                document.getElementById('signup-btn').value = 'Sign up';
                
                // Clear input fields
                document.getElementById("username-signup").value = "";
                document.getElementById("email-signup").value = "";
                document.getElementById("password-signup").value = "";
            } else {
                // Registration failed, show error message
                showNotification("Registration failed. Please try again.");
            }
        } catch (error) {
            console.error("Error during registration:", error.message);
        }
    });
});