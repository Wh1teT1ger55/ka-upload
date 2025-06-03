async function login() {
    const user = document.getElementById("user").value;
    const pw = document.getElementById("pwrd").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user, password: pw }),
        credentials: "include"
    });

    const result = await res.json();

    if (res.ok) {
        document.getElementById("fileListSection").classList.remove("hidden");
        document.getElementById("invalid").classList.add("hidden");

        localStorage.setItem("authToken", result.token);
        ladeDateien();
        window.location.href = "/index.html";
    }
    else {
        document.getElementById("invalid").classList.remove("hidden");
    } 
}

document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("document");
    const formData = new FormData();
    formData.append("document", fileInput.files[0]);

    const res = await fetch("/upload", {
        method: "POST",
        body: formData,
        credentials: "include"
    });

    const result = await res.json();
    document.getElementById("uploadStatus").textContent = result.success
        ? "Upload erfolgreich!"
        : "Upload fehlgeschlagen.";
});

async function ladeDateien() {
    const token = localStorage.getItem("authToken");
    if (!token) {
        // Wenn kein Token vorhanden ist, wird der Nutzer zur Login-Seite umgeleitet.
        window.location.href = "/login";
        return;
    }

    const res = await fetch("/files", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        // Das Token wird im Authorization-Header gesendet. Beachte, dass dein Backend 'Bearer' erwartet.
        "Authorization": "Bearer " + token
    },
    credentials: "include"
    });
    if (res.ok) {
        const data = await res.json();
        const list = document.getElementById("fileList");
        list.innerHTML = "";
        data.files.forEach(f => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            //Upload Ordner muss noch eingefügt werden
            a.href = "/uploads/" + f;
            a.textContent = f;
            a.target = "_blank";
            li.appendChild(a);
            list.appendChild(li);
        });
    }
    else {
        //Sofern Token ungültig wird User zur Login Seite geschickt
        window.location.href = "/login";
    }
}