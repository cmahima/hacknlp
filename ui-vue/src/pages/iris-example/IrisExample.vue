<template>
    <v-container fluid>
        <v-row align="center">
            <v-col class="d-flex" cols="12" sm="6">
                <v-select v-model="formData.sepalLength"
                          :items="availableSepalLengths"
                          hint="Pick your Sepal Length"
                          label="Sepal Length"
                          persistent-hint></v-select>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
                <v-select v-model="formData.sepalWidth"
                          :items="availableSepalWidths"
                          hint="Pick your Sepal Width"
                          label="Sepal Width"
                          persistent-hint></v-select>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
                <v-select v-model="formData.petalLength"
                          :items="availablePetalLengths"
                          hint="Pick your Petal Length"
                          label="Petal Length"
                          persistent-hint></v-select>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
                <v-select v-model="formData.petalWidth"
                          :items="availablePetalWidths"
                          hint="Pick your Petal Width"
                          label="Petal Width"
                          persistent-hint></v-select>
            </v-col>

            <v-col class="d-flex" cols="12" sm="6">
                <v-btn class="flex-sm-grow-1" color="green" depressed @click="handlePredict">Predict</v-btn>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
                <v-btn class="flex-sm-grow-1" color="error" depressed @click="handleResetPrediction">Reset Prediction</v-btn>
            </v-col>
        </v-row>
        <v-row v-if="result">
            <v-col>
                <h5>{{ result }}</h5>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: 'IrisExample',

    data: () => ({
        isLoading: false,
        result: '',
        formData: {
            // sepalLength: 4,
            // sepalWidth: 2,
            // petalLength: 1,
            // petalWidth: 0.1
        },
        availableSepalLengths: [],
        availableSepalWidths: [],
        availablePetalLengths: [],
        availablePetalWidths: []
    }),
    methods: {
        async handlePredict() {
            this.isLoading = true;
            const {data: {result}} = await axios.post('http://127.0.0.1:5000/prediction/', this.formData)
            this.isLoading = false;
            this.result = result;
        },
        handleResetPrediction() {
            this.result = '';
        }
    },
    beforeMount() {
        for (let i = 4; i <= 7; i = +(i + 0.1).toFixed(1)) {
            this.availableSepalLengths.push(i);
        }
        for (let i = 2; i <= 4; i = +(i + 0.1).toFixed(1)) {
            this.availableSepalWidths.push(i);
        }
        for (let i = 1; i <= 6; i = +(i + 0.1).toFixed(1)) {
            this.availablePetalLengths.push(i);
        }
        for (let i = 0.1; i <= 3; i = +(i + 0.1).toFixed(1)) {
            this.availablePetalWidths.push(i);
        }
    }
}
</script>
