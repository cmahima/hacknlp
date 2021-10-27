<template>
    <v-row>
        <v-col col="12">
            <v-expansion-panels focusable multiple>
                <v-expansion-panel>
                    <v-expansion-panel-header>
                        Summary Note
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <p class="user-note">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
                            magna
                            aliqua. Ut
                            enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                        </p>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-col>
        <v-col col="12">
            <v-expansion-panels focusable>
                <v-expansion-panel>
                    <v-expansion-panel-header>
                        Detail Note
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <p class="user-note">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
                            magna
                            aliqua. Ut
                            enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
                            magna
                            aliqua. Ut
                            enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
                            magna
                            aliqua. Ut
                            enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                        </p>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-col>
    </v-row>
</template>

<script>
export default {
    name: "PatientNotesSideBySide"
}
</script>

<style scoped>

</style>