const fileInput = document.getElementById("fileInput");
const fileInfo = document.getElementById("fileInfo");
const loader = document.getElementById("loader");
const btn = document.querySelector(".convert-btn");
const form = document.getElementById("form");

let selectedBtn = null;

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        fileInfo.innerHTML = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    }
});

function setFormat(btn, format) {
    document.getElementById("format").value = format;
    if (selectedBtn)
        selectedBtn.classList.remove("active");
    btn.classList.add("active");
    selectedBtn = btn;
}
async function convertFile() {
    const format = document.getElementById("format").value;
    btn.disabled = true;
    loader.style.display = "block";
    const formData = new FormData(form);
    try {
        // console.log([...formData.entries()]);
        const response = await fetch("/", {
            method: "POST",
            body: formData
        });
        const titles = {
            warning: "Warning",
            error: "Error",
            info: "Information"
        };
        btn.disabled = false;
        if (!response.ok) {
            const data = await response.json();
            loader.style.display = "none";
            btn.disabled = false;
            // const msg = await response.text();
            // alert(msg);
            Swal.fire({
                position: "top",
                icon: data.type,
                title: titles[data.type] || "Message",
                text: data.message,
                customClass: {
                    popup: "small-popup",
                    confirmButton: "popup-btn"
                },
                buttonsStyling: false,

            });
            return;
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "converted_file";

        document.body.appendChild(a);
        a.click();
        a.remove();

        URL.revokeObjectURL(url);

        loader.style.display = "none";

        Swal.fire({
            position: "top",
            // width: "420px",
            // padding: "1rem",
            icon: "success",
            title: "Successful!",
            text: `File converted to ${format.toUpperCase()} successfully.`,
            // confirmButtonColor: "#2563eb",
            // confirmButtonText: "OK",
            customClass: {
                popup: "small-popup",
                confirmButton: "popup-btn"
            },
            buttonsStyling: false,

        }).then(() => {
            window.location.reload();
        });
    }
    catch (error) {
        loader.style.display = "none";
        btn.disabled = false;
        Swal.fire({
            position: "top",
            icon: "error",
            title: "Error",
            text: "Converion Fail",
            customClass: {
                popup: "small-popup",
                confirmButton: "popup-btn"
            },
            buttonsStyling: false,


        });
        console.log(error);
    }
}

const dropArea = document.getElementById("dropArea");
["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    });
});
dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("dragging");
});
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragging");
});
dropArea.addEventListener("drop", (e) => {
    dropArea.classList.remove("dragging");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        const file = files[0];
        fileInfo.innerHTML =
            `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    }
});