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
            <v-row>
                <v-col class="d-flex justify-end">
                    <v-btn color="red" dark @click="confirmDelete">
                        <v-icon>mdi-delete</v-icon>
                        Delete
                    </v-btn>
                </v-col>
            </v-row>
            <div class="ma-2"></div>
            <patient-info :patient="patient"/>
            <div class="ma-10"></div>
            <patient-detail-tabs v-if="patient.detailNote" :patient="patient"/>
            <h3 v-else>Sorry patient doesn't have any note</h3>

            <v-dialog v-model="dialog" max-width="290" persistent>
                <v-card>
                    <v-card-title class="text-h5">Are you sure you want to delete the patient?</v-card-title>
                    <v-card-text>
                        Make sure you delete only those test data you created.
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="red darken-1" text @click="dialog = false">Cancel</v-btn>
                        <v-btn color="red darken-1" text @click="deletePatient">Confirm Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-container>
    </div>
</template>

<script>
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import * as PatientApiService from '../services/PatientApiService.js'
import PatientDetailTabs from '@/pages/patient/components/PatientDetailTabs.vue';
import axios from 'axios';
import {BASE_DOCUMENT_URL_FHIR, BASE_PATIENTS_URL_FHIR} from '@/pages/patient/constants/PatientConstants.js';

export default {
    name: "PatientDetail",
    components: {PatientDetailTabs, PatientInfo},
    props: {
        id: {type: [Number, String], required: true}
    },
    data: () => ({
        dialog: false,
        patient: undefined

    }),
    methods: {
        confirmDelete() {
            this.dialog = true;
        },
        async deletePatient() {
            this.dialog = false;
            await axios.delete(BASE_DOCUMENT_URL_FHIR + this.patient.detailNoteId);
            await axios.delete(BASE_PATIENTS_URL_FHIR + this.id);
            this.$router.push({name: 'PatientTable'})
        }
    },
    async beforeMount() {
        this.patient = await PatientApiService.findById(this.id)
    }
}

</script>

<style lang="scss" scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>