<template>
    <div>
        <v-progress-circular v-if="!patient" color="primary" indeterminate/>
        <v-container v-else>
            <patient-info :patient="patient"/>
            <div class="ma-10"></div>
            <v-row>
                <v-col cols="9">
                    <v-switch v-model="sideBySideMode" inset label="Side By Side View"></v-switch>
                </v-col>
            </v-row>
            <patient-notes v-if="!sideBySideMode" :detail-note="patient.detailNote" :loading="loading" :summarized-note="summarizedNote"/>
            <patient-notes-side-by-side v-else :patient="patient"/>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';
import {BASE_PATIENTS_URL} from '@/pages/patient/constants/PatientConstants.js';
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import PatientNotesSideBySide from '@/pages/patient/components/PatientNotesSideBySide.vue';

export default {
    name: "PatientDetail",
    components: {PatientNotesSideBySide, PatientNotes, PatientInfo},
    props: {
        id: {type: Number, required: true}
    },
    data: () => ({
        loading: false,
        patient: undefined,
        summarizedNote: 'Lorem Ipsum',
        sideBySideMode: false
    }),
    async beforeMount() {
        const {data} = await axios.get(`${BASE_PATIENTS_URL}/${this.id}`)
        this.patient = data;
        this.summarizeNote();
    },
    methods: {
        async summarizeNote() {
            this.loading = true;
            setTimeout(() => {
                this.loading = false;
            }, 2000);
        }
    }
}
</script>

<style lang="scss" scoped>

</style>