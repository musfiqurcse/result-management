<template>
  <div class="c-app flex-row align-items-center">
    <CAlert
              :show.sync="dismissCountDown"
              closeButton
              color="success"
              fade
              :show="alert_success"
            >
             Test URL Created Successfully
    </CAlert>
    <CAlert closeButton show color="danger" :show="alert_danger">
        <strong>Error!</strong> When Creating Test URL.
        <p>{{ error ? error.message : ""}}</p>
    </CAlert>
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>Login</h1>
                  <p class="text-muted">Sign In to your account</p>
                  <CInput
                    placeholder="Email"
                    autocomplete="Email"
                    :was-validated="email.was_validated"
                    :is-valid="email.was_validated"
                    :description="email.description"
                    v-model="email.value"
                  >
                    <template #prepend-content><CIcon name="cil-user"/></template>
                  </CInput>
                  <CInput
                    placeholder="Password"
                    type="password"
                    autocomplete="curent-password"
                    :was-validated="password.was_validated"
                    :is-valid="password.was_validated"
                    :description="password.description"
                    v-model="password.value"
                  >
                    <template #prepend-content><CIcon name="cil-lock-locked"/></template>
                  </CInput>
                  <CRow>
                    <CCol col="6" class="text-left">
                      <CButton @click="submitLogin()" color="primary" class="px-4">Login</CButton>
                    </CCol>
                    <!-- <CCol col="6" class="text-right">
                      <CButton color="link" class="px-0">Forgot password?</CButton>
                    </CCol> -->
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
import Vue from 'vue'
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
import CTableWrapper from '../base/Table.vue'
window.axios = require('axios')
export default {
  props: ['login_props'],
  name: 'LoginVUE',
  mounted: function(){
      this.initialLogin();
  },
  data: function() {
    return {
      dismissCountDown: 5,
      show: true,
      alert_success: false,
      alert_danger: false,
      isCollapsed: true,
      login_props: this.login_props,
      email: {
        value: null,
        description: null,
        was_validated: null,
      },
      password: {
        value: null,
        description: null,
        was_validated: null,
      },
      success: null,
      error: null,
      myModal: false,
    }
  },
  methods: {
    initialLogin: function(){
      Vue.$cookies.set('token',null);
      Vue.$cookies.set('name',null);
      Vue.$cookies.set('is_superuser',null);
      Vue.$cookies.set('is_teacher',null);
      Vue.$cookies.set('is_student',null);
      this.$forceUpdate();
    },
    submitLogin: function(){
      const fields = this ;
      fields.email.was_validated = true
      fields.password.was_validated = true
      fields.email.description = ''
      fields.password.description = ''
      axios.post('http://localhost:8000/api/v1/login/', {
        user: {
          email: fields.email.value,
          password: fields.password.value
        }
    }).then(function(response){
      fields.success = response.data
      console.log(response.data.output)
      Vue.$cookies.set('token',response.data.output.token);
      Vue.$cookies.set('name',response.data.output.name);
      Vue.$cookies.set('is_superuser',response.data.output.is_superuser);
      Vue.$cookies.set('is_teacher',response.data.output.is_teacher);
      Vue.$cookies.set('is_student',response.data.output.is_student);
      fields.$router.push({ path: `/profile`})
    }).catch(function(error){
      alert('Please Provide valid username and password')
      console.log('testing error')
    })

    },
    common: function(){
      const fields = this ;
      fields.email.was_validated = true
      fields.password.was_validated = true
      fields.email.description = ''
      fields.password.description = ''
      axios.post('http://localhost:8000/api/v1/login/', {
    }).then(function(response){

    }).catch(function(error){})

    }

  }
}
</script>
