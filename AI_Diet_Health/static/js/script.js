async function calculateBMI() {
    let weight = document.getElementById("weight").value;
    let height = document.getElementById("height").value;
    let age = document.getElementById("age").value;
    let activity = document.getElementById("activity").value;

    let response = await fetch("/calculate_bmi", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ weight, height, age, activity_level: activity })
    });

    let result = await response.json();
    document.getElementById("bmiResult").innerText = `BMI: ${result.bmi}, ${result.health_status} (${result.advice})`;
}

async function analyzeText() {
    let prompt = document.getElementById("textPrompt").value;

    let response = await fetch("/analyze_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    let result = await response.json();
    document.getElementById("textResult").innerText = result.response;
}

async function analyzeImage() {
    let file = document.getElementById("imageUpload").files[0];
    let formData = new FormData();
    formData.append("image", file);

    let response = await fetch("/analyze_image", { method: "POST", body: formData });
    let result = await response.json();
    document.getElementById("imageResult").innerText = result.response;
}
