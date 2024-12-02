const apiBase = "http://localhost:5000/api";

async function fetchMongoData() {
    const response = await fetch(`${apiBase}/mongo`);
    const data = await response.json();
    displayData(data);
}

async function fetchPostgresData() {
    const response = await fetch(`${apiBase}/postgres`);
    const data = await response.json();
    displayData(data);
}

async function fetchNeo4jData() {
    const response = await fetch(`${apiBase}/neo4j`);
    const data = await response.json();
    displayData(data);
}

function displayData(data) {
    const container = document.getElementById("data");
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
