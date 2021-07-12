<template>
    <div>
        <CAlert
                :show.sync="dismissCountDown"
                closeButton
                color="success"
                fade
                :show="alert_success"
        >
            Class Information Created Successfully
        </CAlert>
        <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
            <strong>Error Occurred!</strong> When Creating Class Information.
            <p>{{ error ? error.message : ""}}</p>
        </CAlert>
        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> Classes </h3>
                        <CButton color="success" @click="myModal = true" class="float-right mr-1">
                            Insert a new Class
                        </CButton>
                    </CCardHeader>
                    <CCardBody>
                        <CCol lg="12">
                            <CDataTable :items="classes" :fields=table_field
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
                                                @click="deleteClass(item, index)"
                                        >
                                            Remove/Archive
                                        </CButton>
                                    </td>
                                </template>
                                <template #header>
                                    <CIcon name="cil-description"/> List of Classes

                                </template>
                            </CDataTable>
                        </CCol>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>
        <CModal
                title="Create a new Class"
                :show.sync="myModal"
                size="xl"
                :close-on-backdrop="false"
        >
            <CCol sm="24">
                <CCard>
                    <CCardHeader>
                        <strong>Class Information</strong>
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
                                            label="Name"
                                            placeholder="Enter name"
                                    />
                                </CCol>
                            </CRow>

                        </div>

                    </CCardBody>
                </CCard>
            </CCol>
            <template #footer>
                <CButton @click="myModal = false" color="danger">Discard</CButton>
                <CButton @click="submitClassInfo()" color="success">Submit</CButton>
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
        props: ['class_props'],
        name: 'Classes',
        components: { CTableWrapper },
        mounted: function(){
            this.updateTableData();
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
                classes: this.class_props,
                table_field: ["name", "is_archived", "unique_name", {
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
                axios.get('http://localhost:8000/api/v1/class/',config).then(function(response){
                        field.classes = response.data.output
                        console.log(response.data.output)
                    }
                ).catch(error => this.classes = {
                    'error': 'Error Occurred'
                })
            },
            deleteUser: function(item, index){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.delete(`http://localhost:8000/api/v1/class/${item.id}`,config).then(function(response){
                        alert('User deleted Successfully!')
                        field.updateTableData();
                    }
                ).catch(error => this.classes = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `details/${item.id}`})
            },
            submitClassInfo: function(){
                let config = {
                        headers: {
                        'Authorization': 'Bearer ' + this.token
                        }
                    }
                const fields = this
                fields.success = null
                fields.error = null
                
                axios.post('http://localhost:8000/api/v1/class/', {
                    class: {
                        name: fields.name.value

                    }
                }, config ).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.name.was_validated = null

                    fields.name.description =  ''

                    fields.name.value =  ''
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
