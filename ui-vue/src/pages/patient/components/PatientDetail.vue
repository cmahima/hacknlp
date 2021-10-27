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
            <patient-detail-tabs v-if="patient.detailNote" :patient="patient"/>
            <h3 v-else>Sorry patient doesn't have any note</h3>
        </v-container>
    </div>
</template>

<script>
import PatientInfo from '@/pages/patient/components/PatientInfo.vue';
import * as PatientApiService from '../services/PatientApiService.js'
import PatientDetailTabs from '@/pages/patient/components/PatientDetailTabs.vue';

export default {
    name: "PatientDetail",
    components: {PatientDetailTabs, PatientInfo},
    props: {
        id: {type: [Number, String], required: true}
    },
    data: () => ({
        patient: undefined

    }),
    async beforeMount() {
        this.patient = await PatientApiService.findById(this.id)
    }
}

</script>

<style lang="scss" scoped>
.main-header-title {
    color: rgb(0 0 0 / 38%);
}
</style>