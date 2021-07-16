<template>
    <div>
        <CAlert
                :show.sync="dismissCountDown"
                closeButton
                color="success"
                fade
                :show="alert_success"
        >
            User Information Created Successfully
        </CAlert>
        <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
            <strong>Error Occurred!</strong> When Creating User Information.
            <p>{{ error ? error.message : ""}}</p>
        </CAlert>

        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> Users </h3>
                        <CButton color="success" @click="myModal = true" class="float-right mr-1">
                            Insert a new User
                        </CButton>
                    </CCardHeader>
                    <CCardBody>
                        <CCol lg="12">
                            <CDataTable :items="users" :fields=table_field
                                        striped
                                        fixed
                                        bordered
                            >
                                <template #show_details="{item, index}">
                                    <td class="py-2">
                                        <CButton
                                                color="success"
                                                square
                                                size="sm"
                                                @click="redirect_url(item, index)"
                                        >
                                            Details
                                        </CButton>
                                    </td>
                                </template>
                                <template #remove_details="{item, index}">
                                    <td class="py-2">
                                        <CButton
                                                color="danger"
                                                square
                                                size="sm"
                                                @click="deleteUser(item, index)"
                                        >
                                            Remove
                                        </CButton>
                                    </td>
                                </template>
                                <template #header>
                                    <CIcon name="cil-description"/> List of Users

                                </template>
                            </CDataTable>
                        </CCol>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>

        <CModal
                title="Create a new User"
                :show.sync="myModal"
                size="xl"
                :close-on-backdrop="false"
        >
            <CCol sm="24">
                <CCard>
                    <CCardHeader>
                        <strong>User Information</strong>
                    </CCardHeader>
                    <CCardBody>
                        <div>
                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            key="email"
                                            :was-validated="email.was_validated"
                                            :is-valid="email.was_validated"
                                            :description="email.description"
                                            v-model="email.value"
                                            label="Email"
                                            placeholder="Enter Email"
                                    />
                                </CCol>
                            </CRow>
                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            key="name"
                                            :was-validated="name.was_validated"
                                            :is-valid="name.was_validated"
                                            :description="name.description"
                                            v-model="name.value"
                                            label="Name"
                                            placeholder="Enter name"
                                    />
                                </CCol>
                            </CRow>

                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            key="phone"
                                            :was-validated="phone.was_validated"
                                            :is-valid="phone.was_validated"
                                            :description="phone.description"
                                            v-model="phone.value"
                                            label="Phone"
                                            placeholder="Enter phone"
                                    />
                                </CCol>
                            </CRow>

                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            type="password"
                                            key="password"
                                            :was-validated="password.was_validated"
                                            :is-valid="password.was_validated"
                                            :description="password.description"
                                            v-model="password.value"
                                            label="Password"
                                            placeholder="Enter password"
                                    />
                                </CCol>
                            </CRow>

                            <CRow>
                                <CCol md="12">
                                    <CSelect
                                        label="Role"
                                        :was-validated="role.was_validated"
                                        :is-valid="role.was_validated"
                                        :description="role.description"
                                        v-model="role.value"
                                        placeholder="Enter role"
                                        :options="role_list"
                                    />
                                </CCol>
                            </CRow>

                        </div>

                    </CCardBody>
                </CCard>
            </CCol>
            <template #footer>
                <CButton @click="myModal = false" color="danger">Discard</CButton>
                <CButton @click="submitUserInfo()" color="success">Submit</CButton>
            </template>
        </CModal>
    </div>
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
            this.updateTableData();
        },
        data: function () {
            return {
                dismissCountDown: 5,
                token: Vue.$cookies.get('token'),
                show: true,
                role_list: [{ value: "admin", label: "Admin" },{ value: "teacher", label: "Teacher" },{ value: "student", label: "Student" }],
                alert_success: false,
                alert_danger: false,
                isCollapsed: true,
                keyRefresh: 0,
                users: this.users_props,
                table_field: ["name", "is_superuser", "is_teacher", "is_student", {
                    key: 'show_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                },
                {
                    key: 'remove_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                }
                ],
                name: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
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
                phone: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
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
            updateTableData: function(){
                
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get('http://localhost:8000/api/v1/users/',config).then(function(response){
                        field.users = response.data.output
                        console.log(response.data.output)
                    }
                ).catch(error => this.users = {
                    'error': 'Error Occurred'
                })
            },
            deleteUser: function(item, index){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.delete(`http://localhost:8000/api/v1/users/${item.id}`,config).then(function(response){
                        alert('User deleted Successfully!')
                        field.updateTableData();
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
                console.log(fields.role)
                debugger
                if(fields.role.value.target.value === 'admin'){
                    fields.is_superuser = true
                }
                else if(fields.role.value.target.value === 'teacher') {
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
                    // fields.role =  null

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
