<template>
  <v-app id="inspire">
    <v-main>
      <router-view/>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>LOGIN</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    v-model = "username"
                    label="Username"
                    name="username"
                    :error-messages="usernameErrors"
                    required
                    @input="$v.username.$touch()"
                    @blur="$v.username.$touch()"
                    prepend-icon="mdi-account"
                    type="text"
                  ></v-text-field>

                  <v-text-field
                    v-model = "password"
                    id="password"
                    label="Password"
                    name="password"
                    :error-messages="passwordErrors"
                    required
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()"
                    prepend-icon="mdi-lock"
                    type="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" v-on:click="fetchData">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import { validationMixin } from 'vuelidate'
  import { required } from 'vuelidate/lib/validators'
  import VueJwtDecode from 'vue-jwt-decode'

  export default {
  mixins: [validationMixin],

  validations: {
    username: { required, },
    password: { required, },
  },

  data: () => ({
    username: '',
    password: '',
  }),

  computed: {
    usernameErrors () {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.required && errors.push('Username is required.')
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.required && errors.push('Password is required')
      return errors
    },
  },
    created() {
      if(localStorage.token != null) {
        this.$router.replace('Profile')
      }
    },
    methods: {
    fetchData: function() {

      fetch('http://localhost:5000/home',{
          mode: 'cors',
          method: 'POST',
          headers: {
              Accept: 'application/json',
              'Content-type' : 'application/json'
          },
          body: JSON.stringify({username: this.username, password: this.password})
          }).then((response) => response.json())
              .then((responseJson) => {
                let token = VueJwtDecode.decode(responseJson.token);
                localStorage.setItem('token', responseJson.token)
                let status = JSON.parse(JSON.stringify(token.status));
                  if(status == "ok"){
                      this.$router.replace({
                        name: 'Profile',
                      })
                  } else {
                    alert('zle dane logowania')
                }
            })
          .catch(error => console.log(error));
        }
      },
    }
</script>