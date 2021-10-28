import axios from 'axios';
import {BASE_PATIENTS_URL_FHIR} from '@/pages/patient/constants/PatientConstants.js';
import find from 'lodash/find.js';

async function findAll() {
    const responseData = await axios.get(BASE_PATIENTS_URL_FHIR + '?_count=1000&_revinclude=DocumentReference:patient');
    const {data: {total, entry}} = responseData;
    if (!entry) {
        return undefined;
    }
    const patients = mapPatients(entry);
    return [patients, total];
}

async function findById(id) {
    const responseData = await axios.get(BASE_PATIENTS_URL_FHIR + `?_id=${id}&_revinclude=DocumentReference:patient`);
    const {data: {entry}} = responseData;
    if (!entry) {
        return undefined;
    }
    let patients = mapPatients(entry);
    return patients[0];

}

export {
    findAll,
    findById
}

//~-- Helper functions

function mapPatients(entry) {
    const documentRef = entry.filter(en => en.search.mode === "include").map(e => e.resource);
    return entry.filter(en => en.search.mode === "match")
        .map(e => e.resource)
        .map(patient => {
            const detailNote = getDetailNote(documentRef, patient.id)
            return {
                id: patient.id,
                streetAddress: formatStreetAddress(patient),
                city: formatCity(patient),
                state: formatState(patient),
                postalCode: formatPostalCode(patient),
                name: formatName(patient),
                gender: patient.gender,
                birthDate: patient.birthDate,
                detailNote: detailNote.detailNote,
                detailNoteId: detailNote.detailNoteId
            };
        });
}

function getDetailNote(detailNoteList, patientId) {
    let note = find(detailNoteList, (note) => note.subject.reference === `Patient/${patientId}`);
    return note ? {detailNote: note.description, detailNoteId: note.id} : '';
}

function formatStreetAddress(patient) {
    return patient.address
        ? patient.address[0].line[0]
        : undefined;
}

function formatCity(patient) {
    return patient.address
        ? patient.address[0].city
        : undefined;
}

function formatState(patient) {
    return patient.address
        ? patient.address[0].state
        : undefined;
}

function formatPostalCode(patient) {
    return patient.address
        ? patient.address[0].postalCode
        : undefined;
}

function formatName(item) {
    let name = '';
    if (!item.name && !item.name.length > 0) {
        return name;
    }
    const nameToUse = item.name[0];
    if (nameToUse.prefix && nameToUse.prefix.length > 0) {
        name += nameToUse.prefix[0] + ' ';
    }
    if (nameToUse.family) {
        name += nameToUse.family + ', ';
    }

    if (nameToUse.given && nameToUse.given.length > 0) {
        name += nameToUse.given[0] + ' ';
    }
    return name;
}

