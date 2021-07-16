<template>
    <div>
        

        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> MyResult  - Average Grade ({{average_grade}}) </h3>
                        
                    </CCardHeader>
                    <CCardBody>
                        <CCol lg="12">
                            <CDataTable :items="test_participants" :fields=table_field
                                        striped
                                        fixed
                                        bordered
                            >
                                
                                <template #header>
                                    <CIcon name="cil-description"/> MyResult
                                </template>
                            </CDataTable>
                        </CCol>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>

        
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
        props: ['test_participant_props'],
        name: 'MyResult',
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
                test_participants: this.test_participant_props,
                average_grade:null,
                table_field: ["teacher_name", "subject_name", "test_name", "grade"
                ],
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
                axios.get('http://localhost:8000/api/v1/test-participant/',config).then(function(response){
                        field.test_participants = response.data.output.results
                        field.average_grade = response.data.output.average_grade
                    }
                ).catch(error => this.test_participants = {
                    'error': 'Error Occurred'
                })
            },
        }
    }
</script>
