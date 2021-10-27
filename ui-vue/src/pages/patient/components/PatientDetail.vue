<template>
    <div>
        <v-progress-circular v-if="!patient" color="primary" indeterminate/>
        <v-container v-else>
            <v-row class="align-center mb-5">
                <v-col class="d-flex align-center" cols="12">
                    <h2 class="pr-5 main-header-title">Patient Details</h2>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
            <patient-info :patient="patient"/>
            <div class="ma-10"></div>
            <patient-notes :detail-note="patient.detailNote" :loading="loading" :summarized-note="summarizedNote"/>
          <div class="ma-10"></div>

            <v-row>
                <v-col class="d-flex align-start">
                    <v-btn color="grey" elevation="2" large @click="summarizeNote">
                        <v-icon>mdi-book-open</v-icon>
                        &nbsp;Summarize
                    </v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-textarea
                            color="secondary"
                            v-model="textToSummarize"
                            class="pt-5 pb-2 pr-2 pl-2"
                            clearable
                            auto-grow
                            hint="Enter text you want to summarize"
                            label="Text To Summarize"
                            name="text-to-summarize"/>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';
import {BASE_PATIENTS_URL} from '@/pages/patient/constants/PatientConstants.js';
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';

export default {
    name: "PatientDetail",
    components: {PatientNotes, PatientInfo},
    props: {
        id: {type: Number, required: true}
    },
    data: () => ({
        loading: false,
        patient: undefined,
        summarizedNote: 'Lorem Ipsum',
        sideBySideMode: false,

        // test code
        textToSummarize: getInitialText(),
    }),
    async beforeMount() {
        const {data} = await axios.get(`${BASE_PATIENTS_URL}/${this.id}`)
        this.patient = data;
        this.summarizeNote();
    },
    methods: {
        async summarizeNote() {
            this.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/ner/', {text: this.textToSummarize})
            this.loading = false;
            this.summarizedNote = data.data.result;
        }
    }
}

function getInitialText() {
    return 'The patient was brought to the operating room and placed in the supine position. Adequate general endotracheal anesthesia was induced. Appropriate monitoring devices were placed. The chest, abdomen and legs were prepped and draped in the sterile fashion. The right greater saphenous vein was harvested and prepared by ligating all branches with 4-0 Surgilon and flushed with heparinized blood. Hemostasis was achieved in the legs and closed with running 2-0 Dexon in the subcutaneous tissue and running 3-0 Dexon subcuticular in the skin. Median sternotomy incision was made and the left mammary artery was dissected free from its takeoff of the subclavian to its bifurcation at the diaphragm and surrounded with papaverine-soaked gauze. The pericardium was opened. The pericardial cradle was created. The patient was fully heparinized and cannulated with a single aortic and single venous cannula and bypass was instituted. A retrograde cardioplegic cannula was placed with a pursestring suture of 4-0 Prolene suture in the right atrial wall into the coronary sinus and tied to a Rumel tourniquet. An antegrade cardioplegic needle sump combination was placed in the ascending aorta and tied in place with 4-0 Prolene. The ascending aorta was crossclamped. Cold blood potassium cardioplegia was given to the ascending aorta followed by sumping through the ascending aorta followed by cold retrograde potassium cardioplegia. The obtuse marginal coronary artery was identified and opened and end-to-side anastomosis was performed to the reversed autogenous saphenous vein with running 7-0 Prolene suture and the vein was cut to length. Cold antegrade and retrograde cardioplegia were given and the posterior descending branch of the right coronary artery was identified and opened. End-to-side anastomosis was performed with a running 7-0 Prolene suture and the vein was cut to length. Cold antegrade and retrograde potassium cardioplegia were given. The mammary artery was clipped distally, divided and spatulated for anastomosis. The anterior descending was identified and opened. End-to-side anastomosis was performed through the left internal mammary artery with running 8-0 Prolene suture. The mammary pedicle was sutured to the heart with interrupted 5-0 Prolene suture. A warm antegrade and retrograde cardioplegia were given. The aortic crossclamp was removed. The partial occlusion clamp was placed. Aortotomies were made. The veins were cut to fit these and sutured in place with running 5-0 Prolene suture. A partial occlusion clamp was removed. All anastomoses were inspected and noted to be patent and dry. Ventricular and atrial pacing wires were placed. The patient was fully warmed and weaned from cardiopulmonary bypass. The patient was decannulated in the routine fashion and Protamine was given. Good hemostasis was noted. A single mediastinal and left pleural chest tube were placed. The sternum was closed with interrupted wire, linea alba with running 0 Prolene, the sternal fascia was closed with running 0 Prolene, the subcutaneous tissue with running 2-0 Dexon and the skin with running 3-0 Dexon subcuticular stitch. The patient tolerated the procedure well.'
}
</script>

<style lang="scss" scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>