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
                Subjects Created Successfully
            </CAlert>
            <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
                <strong>Error Occurred!</strong> When adding Subjects Information.
                <p>{{ error ? error.message : ""}}</p>
            </CAlert>
                
            </CCol>
            <CCol sm="24" md="12">
                    <CCard>
                        <CCardHeader>
                            <h3>  Available Subjects </h3>
                        </CCardHeader>
                        <CCardBody>
                            <CCol lg="12">
                                <CDataTable :items="subjects" :fields=table_field
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
                                <template #header>
                                    <CIcon name="cil-description"/> List of Available Subjects

                                </template>
                                </CDataTable>
                            </CCol>
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
        props: ['classes_props'],
        name: 'Classes',
        components: { CTableWrapper },
        mounted: function(){
            this.updateSubjectInfo();
            // this.availableTeachers();
            // this.getClassList()
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
                subjects: null,
                table_field: ["name", "unique_name",
                {
                    key: 'show_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                }
                ],
                teacher_id: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                name: {
                    value: null,
                    description: null,
                    was_validated: null,
                },

                class_id: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                available_teachers: [],

                available_classes: [],
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
            updateSubjectInfo: function(){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/subject/`,config).then(function(response){
                        field.subjects = response.data.output
                    }
                ).catch(error => this.subjects = {
                    'error': 'Error Occurred'
                })
            },

            availableTeachers:  function(){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/subject/${field.$route.params.id}/available-teacher/`,config).then(function(response){
                        let teacher_array = []
                        for(let i = 0; response.data.output.length > i; i+=1){
                            teacher_array.push({ value: response.data.output[i]['id'].toString(), label: response.data.output[i]['name'] })
                        }
                        console.log(teacher_array)
                        field.available_teachers = teacher_array
                    }
                ).catch(error => this.available_teachers = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `details/${item.id}`})
            },
            deleteSubjects: function(item, index){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.delete(`http://localhost:8000/api/v1/subject/${item.id}/`,config).then(function(response){
                        alert(response.data.output)
                        field.updateSubjectInfo();
                    }
                ).catch(error => this.subjects = {
                    'error': 'Error Occurred'
                })
            },
            getClassList: function(){
                
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get('http://localhost:8000/api/v1/class/',config).then(function(response){
                        let class_array = []
                        for(let i = 0; response.data.output.length > i; i+=1){
                            if(response.data.output[i]['is_archived'] === false){
                                class_array.push({ value: response.data.output[i]['id'].toString(), label: response.data.output[i]['name']+"-"+response.data.output[i]['unique_name'] })
                            }
                        }
                        console.log(class_array)
                        field.available_classes = class_array
                    }
                ).catch(error => this.available_classes = {
                    'error': 'Error Occurred'
                })
            },
            submitSubjectInfo: function(){
                let config = {
                        headers: {
                        'Authorization': 'Bearer ' + this.token
                        }
                    }
                const fields = this
                fields.success = null
                fields.error = null
                axios.post(`http://localhost:8000/api/v1/subject/`, {
                    subject: {
                        name: fields.name.value,
                        assigned_teacher: fields.teacher_id.value,
                        class_id: fields.class_id.value
                    }
                }, config ).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.name.was_validated = null

                    fields.name.description =  ''

                    fields.name.value =  ''

                    fields.teacher_id.was_validated = null

                    fields.teacher_id.description =  ''

                    fields.teacher_id.value =  ''

                    fields.class_id.was_validated = null

                    fields.class_id.description =  ''

                    fields.class_id.value =  ''
                    fields.keyRefresh +=1;
                    fields.updateSubjectInfo();
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
                    fields.updateSubjectInfo();
                    }
                })
            }
        }
    }
</script>
