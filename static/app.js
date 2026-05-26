const compileButton = document.getElementById("compile");
const loadSampleButton = document.getElementById("load-sample");
const sourceInput = document.getElementById("source");
const targetSelect = document.getElementById("target");
const runCheckbox = document.getElementById("run");
const generatedOutput = document.getElementById("generated");
const runtimeOutput = document.getElementById("output");

const sample = `create variable x with value 10
create variable y with value 20
add x and y into sum
print sum

if sum > 25
print sum
else
print x
end

loop 2
print sum
end`;

function setOutput(element, text) {
    element.textContent = text || "";
}

async function compileSource() {
    const cleanedSource = sourceInput.value
        .split("\n")
        .filter((line) => line.trim().toUpperCase() !== "ENDINPUT")
        .join("\n");

    const payload = {
        source: cleanedSource,
        target: targetSelect.value,
        run: runCheckbox.checked,
    };

    setOutput(generatedOutput, "Generating...");
    setOutput(runtimeOutput, "");

    try {
        const response = await fetch("/api/compile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            setOutput(generatedOutput, "");
            setOutput(runtimeOutput, data.error || "Unknown error");
            return;
        }

        setOutput(generatedOutput, data.generated);
        setOutput(runtimeOutput, data.output || "(No output)");
    } catch (err) {
        setOutput(generatedOutput, "");
        setOutput(runtimeOutput, `Request failed: ${err}`);
    }
}

compileButton.addEventListener("click", compileSource);
loadSampleButton.addEventListener("click", () => {
    sourceInput.value = sample;
});
