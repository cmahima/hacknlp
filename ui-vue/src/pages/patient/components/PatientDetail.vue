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

            <v-tabs color="secondary">
                <v-tab>
                    <v-icon left>mdi-form-select</v-icon>
                    Summary
                </v-tab>
                <v-tab>
                    <v-icon left>mdi-marker</v-icon>
                    Highlight
                </v-tab>
                <v-tab-item>
                    <v-card>
                        <patient-notes :detail-note="patient.detailNote" :loading="summarizedNote.loading" :summarized-note="summarizedNote.value"/>
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
                                        v-model="this.patient.detailNote"
                                        auto-grow
                                        class="pt-5 pb-2 pr-2 pl-2"
                                        clearable
                                        color="secondary"
                                        hint="Enter text you want to summarize"
                                        label="Text To Summarize"
                                        name="text-to-summarize"/>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-tab-item>
                <v-tab-item>
                    <v-container>
                        <v-card>
                            <patient-note-highlighted :highlighted-note="highlightedNote.value" :loading="highlightedNote.loading"/>
                        </v-card>
                    </v-container>
                </v-tab-item>
            </v-tabs>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import * as PatientApiService from '../services/PatientApiService.js'
import PatientNoteHighlighted from '@/pages/patient/components/PatientNoteHighlighted.vue';

export default {
    name: "PatientDetail",
    components: {PatientNoteHighlighted, PatientNotes, PatientInfo},
    props: {
        id: {type: [Number, String], required: true}
    },
    data: () => ({
        patient: undefined,
        summarizedNote: {
            loading: false,
            value: ''
        },
        highlightedNote: {
            loading: false,
            value: ''
        }
    }),
    async beforeMount() {
        this.patient = await PatientApiService.findById(this.id)
        this.summarizeNote();
        this.getHighlightedNote();
    },
    methods: {
        async summarizeNote() {
            this.summarizedNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/summarize/', {text: this.patient.detailNote})
            this.summarizedNote.loading = false;
            this.summarizedNote.value = data.data.result;
        },
        async getHighlightedNote() {
            this.highlightedNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/ner/', {text: this.patient.detailNote})
            this.highlightedNote.loading = false;
            this.highlightedNote.value = data.data.result;
        }
    }
}

</script>

<style lang="scss" scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>