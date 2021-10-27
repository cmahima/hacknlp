<template>
    <v-container>
        <v-row class="align-center mb-5">
            <v-col class="d-flex align-center" cols="12">
                <h2 class="pr-5 main-header-title">Patients</h2>
                <v-divider></v-divider>
            </v-col>
        </v-row>
        <v-card>
            <v-card-title>
                Search Patient
                <v-spacer></v-spacer>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    hide-details
                    label="Search"
                    single-line
                ></v-text-field>
            </v-card-title>
            <v-data-table
                :headers="headers"
                :items="patientList"
                :items-per-page="10"
                :loading="loading"
                :search="search"
                loading-text="Loading patient data.... Please wait"
                @click:row="handleRowClick">
                <template v-slot:item.name="{ item }">
                    <v-row align="center" class="spacer pa-1" no-gutters>
                        <v-col cols="4">
                            <v-avatar>
                                <img :src="item.avatar" alt="item.name">
                            </v-avatar>
                        </v-col>
                        <v-col cols="8">
                            <strong v-html="item.name"></strong>
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:item.phone="{ item }">
                    <v-chip color="secondary" dark>
                        {{ item.phone }}
                    </v-chip>
                </template>
                <template v-slot:item.dateOfBirth="{ item }">
                        {{ item.dateOfBirth | formatDate("MM/DD/yyyy") }}
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script>
import axios from 'axios';
import {BASE_PATIENTS_URL} from '@/pages/patient/constants/PatientConstants.js';

export default {
    name: "PatientTable",
    data: () => ({
        loading: false,
        search: '',
        headers: [
            {text: 'ID', align: 'start', sortable: true, value: 'id'},
            {text: 'Name', value: 'name', width: '200px'},
            {text: 'Phone', value: 'phone'},
            {text: 'Street Address', value: 'streetAddress'},
            {text: 'City', value: 'city'},
            {text: 'DoB', value: 'dateOfBirth'}
        ],
        patientList: []
    }),

    methods: {
        handleRowClick(patient) {
            this.$router.push({name: 'PatientDetail', params: {id: patient.id}})
        }
    },
    async beforeMount() {
        this.loading = true;
        const {data} = await axios.get(BASE_PATIENTS_URL);
        this.loading = false;
        this.patientList = data;
    }
}
</script>

<style scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>