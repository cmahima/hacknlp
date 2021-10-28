<template>
    <v-container>
        <v-tabs color="secondary">
            <v-tab>
                <v-icon left>mdi-form-select</v-icon>
                Summary
                &nbsp;&nbsp;<v-progress-circular v-if="summarizedNote.loading"
                                                 :size="30"
                                                 :width="5"
                                                 color="purple"
                                                 indeterminate></v-progress-circular>
            </v-tab>
            <v-tab>
                <v-icon left>mdi-form-select</v-icon>
                Summary (Open AI)
                &nbsp;&nbsp;<v-progress-circular v-if="summarizedNote.loading"
                                                 :size="30"
                                                 :width="5"
                                                 color="purple"
                                                 indeterminate></v-progress-circular>
            </v-tab>
            <v-tab>
                <v-icon left>mdi-marker</v-icon>
                Highlight
                &nbsp;&nbsp;<v-progress-circular v-if="highlightedNote.loading"
                                                 :size="30"
                                                 :width="5"
                                                 color="purple"
                                                 indeterminate></v-progress-circular>
            </v-tab>
            <v-tab>
                <v-icon left>mdi-arrange-bring-forward</v-icon>
                Social Determinants
                &nbsp;&nbsp;<v-progress-circular v-if="classifyNote.loading" :size="30" :width="5" color="purple" indeterminate></v-progress-circular>
            </v-tab>
            <v-tab-item>
                <patient-notes :detail-note="patient.detailNote" :loading="summarizedNote.loading" :summarized-note="summarizedNote.value"/>
            </v-tab-item>
            <v-tab-item>
                <patient-notes :detail-note="patient.detailNote"
                               :loading="summarizedNoteOpenAi.loading"
                               :summarized-note="summarizedNoteOpenAi.value"/>
            </v-tab-item>
            <v-tab-item>
                <patient-note-highlighted :highlighted-note="highlightedNote.value" :loading="highlightedNote.loading"/>
            </v-tab-item>
            <v-tab-item>
                <patient-classification :classify-note="classifyNote" :detail-note="patient.detailNote"/>
            </v-tab-item>
        </v-tabs>
    </v-container>
</template>

<script>
import axios from 'axios';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import PatientNoteHighlighted from '@/pages/patient/components/PatientNoteHighlighted.vue';
import PatientClassification from '@/pages/patient/components/PatientClassification.vue';
import {get, put} from '../services/StorageService.js'

export default {
    name: "PatientDetailTabs",
    components: {PatientClassification, PatientNoteHighlighted, PatientNotes},

    props: {
        patient: {type: Object, required: true}
    },
    async beforeMount() {
        const savedData = get(this.patient.id);
        if (savedData && savedData.summarizedNote) {
            this.summarizedNote.value = savedData.summarizedNote
        } else {
            this.getSummarizeNote();
        }

        if (savedData && savedData.summarizedNoteOpenAi) {
            this.summarizedNoteOpenAi.value = savedData.summarizedNoteOpenAi
        } else {
            this.getSummarizeNoteOpenAi();
        }

        if (savedData && savedData.highlightedNote) {
            this.highlightedNote.value = savedData.highlightedNote
        } else {
            this.getHighlightedNote();
        }

        if (savedData && savedData.classifyNote) {
            this.classifyNote.value = savedData.classifyNote
        } else {
            this.getClassifiedNote();
        }
    },
    computed: {},
    data: () => ({
        value: 0.5,
        red: 90,
        green: 100,
        summarizedNote: {
            loading: false,
            value: ''
        },
        summarizedNoteOpenAi: {
            loading: false,
            value: ''
        },
        highlightedNote: {
            loading: false,
            value: ''
        },
        classifyNote: {
            loading: false,
            value: ''
        }
    }),
    methods: {
        async getSummarizeNote() {
            this.summarizedNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/summarize/', {text: this.patient.detailNote})
            this.summarizedNote.loading = false;
            this.summarizedNote.value = data.data.result;
            put(this.patient.id, {
                ...get(this.patient.id),
                ...{
                    summarizedNote: this.summarizedNote.value
                }
            })
        },
        async getSummarizeNoteOpenAi() {
            this.summarizedNoteOpenAi.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/summarize_openai/', {text: this.patient.detailNote})
            this.summarizedNoteOpenAi.loading = false;
            this.summarizedNoteOpenAi.value = data.data.result;
            put(this.patient.id, {
                ...get(this.patient.id),
                ...{
                    summarizedNoteOpenAi: this.summarizedNoteOpenAi.value
                }
            })
        },
        async getHighlightedNote() {
            this.highlightedNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/ner/', {text: this.patient.detailNote})
            this.highlightedNote.loading = false;
            this.highlightedNote.value = data.data.result;
            put(this.patient.id, {
                ...get(this.patient.id),
                ...{
                    highlightedNote: this.highlightedNote.value
                }
            })
        },
        async getClassifiedNote() {
            this.classifyNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/classify/', {
                patients: [
                    {
                        'patient_id': this.patient.id,
                        'text': this.patient.detailNote
                    }
                ]
            })
            this.classifyNote.loading = false;
            this.classifyNote.value = data.data.data[0].score;
            put(this.patient.id, {
                ...get(this.patient.id),
                ...{
                    classifyNote: this.classifyNote.value
                }
            })
        }
    }
}
</script>

<style lang="scss" scoped>

</style>