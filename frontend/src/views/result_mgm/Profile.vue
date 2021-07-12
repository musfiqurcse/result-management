<template>
    
        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> Profile Information </h3>
                    </CCardHeader>
                    <CCardBody>
                        <CCardHeader>User Name: <strong>{{name}}</strong></CCardHeader>
                        <CCardBody>
                                <p>
                                   User Type:  <strong>{{is_usertype}}</strong> 
                                </p>
                            <br>
                        </CCardBody>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>
    
</template>
<script>
import Vue from 'vue';
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
window.axios = require('axios')
export default {
    props: ['profile_props'],
    name: 'ProfileView',
    mounted: function(){
     
    },
    data: function () {
        const is_superuser = Vue.$cookies.get('is_superuser')
      const is_teacher = Vue.$cookies.get('is_teacher')
      const is_student = Vue.$cookies.get('is_student')
      const token = Vue.$cookies.get('token')
      const name = Vue.$cookies.get('name')
      var userType = "";
      if(is_superuser === "true"){
          userType = "Admin"
      }
      else if(is_teacher === "true"){
          userType = "Teacher"
      }

      else if(is_student === "true"){
          userType = "Student"
      } 
        return {
            is_usertype:userType,
            token: token,
            name: name,
            show: true,
            isCollapsed: true,
            func_test: null,
            proxies: null,

        }
    },
    methods: {
        redirect_url: function (item, index) {
            console.log(index)
            console.log(item)
            this.$router.push({ path: `details/${item.id}`})
        }
    }
}
</script>
