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
                            v-model="this.patient.detailNote"
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
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import * as PatientApiService from '../services/PatientApiService.js'

export default {
    name: "PatientDetail",
    components: {PatientNotes, PatientInfo},
    props: {
        id: {type: [Number, String], required: true}
    },
    data: () => ({
        loading: false,
        patient: undefined,
        summarizedNote: 'Lorem Ipsum',
    }),
    async beforeMount() {
        this.patient = await PatientApiService.findById(this.id)
        this.summarizeNote();
    },
    methods: {
        async summarizeNote() {
            this.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/summarize/', {text: this.patient.detailNote})
            this.loading = false;
            this.summarizedNote = data.data.result;
        }
    }
}

</script>

<style lang="scss" scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>