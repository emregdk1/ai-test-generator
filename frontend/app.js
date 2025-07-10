const analyzeBtn = document.getElementById("analyzeBtn");
const runBtn = document.getElementById("runBtn");
const stepsOutput = document.getElementById("stepsOutput");
const resultOutput = document.getElementById("resultOutput");

let lastAnalyzedSteps = [];

analyzeBtn.addEventListener("click", async () => {
    const stepsText = document.getElementById("stepsText").value;

    const response = await fetch("http://localhost:8002/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steps_text: stepsText }),
    });

    const data = await response.json();

    lastAnalyzedSteps = data.steps;

    stepsOutput.innerHTML = `<pre>${JSON.stringify(data.steps, null, 2)}</pre>`;
});

runBtn.addEventListener("click", async () => {
    if (!lastAnalyzedSteps.length) {
        alert("Önce adımları analiz etmelisiniz.");
        return;
    }

    const response = await fetch("http://localhost:8002/run-test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lastAnalyzedSteps),
    });

    if (!response.ok) {
        const error = await response.text();
        resultOutput.innerHTML = `<pre style="color:red;">Hata: ${error}</pre>`;
        return;
    }

    const resultData = await response.json();
    resultOutput.innerHTML = `<pre>${JSON.stringify(resultData.results, null, 2)}</pre>`;

    // Eğer ekran görüntüsü varsa görsel olarak da göster
    resultData.results.forEach((step) => {
        if (step.screenshot) {
            const img = document.createElement("img");
            img.src = `data:image/png;base64,${step.screenshot}`;
            img.style.maxWidth = "500px";
            img.style.marginTop = "10px";
            resultOutput.appendChild(img);
        }
    });
});
