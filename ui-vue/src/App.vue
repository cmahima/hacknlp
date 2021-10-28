<template>
    <v-app>
        <v-app-bar app color="secondary" dark>
            <div class="d-flex align-center">
                <h2>Fun with NLP</h2>
            </div>

            <v-spacer></v-spacer>

            <v-btn href="https://git.pointclickcare.com/users/tulada/repos/hacknlp/browse" target="_blank" text>
                <span class="mr-2">Bit Bucket</span>
                <v-icon>mdi-code-braces</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <div id="nav">
                <router-link :to="{name: 'PatientTable'}">Patient</router-link>
                <!--                |-->
                <!--                <router-link :to="{name: 'Iris'}">Iris Example</router-link>-->
                <!--                |-->
                <!--                <router-link :to="{name: 'Summary'}">Summary Example</router-link>-->
                | <a @click="cleanCache">Clean</a>
            </div>
            <router-view/>
        </v-main>
    </v-app>
</template>

<script>
export default {
    methods: {
        cleanCache() {
            Object.keys(localStorage).forEach(key => {
                if (key.startsWith('NLP::')) {
                    localStorage.removeItem(key);
                }
            })
        }
    }
}
</script>

<style lang="scss">
#app {
    color: #2c3e50;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

#nav {
  padding: 30px;

  a {
      color: #2c3e50;
      font-weight: bold;

      &.router-link-active,
      &.router-link-exact-active {
          color: #42b983;
      }
  }
}
</style>
