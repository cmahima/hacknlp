<template>
    <v-row justify="end">
        <v-dialog v-model="showDialog" max-width="600px" persistent>
            <v-card>
                <v-card-title><span class="text-h5">User Profile</span></v-card-title>
                <v-card-text>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-container>
                            <v-row>
                                <v-col cols="12" md="6" sm="6">
                                    <v-text-field v-model="patientData.firstName" :rules="requiredRule" label="First Name *" required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6" sm="6">
                                    <v-text-field v-model="patientData.lastName"
                                                  :rules="requiredRule"
                                                  label="Last Name *"
                                                  persistent-hint
                                                  required></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6" sm="6">
                                    <v-menu v-model="showDatePicker"
                                            :close-on-content-click="false"
                                            :nudge-right="40"
                                            max-width="290px"
                                            min-width="290px"
                                            offset-y
                                            transition="scale-transition">
                                        <template v-slot:activator="{ on }">
                                            <v-text-field :rules="requiredRule"
                                                          :value="formattedDate"
                                                          label="Date of Birth *"
                                                          prepend-inner-icon="mdi-calendar-month-outline"
                                                          readonly
                                                          required
                                                          v-on="on"></v-text-field>
                                        </template>
                                        <v-date-picker v-model="patientData.birthDate"
                                                       locale="en-in"
                                                       no-title
                                                       @input="showDatePicker = false"></v-date-picker>
                                    </v-menu>
                                </v-col>
                                <v-col cols="12" md="6" sm="6">
                                    <v-select
                                        v-model="patientData.gender"
                                        :items="['male', 'female', 'other', 'unknown']"
                                        :rules="requiredRule"
                                        label="Gender *"
                                        required
                                    ></v-select>
                                </v-col>
                                <v-col cols="12" md="12" sm="12">
                                    <v-textarea
                                        v-model="patientData.note"
                                        hint="Enter Note"
                                        label="Note"
                                    ></v-textarea>
                                </v-col>
                            </v-row>
                        </v-container>
                        <small>*indicates required field</small>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="$emit('close')">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import moment from 'moment';
import axios from 'axios';
import {BASE_DOCUMENT_URL_FHIR, BASE_PATIENTS_URL_FHIR} from '@/pages/patient/constants/PatientConstants.js';

export default {
    name: "AddEditPatient",
    props: {
        showDialog: {type: Boolean, default: false}
    },
    data: () => ({
        valid: false,
        showDatePicker: false,
        requiredRule: [
            v => !!v || 'This field is required'
        ],
        patientData: {
            firstName: '',
            lastName: '',
            birthDate: '',
            gender: '',
            note: ''
        }
    }),
    methods: {
        async save() {
            if (this.validate()) {
                const data = await this.savePatient();

                if (this.patientData.note && this.patientData.note.length > 0) {
                    await this.saveNote(data.data.id);
                }
                this.$emit('save')
            }
        },
        async savePatient() {
            return axios.post(BASE_PATIENTS_URL_FHIR, {
                    "resourceType": "Patient",
                    "active": true,
                    "name": [{"family": this.patientData.lastName, "given": [this.patientData.firstName]}],
                    "gender": this.patientData.gender,
                    "birthDate": this.patientData.birthDate
                }
            )
        },
        async saveNote(id) {
            return axios.post(BASE_DOCUMENT_URL_FHIR, {
                    "resourceType": "DocumentReference",
                    "status": "current",
                    "subject": {
                        "reference": `Patient/${id}`
                    },
                    "description": this.patientData.note,
                    "content": [
                        {
                            "attachment": {
                                "contentType": "text/plain"
                            }
                        }
                    ]
                }
            )
        },
        validate() {
            return this.$refs.form.validate()
        },
        reset() {
            this.$refs.form.reset()
        },
        resetValidation() {
            this.$refs.form.resetValidation()
        }
    },
    computed: {
        formattedDate() {
            if (this.patientData.birthDate) {
                return moment(this.patientData.birthDate).format('MM/DD/yyyy')
            }
            return ''
        }
    }
}
</script>

<style scoped>

</style>