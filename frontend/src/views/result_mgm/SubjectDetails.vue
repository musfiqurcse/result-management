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
            Test Created Successfully
        </CAlert>
        <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
            <strong>Error Occurred!</strong> When adding Test Information.
            <p>{{ error ? error.message : ""}}</p>
        </CAlert>
                <CCard>
                    <CCardHeader>
                        <h3> Subject Information </h3>
                    </CCardHeader>
                    <CCardBody>
                        <CCardHeader>Subject Name: <strong>{{subjects.name}}</strong></CCardHeader>
                        <CCardBody>
                                <p>
                                   Is Archied:  <strong>{{subjects.is_archived}}</strong> 
                                </p>
                                <p>
                                   Unique Name:  <strong>{{subjects.unique_name}}</strong> 
                                </p>
                            <br>
                        </CCardBody>
                    </CCardBody>
                </CCard>
            </CCol>
            <CCol sm="24" md="12">
                    <CCard>
                        <CCardHeader>
                            <h3> Tests </h3>
                            <CButton v-if="subjects.is_archived === false" color="success" @click="myModal = true" class="float-right mr-1">
                                Add Tests
                            </CButton>
                        </CCardHeader>
                        <CCardBody>
                            <CCol lg="12">
                                <CDataTable :items="tests" :fields=table_field
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
                                                    @click="deleteTest(item, index)"
                                            >
                                                Remove
                                            </CButton>
                                        </td>
                                    </template>
                                    <template #header>
                                        <CIcon name="cil-description"/> List of Tests

                                    </template>
                                </CDataTable>
                            </CCol>
                        </CCardBody>
                    </CCard>
                </CCol>
                <CModal
                title="Create a new Test"
                :show.sync="myModal"
                size="xl"
                :close-on-backdrop="false"
        >
            <CCol sm="24">
                <CCard>
                    <CCardHeader>
                        <strong>Test Information</strong>
                    </CCardHeader>
                    <CCardBody>
                        <div>
                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            key="name"
                                            :was-validated="name.was_validated"
                                            :is-valid="name.was_validated"
                                            :description="name.description"
                                            v-model="name.value"
                                            label="Test Name"
                                            placeholder="Enter test name"
                                    />
                                </CCol>
                            </CRow>

                            <CRow>
                                <CCol md="12">
                                    <CInput
                                            type="date"
                                            key="test_date"
                                            :was-validated="test_date.was_validated"
                                            :is-valid="test_date.was_validated"
                                            :description="test_date.description"
                                            v-model="test_date.value"
                                            label="Test date"
                                            placeholder="Enter test date"
                                    />
                                </CCol>
                            </CRow>

                        </div>

                    </CCardBody>
                </CCard>
            </CCol>
            <template #footer>
                <CButton @click="myModal = false" color="danger">Discard</CButton>
                <CButton @click="submitTestInfo()" color="success">Submit</CButton>
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
        props: ['subjects_props'],
        name: 'Subject',
        components: { CTableWrapper },
        mounted: function(){
            this.updateSubjectInfo();
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
                subjects: this.subjects_props,
                tests: null,
                table_field: ["name", 

                {
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
                test_date: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                available_tests: [],
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
                axios.get(`http://localhost:8000/api/v1/subject/${field.$route.params.id}/`,config).then(function(response){
                        field.subjects = response.data.output
                        field.tests = response.data.output.tests
                    }
                ).catch(error => this.subjects = {
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
                        field.available_tests = student_array
                    }
                ).catch(error => this.available_tests = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `/test/details/${item.id}`})
            },
            deleteTest: function(item, index){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.delete(`http://localhost:8000/api/v1/test/${item.id}/`,config).then(function(response){
                        alert(response.data.output)
                        field.updateSubjectInfo();
                    }
                ).catch(error => this.subjects = {
                    'error': 'Error Occurred'
                })
            },
            submitTestInfo: function(){
                let config = {
                        headers: {
                        'Authorization': 'Bearer ' + this.token
                        }
                    }
                const fields = this
                fields.success = null
                fields.error = null
                console.log(fields.name.value)
                axios.post(`http://localhost:8000/api/v1/test/`, {
                    test: {
                        subject_id: fields.$route.params.id,
                        name: fields.name.value,
                        test_date: fields.test_date.value
                    }
                }, config ).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.name.was_validated = null

                    fields.name.description =  ''

                    fields.name.value =  ''


                    fields.test_date.was_validated = null

                    fields.test_date.description =  ''

                    fields.test_date.value =  ''
                    fields.keyRefresh +=1;
                    fields.updateSubjectInfo();
                    console.log('====SUCCES===')
                }).catch(function(error){
                    if(error.response !== undefined){
                    console.log(error.response)
                    fields.error = error.data.message;
                    if(fields.error.hasOwnProperty('test_date')){
                        fields.test_date.was_validated = false
                        fields.test_date.description = 'Please provide a valid test date'
                    }

                    if(fields.error.hasOwnProperty('name')){
                        fields.name.was_validated = false
                        fields.name.description = 'Please provide a valid name'
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
