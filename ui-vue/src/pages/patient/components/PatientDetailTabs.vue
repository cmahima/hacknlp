<template>
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
</template>

<script>
import axios from 'axios';
import PatientNotes from '@/pages/patient/components/PatientNotes.vue';
import PatientNoteHighlighted from '@/pages/patient/components/PatientNoteHighlighted.vue';

export default {
    name: "PatientDetailTabs",
    components: {PatientNoteHighlighted, PatientNotes},

    props: {
        patient: {type: Object, required: true}
    },
    async beforeMount() {
        this.summarizeNote();
        this.getHighlightedNote();
    },
    data: () => ({
        summarizedNote: {
            loading: false,
            value: ''
        },
        highlightedNote: {
            loading: false,
            value: ''
        }
    }),
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

<style scoped>

</style>