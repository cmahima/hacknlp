<template>
    <v-tabs color="secondary">
        <v-tab>
            <v-icon left>mdi-form-select</v-icon>
            Summary
            &nbsp;&nbsp;<v-progress-circular v-if="summarizedNote.loading" :size="30" :width="5" color="purple" indeterminate></v-progress-circular>
        </v-tab>
        <v-tab>
            <v-icon left>mdi-marker</v-icon>
            Highlight
            &nbsp;&nbsp;<v-progress-circular v-if="highlightedNote.loading" :size="30" :width="5" color="purple" indeterminate></v-progress-circular>
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
            <patient-note-highlighted :highlighted-note="highlightedNote.value" :loading="highlightedNote.loading"/>
        </v-tab-item>
        <v-tab-item>
            <patient-classification :classify-note="classifyNote" :detail-note="patient.detailNote"/>
        </v-tab-item>
    </v-tabs>
</template>

<script>
import axios from 'axios';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import PatientNoteHighlighted from '@/pages/patient/components/PatientNoteHighlighted.vue';
import PatientClassification from '@/pages/patient/components/PatientClassification.vue';

export default {
    name: "PatientDetailTabs",
    components: {PatientClassification, PatientNoteHighlighted, PatientNotes},

    props: {
        patient: {type: Object, required: true}
    },
    async beforeMount() {
        this.getSummarizeNote();
        this.getHighlightedNote();
        this.getClassifiedNote();
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
        },
        async getHighlightedNote() {
            this.highlightedNote.loading = true;
            const data = await axios.post('http://127.0.0.1:8000/ner/', {text: this.patient.detailNote})
            this.highlightedNote.loading = false;
            this.highlightedNote.value = data.data.result;
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
        }
    }
}
</script>

<style lang="scss" scoped>

</style>