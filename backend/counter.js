const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '../web/data/counter.json');

function getData() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
        }
    } catch {}
    return { count: 0, updated: new Date().toISOString() };
}

function saveData(data) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function getCounter() {
    return getData();
}

function incrementCounter(req) {
    const data = getData();
    data.count++;
    data.updated = new Date().toISOString();
    saveData(data);
    return data;
}

module.exports = { getCounter, incrementCounter };
