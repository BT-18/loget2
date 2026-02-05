import {verify} from './util/verifyLogin.js'

if (await verify() == false){
    document.location.href="index.html"
}

let form = document.querySelector('form');
let allLogs = [];

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    
    data.entities = [data.entities]

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
        displayLogs(allLogs);
        form = document.querySelector('form');
    } catch (error) {
        console.error('Error fetching logs:', error);
        alert('Error fetching logs: ' + error.message);
    }
});

function displayLogs(logs) {
    const tableBody = document.querySelector('table tbody');
    
    if (!tableBody) {
        console.error('Table body not found');
        return;
    }
    
    tableBody.innerHTML = '';

    const filter = document.createElement('tr');
    filter.innerHTML = `
        <td></td>
        <td><input type="search" name="entities" placeholder="Hostname"></td>
        <td>
            <input type="date" name="start_timestamp"> 
            -
            <input type="date" name="end_timestamp">
        </td>
        <td><input type="search" name="keyword" placeholder="Keyword"></td>
    `;

    tableBody.appendChild(filter);

    const attributes = document.createElement('tr');
    attributes.innerHTML = `
        <td>ID</td>
        <td>Host</td>
        <td>Time Received</td>
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