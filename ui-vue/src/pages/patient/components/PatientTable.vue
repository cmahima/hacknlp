<template>
    <v-container>
        <v-row class="align-center mb-5">
            <v-col class="d-flex align-center" cols="12">
                <h2 class="pr-5 main-header-title">Patients</h2>
                <v-divider></v-divider>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="d-flex justify-end" cols="12">
                <v-btn color="green" dark @click="showAddDialog = true">
                    <v-icon>mdi-plus</v-icon>&nbsp;Add Patient
                </v-btn>
            </v-col>
        </v-row>
        <div class="ma-5"></div>
        <v-card>
            <v-card-title>
                <v-switch v-model="displayPatientWithNotes" inset label="Patient With Notes Only"></v-switch>
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
                :items="computedPatients"
                :items-per-page="10"
                :loading="loading"
                :search="search"
                loading-text="Loading patient data.... Please wait"
                @click:row="handleRowClick">
                <template v-slot:item.name="{ item }">
                    <v-row align="center" class="spacer pa-1" no-gutters>
                        <v-col cols="4">
                            <v-avatar>
                                <img alt="item.name" src="../../../assets/placeholder.png">
                            </v-avatar>
                        </v-col>
                        <v-col cols="8">
                            <strong>{{ item.name }}</strong>
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:item.phone="{ item }">
                    <v-chip color="secondary" dark>
                        {{ item.phone }}
                    </v-chip>
                </template>
                <template v-slot:item.birthDate="{ item }">
                    {{ item.birthDate | formatDate("MM/DD/yyyy") }}
                </template>
            </v-data-table>
        </v-card>

        <!-- -->
        <add-edit-patient v-if="showAddDialog" :show-dialog="showAddDialog"
                          @close="showAddDialog = false"
                          @save="onSavePatient()"/>

    </v-container>
</template>

<script>
import * as PatientApiService from '../services/PatientApiService.js'
import AddEditPatient from '@/pages/patient/components/AddEditPatient.vue';

export default {
    name: "PatientTable",
    components: {AddEditPatient},
    data: () => ({
        loading: false,
        search: '',
        displayPatientWithNotes: true,
        showAddDialog: false,
        headers: [
            {text: 'Name', value: 'name', width: '200px'},
            {text: 'Gender', value: 'gender'},
            {text: 'Street Address', value: 'streetAddress'},
            {text: 'City', value: 'city'},
            {text: 'State', value: 'state'},
            {text: 'Postal Code', value: 'postalCode'},
            {text: 'DoB', value: 'birthDate'}
        ],
        patientList: [],
        totalPatientCount: null
    }),
    computed: {
        computedPatients() {
            if (this.displayPatientWithNotes) {
                return this.patientList.filter(pat => !!pat.detailNote);
            }
            return this.patientList;
        }
    },
    methods: {
        onSavePatient() {
            this.showAddDialog = false;
            this.loadPatients();
        },
        handleRowClick(patient) {
            this.$router.push({name: 'PatientDetail', params: {id: patient.id}})
        },
        async loadPatients() {
            this.loading = true;
            const [patients, totalPatientCount] = await PatientApiService.findAll();
            this.loading = false;
            this.totalPatientCount = totalPatientCount;
            this.patientList = patients;
        }

    },
    async beforeMount() {
        this.loadPatients();
    }
}
</script>

<style scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>