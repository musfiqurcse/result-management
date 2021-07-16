<template>
    
        <CRow>
            
            <CCol sm="24" md="12">
                <CAlert
                :show.sync="dismissCountDown"
                closeButton
                color="success"
                fade
                :show="alert_success"
        >
            Student Assigned Successfully
        </CAlert>
        <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
            <strong>Error Occurred!</strong> When adding student Information.
            <p>{{ error ? error.message : ""}}</p>
        </CAlert>
                <CCard>
                    <CCardHeader>
                        <h3> Classes Information </h3>
                    </CCardHeader>
                    <CCardBody>
                        <CCardHeader>Class Name: <strong>{{classes.name}}</strong></CCardHeader>
                        <CCardBody>
                                <p>
                                   Is Archied:  <strong>{{classes.is_archived}}</strong> 
                                </p>
                                <p>
                                   Unique Name:  <strong>{{classes.unique_name}}</strong> 
                                </p>
                            <br>
                        </CCardBody>
                    </CCardBody>
                </CCard>
            </CCol>
            <CCol sm="24" md="12">
                    <CCard>
                        <CCardHeader>
                            <h3> Assigned Students </h3>
                            <CButton color="success" @click="myModal = true" class="float-right mr-1">
                                Add Pupils
                            </CButton>
                        </CCardHeader>
                        <CCardBody>
                            <CCol lg="12">
                                <CDataTable :items="students" :fields=table_field
                                            striped
                                            fixed
                                            bordered
                                >
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
                                        <CIcon name="cil-description"/> List of Students

                                    </template>
                                </CDataTable>
                            </CCol>
                        </CCardBody>
                    </CCard>
                </CCol>
                <CModal
                title="Create a new User"
                :show.sync="myModal"
                size="xl"
                :close-on-backdrop="false"
        >
            <CCol sm="24">
                <CCard>
                    <CCardHeader>
                        <strong>Student List</strong>
                    </CCardHeader>
                    <CCardBody>
                        <div>
                            <CRow>
                                <CCol md="12">
                                    <CSelect
                                        label="Student List"
                                        :was-validated="student_id.was_validated"
                                        :is-valid="student_id.was_validated"
                                        :description="student_id.description"
                                        :value.sync="student_id.value"
                                        placeholder="Select Student"
                                        :options="available_students"
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
        props: ['classes_props'],
        name: 'Classes',
        components: { CTableWrapper },
        mounted: function(){
            this.updateClassInfo();
            this.availablePupils();
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
                classes: this.classes_props,
                students: null,
                table_field: ["name", 
                {
                    key: 'remove_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                }
                ],
                student_id: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                available_students: [],
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
            updateClassInfo: function(){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/class/${field.$route.params.id}/`,config).then(function(response){
                        field.classes = response.data.output
                        field.students = response.data.output.assigned_students
                    }
                ).catch(error => this.classes = {
                    'error': 'Error Occurred'
                })
            },

            availablePupils:  function(){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/class/${field.$route.params.id}/available-pupil/`,config).then(function(response){
                        let student_array = []
                        for(let i = 0; response.data.output.length > i; i+=1){
                            student_array.push({ value: response.data.output[i]['id'].toString(), label: response.data.output[i]['name'] })
                        }
                        console.log(student_array)
                        field.available_students = student_array
                    }
                ).catch(error => this.available_students = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `details/${item.id}`})
            },
            deleteUser: function(item, index){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.put(`http://localhost:8000/api/v1/class/${field.$route.params.id}/manage-pupil/`, {
                    class: {
                        student_id: item.id,
                        action: "REMOVE",
                    }
                },config).then(function(response){
                        alert('Student Removed Successfully!')
                        field.updateClassInfo();
                        field.availablePupils();
                    }
                ).catch(error => this.users = {
                    'error': 'Error Occurred'
                })
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
                console.log(fields.student_id.value)
                axios.put(`http://localhost:8000/api/v1/class/${fields.$route.params.id}/manage-pupil/`, {
                    class: {
                        student_id: fields.student_id.value,
                        action: "ADD",
                    }
                }, config ).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.student_id.was_validated = null

                    fields.student_id.description =  ''

                    fields.student_id.value =  ''
                    fields.keyRefresh +=1;
                    fields.updateClassInfo();
                    console.log('====SUCCES===')
                }).catch(function(error){
                    if(error.response !== undefined){
                    console.log(error.response)
                    fields.error = error.data.message;
                    if(fields.error.hasOwnProperty('student_id')){
                        fields.student_id.was_validated = false
                        fields.student_id.description = 'Please provide a valid student'
                    }
                    }
                    else{
                    fields.keyRefresh +=1;
                    fields.updateTableData();
                    fields.availablePupils();
                    }
                })
            }
        }
    }
</script>
