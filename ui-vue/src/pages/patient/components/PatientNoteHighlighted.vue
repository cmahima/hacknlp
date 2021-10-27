<template>
    <v-expansion-panels flat focusable multiple>
        <v-expansion-panel>
            <v-expansion-panel-header>
                Highlighted Note
            </v-expansion-panel-header>
            <v-expansion-panel-content>
                <div v-if="loading" class="ma-5">
                    <v-progress-circular :size="70" :width="7" color="purple" indeterminate></v-progress-circular>
                    <h4 class="mt-5">Processing note.. Please Wait.</h4>
                </div>
                <div class="highlighted-note" v-html="highlightedNote"></div>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
export default {
    name: "PatientNoteHighlighted",
    props: {
        loading: {type: Boolean, default: false},
        highlightedNote: {type: String, required: false}
    },
    data: () => ({})
}
</script>

<style scoped>
.highlighted-note {
    text-align: start;
}
</style>