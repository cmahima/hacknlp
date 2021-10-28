<template>
    <v-container>
        <v-card>
            <v-expansion-panels focusable multiple>
                <v-expansion-panel>
                    <v-expansion-panel-header>
                        Summary Note
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <div v-if="loading" class="ma-5">
                            <v-progress-circular :size="70" :width="7" color="purple" indeterminate></v-progress-circular>
                            <h4 class="mt-5">Preparing summary for the note.. Please Wait.</h4>
                        </div>
                        <p v-else class="user-note">{{ summarizedNote }}</p>
                    </v-expansion-panel-content>
                </v-expansion-panel>
                <v-expansion-panel>
                    <v-expansion-panel-header>
                        Detail Note
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <p class="user-note"> {{ detailNote }} </p>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-card>
    </v-container>
</template>

<script>
export default {
    name: "PatientNotes",
    props: {
        loading: {type: Boolean, default: false},
        detailNote: {type: String, required: false},
        summarizedNote: {type: String, required: false}
    },
}
</script>

<style scoped>
.user-note {
    text-align: start;
}
</style>