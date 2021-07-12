<template>
    
        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> User Information </h3>
                    </CCardHeader>
                    <CCardBody>
                        <CCardHeader>User Name: <strong>{{users.name}}</strong></CCardHeader>
                        <CCardBody>
                                <p>
                                   User Type:  <strong>{{users.user_type}}</strong> 
                                </p>
                                <p>
                                   Email Address:  <strong>{{users.email}}</strong> 
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
    import checkAuth from './_auth'
    Vue.use(VueCookies)
    import CTableWrapper from '../base/Table.vue'
    window.axios = require('axios')
    export default {
        props: ['users_props'],
        name: 'Users',
        components: { CTableWrapper },
        mounted: function(){
            this.updateUserInfo();
        },
        data: function () {
            return {
                dismissCountDown: 5,
                token: Vue.$cookies.get('token'),
                show: true,
                alert_success: false,
                alert_danger: false,
                isCollapsed: true,
                keyRefresh: 0,
                users: this.users_props,
                role: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                is_superuser: false,
                is_teacher: false,
                is_student: false,
                success: null,
                error: null,
                myModal: false,

            }
        },
        methods: {
            countDownChanged (dismissCountDown) {
                this.dismiss = dismissCountDown
            },
            updateUserInfo: function(){
                
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/users/${field.$route.params.id}`,config).then(function(response){
                        field.users = response.data.output
                        if(field.users.is_superuser){
                            field.users.user_type = 'Admin'
                        }
                        else if(field.users.is_teacher){
                            field.users.user_type = 'Teacher'
                        }
                        else if(field.users.is_student){
                            field.users.user_type = 'Student'
                        }
                    }
                ).catch(error => this.users = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `details/${item.id}`})
            },
            submitProxyRequest: function(){
                console.log('GOT')
                console.log(this.users.value)
                console.log('GOT')
                this.users.was_validated = false
                this.users.description = 'Please provide a valid User address'


            },
            submitUserInfo: function(){
                let config = {
                        headers: {
                        'Authorization': 'Bearer ' + this.token
                        }
                    }
                const fields = this
                fields.success = null
                fields.error = null
                if(fields.role.value === 'admin'){
                    fields.is_superuser = true
                }
                else if(fields.role.value === 'teacher') {
                    fields.is_teacher = true
                }
                else {
                    fields.is_student = true
                }
                
                axios.post('http://localhost:8000/api/v1/users/', {
                    user: {
                        name: fields.name.value,
                        email: fields.email.value,
                        password: fields.password.value,
                        username: fields.email.value,
                        is_superuser: fields.is_superuser,
                        is_teacher: fields.is_teacher,
                        is_student: fields.is_student,

                    }
                }, config ).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.name.was_validated = null
                    fields.email.was_validated = null
                    fields.password.was_validated = null
                    fields.username.was_validated = null
                    fields.role.was_validated = null

                    fields.name.description =  ''
                    fields.email.description =  ''
                    fields.password.description =  ''
                    fields.username.description =  ''
                    fields.role.description =  ''

                    fields.name.value =  ''
                    fields.email.value =  ''
                    fields.password.value =  ''
                    fields.username.value =  ''
                    fields.role.value =  ''

                    fields.is_student = false
                    fields.is_teacher = false
                    fields.is_superuser = false
                    fields.keyRefresh +=1;
                    fields.updateTableData();
                    console.log('====SUCCES===')
                }).catch(function(error){
                    if(error.response !== undefined){
                    console.log(error.response)
                    fields.error = error.data.message;
                    if(fields.error.hasOwnProperty('name')){
                        fields.proxy_provider_address.was_validated = false
                        fields.proxy_provider_address.description = 'Please provide a valid name'
                    }
                    if(fields.error.hasOwnProperty('email')){
                        fields.time_interval.was_validated = false
                        fields.time_interval.description = 'Please provide a valid/different Email'
                    }

                    if(fields.error.hasOwnProperty('password')){
                        fields.time_interval.was_validated = false
                        fields.time_interval.description = 'Please provide a valid password'
                    }

                    if(fields.error.hasOwnProperty('role')){
                        fields.time_interval.was_validated = false
                        fields.time_interval.description = 'Please provide a valid role'
                    }
                    }
                    else{
                    fields.keyRefresh +=1;
                    fields.updateTableData();
                    }
                })
            }
        }
    }
</script>
