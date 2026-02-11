import {verify} from './util/verifyLogin.js'

if (await verify() == false){
    document.location.href="index.html"
}

let form = document.querySelector('form');

let hostnameInput = document.getElementsByName('entities');

let allLogs = [];
let currentOffset = 0;

async function getLogs(data){
    try {
        console.log('Sending request with data:', data);
        const response = await fetch('http://192.168.214.1:3000/log/get_logs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', 
            body: JSON.stringify(data),
        });

        console.log('Response status:', response.status, response.statusText);
        if (!response.ok) throw new Error(`Failed to fetch logs: ${response.status} ${response.statusText}`);
        
        allLogs = await response.json();
        console.log('Received logs:', allLogs);
        console.log('Number of logs:', allLogs.length);
        
        if (!Array.isArray(allLogs)) {
            console.warn('Response is not an array:', typeof allLogs);
        }
        displayLogs(allLogs, data);
        form = document.querySelector('form');
    } catch (error) {
        console.error('Error fetching logs:', error);
        alert('Error fetching logs: ' + error.message);
        document.location.href="index.html" //a enlever potentitellement 
    }
}


form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    const button = e.submitter;
    console.log(button.name)

    if (button.name == "search"){
        currentOffset = 0;
        data.offset = 0;
    } else if (button.name == "next"){
        currentOffset = currentOffset + 50;
        data.offset = currentOffset;
    } else {
        if (currentOffset - 50 >= 0){
            currentOffset = currentOffset - 50;
        } 
        data.offset = currentOffset;
    }
    data.entities = [data.entities]
    getLogs(data)
});


function displayLogs(logs, data) {
    const tableBody = document.querySelector('table tbody');

    console.log(`Entity value: ${data.entities}`) 
    
    if (!tableBody) {
        console.error('Table body not found');
        return;
    }
    tableBody.innerHTML = '';

    const entitiesValue = data.entities ? ` value="${data.entities}"` : '';
    const keywordValue = data.keyword ? ` value="${data.keyword}"` : '';
    const start_timestampValue = data.start_timestamp ? ` value="${data.start_timestamp}"` : '';
    const end_timestampValue = data.end_timestamp ? ` value="${data.end_timestamp}"` : '';

    const filter = document.createElement('tr');
    filter.innerHTML = `
        <td></td>
        <td><input type="search" name="entities"${entitiesValue} placeholder="Hostname"></td>
        <td>
            <input type="date"${start_timestampValue} name="start_timestamp"> 
            -
            <input type="date"${end_timestampValue} name="end_timestamp">
        </td>
        <td><input type="search" name="keyword"${keywordValue} placeholder="Keyword"></td>
    `;

    tableBody.appendChild(filter);

    const attributes = document.createElement('tr');
    attributes.setAttribute("id", "title");
    attributes.innerHTML = `
        <td>ID</td>
        <td>Hôte</td>
        <td>Date</td>
        <td>Message</td>
    `;
        
    tableBody.appendChild(attributes);
    
    for (let i = 0; i < logs.length; i++) {
        const log = logs[i];
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${log.id || ''}</td>
            <td>${log.fromHost || ''}</td>
            <td>${log.receivedAt || ''}</td>
            <td>${log.message || ''}</td>
        `;
        tableBody.appendChild(row);
    }
}