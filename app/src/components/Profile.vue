<template>
    <v-app>
        <div>
            <v-toolbar :dark=true>
                <v-row>Welcome, {{ name }} {{ surname }}!</v-row>
                <v-btn color="primary" v-on:click="logOut">Logout</v-btn>
            </v-toolbar>

            <v-data-table
                :headers="headers"
                :items="results"
                :item-key="name"
                class="elevation-1"
                >
            </v-data-table>
        </div>
    </v-app>
</template>

<script>

      import VueJwtDecode from 'vue-jwt-decode'
    export default {
        name: "Profile",
        data: function() {
          return {
              name: '',
              surname: '',
              results: [],
              headers: [
                  {
                      text: 'Login history',
                      value: 'date',
                  },
                  {text: 'Name', value: 'name'},
                  {text: 'Surname', value: 'surname'}
              ]
          }
        },
        methods: {
            logOut: function() {
                localStorage.removeItem('token');
                this.$router.replace('/')
            }
        },
        created() {
            if(localStorage.token == null) { this.$router.replace('/')}
            let userData = VueJwtDecode.decode(localStorage.token);
            this.name = userData.name;
            this.surname = userData.surname;

                fetch('http://localhost:5000/history', {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type' : 'application/json'
                    },
                    body: JSON.stringify({token: localStorage.token})
                }).then(response => response.json())
                    .then(responseJson => {
                        this.results = JSON.parse(JSON.stringify(responseJson))

                    })
                .catch( e => console.log(e))
            },
        }
</script>

<style scoped>

</style>