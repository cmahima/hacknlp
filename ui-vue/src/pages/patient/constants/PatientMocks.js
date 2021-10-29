// Some mock patient if FHIR server data get's corrupted

export {
    isMockPatient,
    getMockPatients,
    getMockPatientById
}

function isMockPatient(id) {
    return getMockPatients().map(p => p.id).includes(id);
}

function getMockPatientById(id) {
    return getMockPatients().find(pat => pat.id === id);
}

function getMockPatients() {
    return [{...mockPatient1}]
}

// Mock patient if FHIR server is not working as expected
const mockPatient1 = {
    birthDate: "1972-05-06",
    city: undefined,
    detailNote: "The patient is an 80-year-old male , who had a history of colon cancer in the past , resected approximately ten years prior to admission , history of heavy alcohol use , who presented with a two week history of poor PO intake , weight loss , and was noted to have acute on chronic Hepatitis by chemistries and question of pyelonephritis .\nHe lived alone but was driven to the hospital by his son because of reported worsening and general care and deconditioning .\nEmergency Department course ; he was evaluated in the emergency room , found to be severely cachectic and jaundiced .\nHe was given a liter of normal saline , along with thiamine , folate .\nAn abdominal ultrasound was performed showing no stones .\nChest x-ray revealed clear lungs and then he was admitted to Team C for management .\nPAST MEDICAL HISTORY :\nCancer , ten years prior to admission , status post resection .\nMEDICATIONS ON ADMISSION :\nFolic acid .\nALLERGIES :\nNone .\nFAMILY HISTORY :\nNot obtained .\nSOCIAL HISTORY :\nLives in ZXY .\nDrinks ginger brandy to excess , pipe and cigar smoker for many years .",
    detailNoteId: "21607",
    gender: "male",
    id: "1972N05L06P",
    name: "Tyler, Furious",
    postalCode: undefined,
    state: undefined,
    streetAddress: undefined
}



