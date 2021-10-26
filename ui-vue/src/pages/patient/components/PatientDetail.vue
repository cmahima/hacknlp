<template>
    <div>
        <v-progress-circular v-if="loading"
                             color="primary"
                             indeterminate/>

        <v-container v-else>
            <v-card class="mx-auto">
                <v-row>
                    <v-col cols="3" md="3">
                        <v-row class="d-flex justify-center mt-1 mb-1">
                            <v-avatar size="128">
                                <img :alt="patient.name" :src="patient.avatar">
                            </v-avatar>
                        </v-row>
                        <v-row class="d-flex justify-center mb-1">
                            <h3>{{ patient.name }}</h3>
                        </v-row>
                    </v-col>
                    <v-col class="d-flex align-center" cols="9" md="9">
                        <v-container>
                            <v-row>
                                <v-col class="d-flex pt-0 pb-0" cols="12" md="12" sm="12">User Info</v-col>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">Gender: &nbsp;<b>Female</b></v-col>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">DOB: &nbsp;<b>XX/XX/XXXX</b></v-col>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">Phone: &nbsp;<b>123-456-7890</b></v-col>
                            </v-row>
                            <v-row>
                                <v-divider class="mt-2 mb-2"/>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex pt-0 pb-0" cols="12" md="12" sm="12">Health Info</v-col>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">Blood Type: &nbsp;<b>A</b></v-col>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">Allergies: &nbsp;<b>None</b></v-col>
                                <v-col class="d-flex pt-0" cols="4" md="4" sm="12">Covid-19: &nbsp;<b>No</b></v-col>
                            </v-row>
                        </v-container>
                    </v-col>
                </v-row>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';
import {BASE_PATIENTS_URL} from '@/pages/patient/constants/PatientConstants.js';

export default {
    name: "PatientDetail",
    props: {
        id: {type: Number, required: true}
    },
    data: () => ({
        loading: false,
        patient: undefined
    }),
    async beforeMount() {
        this.loading = true;
        const {data} = await axios.get(`${BASE_PATIENTS_URL}/${this.id}`)
        this.loading = false;
        this.patient = data;
    }
}
</script>

<style lang="scss" scoped>
.user-info-container {
    display: flex;
    flex-direction: column;
    margin: 10px 5px;

    .info-group {
        display: flex;
        flex: 1;

        &.user-info {
            border-bottom: 1px solid red;
        }

        .info-item {
            align-items: center;
            display: inline-flex;
            flex: 1;
        }
    }
}
</style>