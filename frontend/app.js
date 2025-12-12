const API = "https://YOUR_RENDER_BACKEND_URL";  // CHANGE THIS AFTER DEPLOYMENT

// ---------- REGISTER ----------
async function register() {
    let data = {
        first_name: document.getElementById("first").value,
        last_name: document.getElementById("last").value,
        email: document.getElementById("email").value,
        password: document.getElementById("pass").value
    };

    let res = await fetch(`${API}/register/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    let out = await res.json();
    document.getElementById("msg").innerText = out.message;

    if (res.status === 201) {
        // Redirect to OTP page
        setTimeout(() => {
            window.location.href = "verify.html";
        }, 1500);
    }
}


// ---------- VERIFY OTP ----------
async function verifyOtp() {
    let data = {
        email: document.getElementById("email").value,
        otp_code: document.getElementById("otp").value
    };

    let res = await fetch(`${API}/verify_otp`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    let out = await res.json();
    document.getElementById("msg").innerText = out.message;

    if (res.status === 200) {
        setTimeout(() => {
            window.location.href = "index.html";
        }, 1500);
    }
}


// ---------- LOGIN ----------
async function login() {
    let data = {
        email: document.getElementById("email").value,
        password: document.getElementById("pass").value
    };

    let res = await fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    let out = await res.json();

    if (res.status === 200) {
        localStorage.setItem("user_id", out.user.id);
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("msg").innerText = out.detail;
    }
}


// ---------- CREATE TODO ----------
async function createTodo() {
    let data = {
        title: document.getElementById("title").value,
        subtitle: document.getElementById("subtitle").value,
        description: document.getElementById("desc").value,
        owner_id: Number(localStorage.getItem("user_id")),
        date: document.getElementById("date").value,
        time: document.getElementById("time").value
    };

    let res = await fetch(`${API}/todos/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    loadTodos();
}


// ---------- LOAD TODOS ----------
async function loadTodos() {
    let res = await fetch(`${API}/todos/`);
    let todos = await res.json();

    let list = document.getElementById("todo-list");
    list.innerHTML = "";

    todos.forEach(t => {
        list.innerHTML += `
            <div class="todo-item">
                <b>${t.title}</b><br>
                <small>${t.subtitle}</small><br>
                ${t.description}<br>
                ${t.date} ${t.time}<br>
            </div>
        `;
    });
}


// Load todos automatically if on dashboard page
if (window.location.pathname.endsWith("dashboard.html")) {
    loadTodos();
}
