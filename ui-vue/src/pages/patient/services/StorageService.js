export {
    put,
    get
}

function put(patientId, value) {
    localStorage.setItem(`NLP::${patientId}`, JSON.stringify(value))
}

function get(patientId) {
    return JSON.parse(localStorage.getItem(`NLP::${patientId}`));
}