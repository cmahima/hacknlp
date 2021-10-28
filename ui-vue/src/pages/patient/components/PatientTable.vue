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
                <template v-slot:item.classifyNote="{ item }">
                    <div v-if="loadingClassifiyNotes" class="ma-5">
                        <v-progress-circular :size="20" :width="3" color="purple" indeterminate></v-progress-circular>
                    </div>
                    <div v-else>
                    <span v-if="item.classifyNote">
                        <v-chip v-for="key in item.classifyNote.split(', ')"
                                :key="`${item.id}-${key}`"
                                :color="key === 'family support' ? 'green' : 'red'"
                                class="text-capitalize"
                                label
                                outlined>
                            {{ key }}
                        </v-chip>
                    </span>
                    </div>
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
import axios from 'axios';
import {get, put} from '../services/StorageService.js'

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
            {text: 'Social Determinants', value: 'classifyNote'},
            {text: 'DoB', value: 'birthDate'}
        ],
        patientList: [],
        totalPatientCount: null,
        loadingClassifiyNotes: false,
        classifyNote: {
            loading: false,
            value: ''
        }
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
            this.getClassifiedNote();
        },
        async getClassifiedNote() {
            const mappedPatient = this.patientList.filter(pat => !!pat.detailNote).map(patient => ({
                'patient_id': patient.id,
                'text': patient.detailNote || ''
            })).filter(patient => {
                const cachedValue = get(patient['patient_id']);
                return !(cachedValue && cachedValue.classifyNote);
            });
            if (mappedPatient.length > 0) {
                this.loadingClassifiyNotes = true;
                const data = await axios.post('http://127.0.0.1:8000/classify/', {
                    patients: mappedPatient
                });
                data.data.data.forEach(val => {
                    put(val['patient_id'], {
                        ...get(val['patient_id']),
                        ...{
                            classifyNote: val.score
                        }
                    })
                })
                this.loadingClassifiyNotes = false;
            }
            this.patientList = this.patientList.map(patient => {
                const value = get(patient.id);
                if (value && value.classifyNote) {
                    const commaSeperatedValue = [];
                    Object.keys(value.classifyNote).forEach(key => {
                        const threshold = key === 'family support' ? 30 : 70;
                        if (parseInt(value.classifyNote[key] * 100, 10) > threshold) {
                            commaSeperatedValue.push(key);
                        }
                    })
                    patient.classifyNote = commaSeperatedValue.join(", ")
                }
                return patient;
            })
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