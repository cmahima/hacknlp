<template>
    <v-card class="mx-auto">
        <v-row>
            <v-col class="user-avatar-wrapper mt-1 mb-1" cols="3" md="3">
                <v-row class="d-flex justify-center mt-1 mb-1">
                    <v-avatar size="128">
                        <img :alt="patient.name" :src="patient.avatar">
                    </v-avatar>
                </v-row>
                <v-row class="d-flex justify-center mb-1">
                    <h3>{{ patient.name }}</h3>
                </v-row>
            </v-col>
            <v-divider class="mt-2 mb-2" vertical></v-divider>
            <v-col class="d-flex align-center" cols="9" md="9">
                <v-container>
                    <v-row>
                        <v-col class="d-flex pt-0 patient-info-container-header" cols="12" md="12" sm="12" xs="12">User Info</v-col>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">Gender: &nbsp;<b>{{ patient.gender }}</b></v-col>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">DOB: &nbsp;<b>{{
                                patient.dateOfBirth | formatDate('MM/DD/yyyy')
                            }}</b></v-col>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">Phone: &nbsp;<b>{{ patient.phone }}</b></v-col>
                    </v-row>
                    <v-row>
                        <v-divider class="mt-2 mb-2"/>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex pt-0 patient-info-container-header" cols="12" md="12" sm="12" xs="12">Health Info</v-col>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">Blood Type: &nbsp;<b>A</b></v-col>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">Allergies: &nbsp;<b>None</b></v-col>
                        <v-col class="d-flex pt-0" cols="4" md="4" sm="12" xs="12">Covid-19: &nbsp;<b>No</b></v-col>
                    </v-row>
                </v-container>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    name: "PatientInfo",
    props: {
        patient: {type: Object, required: true}
    }
}
</script>

<style lang="scss" scoped>
.patient-info-container-header {
    color: grey;
    font-size: .8em;
}
</style>