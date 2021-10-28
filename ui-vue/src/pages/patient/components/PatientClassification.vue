<template>
    <v-container>
        <v-card class="d-flex flex-column pa-5 justify-center">
            <div v-if="classifyNote.loading" class="ma-5">
                <v-progress-circular :size="70" :width="7" color="purple" indeterminate></v-progress-circular>
                <h4 class="mt-5">Evaluating note.. Please Wait.</h4>
            </div>
            <div v-else>
                <v-row class="d-flex flex-column">
                    <div v-for="(value, key) in classifyNote.value" :key="key" class="pill-wrapper">
                        <v-col>
                            <v-row>
                                        <span class="label">
                                            {{ key }}&nbsp;&nbsp;
                                        </span>
                            </v-row>
                            <v-row>
                                <v-progress-linear :color="getColor(getPercentage(value, key))"
                                                   :value="parseInt(value * 100, 10)"
                                                   height="25"
                                                   striped>
                                    <strong>{{ parseInt(value * 100, 10) }}%</strong>
                                </v-progress-linear>
                            </v-row>
                        </v-col>
                    </div>
                </v-row>
            </div>
        </v-card>
    </v-container>
</template>

<script>
import {getColor} from '@/pages/patient/services/ColorService.js';

export default {
    name: "PatientClassification",
    props: {
        classifyNote: {type: Object, required: true}
    },
    methods: {
        getColor,
        getPercentage(value, classification) {
            if (classification === 'family support') {
                return 1 - value;
            }
            return value;
        }
    }
}
</script>

<style lang="scss" scoped>
.pill-wrapper {
    font-weight: 500;
    text-transform: capitalize;
}
</style>