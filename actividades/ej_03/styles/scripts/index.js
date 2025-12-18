document.addEventListener('DOMContentLoaded', function() {
    console.log("Iniciando control de temperatura...");
    
    const setpointSlider = document.getElementById("setpoint");
    const setpointValue = document.getElementById("setpoint-value");
    const currentSetpoint = document.getElementById("current-setpoint");
    const tempActual = document.getElementById("temp-actual");
    const buzzerStatus = document.getElementById("buzzer-status");
    
    if (!setpointSlider || !tempActual || !buzzerStatus) {
        console.error("Error: Elementos no encontrados");
        return;
    }
    
    setpointSlider.addEventListener("input", () => {
        const valor = setpointSlider.value;
        setpointValue.textContent = valor;
        currentSetpoint.textContent = valor;
    });
    
    setpointSlider.addEventListener("change", () => {
        const nuevoSetpoint = parseFloat(setpointSlider.value);
        
        fetch("/setpoint", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ setpoint: nuevoSetpoint })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Setpoint actualizado:", data.nuevo_setpoint);
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
    
    async function actualizarDatos() {
        try {
            const res = await fetch("/estado");
            const data = await res.json();
            
            tempActual.textContent = data.temp.toFixed(1) + " °C";
            
            if (data.temp > data.setpoint) {
                tempActual.style.color = "#e74c3c";
                tempActual.style.backgroundColor = "#ffebee";
                tempActual.style.borderColor = "#e74c3c";
            } else {
                tempActual.style.color = "#27ae60";
                tempActual.style.backgroundColor = "#e8f5e9";
                tempActual.style.borderColor = "#27ae60";
            }
            
            if (data.buzzer) {
                buzzerStatus.textContent = "🔔 ACTIVO - Temperatura alta";
                buzzerStatus.style.color = "#c0392b";
                buzzerStatus.style.backgroundColor = "#ffcdd2";
                buzzerStatus.style.borderColor = "#c0392b";
                buzzerStatus.classList.add("buzzer-activo");
            } else {
                buzzerStatus.textContent = "✅ INACTIVO - Normal";
                buzzerStatus.style.color = "#27ae60";
                buzzerStatus.style.backgroundColor = "#c8e6c9";
                buzzerStatus.style.borderColor = "#27ae60";
                buzzerStatus.classList.remove("buzzer-activo");
            }
            
        } catch (err) {
            console.error("Error al obtener datos:", err);
            tempActual.textContent = "Error";
            buzzerStatus.textContent = "Error de conexión";
        }
    }
    
    setInterval(actualizarDatos, 2000);
    actualizarDatos(); 
});
