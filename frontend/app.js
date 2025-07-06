document.getElementById("run").onclick = async () => {
    const stepsText = document.getElementById("steps").value;
    let steps;

    try {
        steps = JSON.parse(stepsText);

        // Eğer steps iç içe listeyse dıştakini çıkar
        if (Array.isArray(steps) && steps.length === 1 && Array.isArray(steps[0])) {
            steps = steps[0];
        }
    } catch {
        alert("Geçersiz JSON formatı");
        return;
    }

    document.getElementById("loading").style.display = "block";

    const res = await fetch("http://localhost:8002/run-test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steps }),
    });

    const data = await res.json();

    document.getElementById("loading").style.display = "none";
    document.getElementById("results").textContent = JSON.stringify(data, null, 2);
};
