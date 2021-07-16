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
        {{ success_message }}
      </CAlert>
      <CAlert
        closeButton
        :show.sync="dismissCountDown"
        show
        color="danger"
        :show="alert_danger"
      >
        <strong>Error Occurred!</strong> {{ error_message }}
        <p>{{ error ? error.message : "" }}</p>
      </CAlert>
      <CCard>
        <CCardHeader>
          <h3>Test Information</h3>
        </CCardHeader>
        <CCardBody>
          <CCardHeader
            >Subject Name: <strong>{{ tests.name }}</strong></CCardHeader
          >
          <CCardBody>
            <p>
              Is Archied: <strong>{{ tests.is_archived }}</strong>
            </p>
            <p>
              Test Date: <strong>{{ tests.test_date }}</strong>
            </p>
            <br />
          </CCardBody>
        </CCardBody>
      </CCard>
    </CCol>
    <CCol sm="24" md="12">
      <CCard>
        <CCardHeader>
          <h3>Tests</h3>
          <CButton
            v-if="tests.is_archived === false"
            color="success"
            @click="myModal = true"
            class="float-right mr-1"
          >
            Insert Pupil Test Result
          </CButton>

          <CButton
            v-if="tests.is_archived === false"
            color="success"
            @click="myFileModal = true"
            class="float-right mr-1"
          >
            CSV Result Upload
          </CButton>
        </CCardHeader>
        <CCardBody>
          <CCol lg="12">
            <CDataTable
              :items="test_participants"
              :fields="table_field"
              striped
              fixed
              bordered
            >
              <template #remove_details="{ item, index }">
                <td class="py-2">
                  <CButton
                    color="danger"
                    square
                    size="sm"
                    @click="deleteTestResult(item, index)"
                  >
                    Remove
                  </CButton>
                </td>
              </template>
              <template #header>
                <CIcon name="cil-description" /> List of Test Result
              </template>
            </CDataTable>
          </CCol>
        </CCardBody>
      </CCard>
    </CCol>
    <CModal
      title="Submit a Student Result"
      :show.sync="myModal"
      size="xl"
      :close-on-backdrop="false"
    >
      <CCol sm="24">
        <CCard>
          <CCardHeader>
            <strong>Test Individual Result Information</strong>
          </CCardHeader>
          <CCardBody>
            <div>
              <CRow>
                <CCol md="12">
                  <CSelect
                    label="Student List"
                    :was-validated="pupil_id.was_validated"
                    :is-valid="pupil_id.was_validated"
                    :description="pupil_id.description"
                    :value.sync="pupil_id.value"
                    placeholder="Select Student"
                    :options="available_students"
                  />
                </CCol>
              </CRow>

              <CRow>
                <CCol md="12">
                  <CInput
                    key="grade"
                    type="number"
                    max="99"
                    min="0"
                    :was-validated="grade.was_validated"
                    :is-valid="grade.was_validated"
                    :description="grade.description"
                    v-model="grade.value"
                    label="Test grade"
                    placeholder="Enter test grade"
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

    <CModal
      title="Batch Result CSV Upload"
      :show.sync="myFileModal"
      size="xl"
      :close-on-backdrop="false"
    >
      <CCol sm="24">
        <CCard>
          <CCardHeader>
            <strong>Test Batch Result Information</strong>
          </CCardHeader>
          <CCardBody>
            <div>
              <CRow>
                <CCol md="12">
                  <CInputFile
                    key="csv_file"
                    ref="myFiles"
                    v-on:change="previewFiles"
                    label="CSV File"
                    placeholder="Select CSV File"
                  />
                </CCol>
              </CRow>
            </div>
          </CCardBody>
        </CCard>
      </CCol>
      <template #footer>
        <CButton @click="myFileModal = false" color="danger">Discard</CButton>
        <CButton @click="submitFileUpload()" color="success">Submit</CButton>
      </template>
    </CModal>
  </CRow>
</template>

<script>
import Vue from "vue";
import VueCookies from "vue-cookies";
import checkAuth from "./_auth";
Vue.use(VueCookies);
import CTableWrapper from "../base/Table.vue";
window.axios = require("axios");
export default {
  props: ["tests_props"],
  name: "Tests",
  components: { CTableWrapper },
  mounted: function () {
    this.updateTestInfo();
    this.availablePupils();
  },
  data: function () {
    return {
      dismissCountDown: 5,
      $refs: {
          myFiles: null,
      },
      token: Vue.$cookies.get("token"),
      show: true,
      alert_success: false,
      alert_danger: false,
      isCollapsed: true,
      keyRefresh: 0,
      tests: this.tests_props,
      test_participants: null,
      table_field: [
        "pupil_name","grade",
        {
          key: "remove_details",
          label: "",
          _style: "width:1%",
          sorter: false,
          filter: false,
        },
      ],
      grade: {
        value: null,
        description: null,
        was_validated: null,
      },

      pupil_id: {
        value: null,
        description: null,
        was_validated: null,
      },
      csv_file: {
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
        success_message:"",
        error_message: "",
      myFileModal: false,
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismiss = dismissCountDown;
    },
    previewFiles() {
        // console.log(ev.target)
        console.log(this.$refs.myFiles)
        // debugger;
      this.csv_file =  this.$refs.myFiles.$data.state[0];
    },
    availablePupils:  function(){
                const field = this
                const token = this.token
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get(`http://localhost:8000/api/v1/test/${field.$route.params.id}/available-pupil/`,config).then(function(response){
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
    updateTestInfo: function () {
      const field = this;
      const token = this.token;
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      axios
        .get(
          `http://localhost:8000/api/v1/test/${field.$route.params.id}/`,
          config
        )
        .then(function (response) {
          field.tests = response.data.output;
          field.test_participants = response.data.output.test_participants;
        })
        .catch(
          (error) =>
            (this.tests = {
              error: "Error Occurred",
            })
        );
    },

    
    redirect_url: function (item, index) {
      console.log(index);
      console.log(item);
      this.$router.push({ path: `/test/details/${item.id}` });
    },
    deleteTestResult: function (item, index) {
      const field = this;
      const token = this.token;
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      axios
        .delete(`http://localhost:8000/api/v1/test-participant/${item.id}/`, config)
        .then(function (response) {
          alert(response.data.output);
          field.updateTestInfo();
          field.availablePupils();
        })
        .catch(
          (error) =>
            (this.tests = {
              error: "Error Occurred",
            })
        );
    },
    submitTestInfo: function () {
      let config = {
        headers: {
          Authorization: "Bearer " + this.token,
        },
      };
      const fields = this;
      fields.success = null;
      fields.error = null;
      console.log(fields.pupil_id.value);
      axios
        .post(
          `http://localhost:8000/api/v1/test-participant/`,
          {
            'test-participant': {
              test_id: fields.$route.params.id,
              pupil_id: fields.pupil_id.value,
              grade: fields.grade.value,
            },
          },
          config
        )
        .then(function (response) {
          fields.success = response.data;
          fields.myModal = false;
          fields.alert_success = true;

          fields.grade.was_validated = null;

          fields.grade.description = "";

          fields.grade.value = "";

          fields.pupil_id.was_validated = null;

          fields.pupil_id.description = "";

          fields.pupil_id.value = "";
          fields.keyRefresh += 1;
          fields.updateTestInfo();
          fields.availablePupils();
          fields.success_message = "Result Submitted Successfully"
        })
        .catch(function (error) {
          if (error.response !== undefined) {
            console.log(error.response);
            fields.error = error.data.message;
            if (fields.error.hasOwnProperty("pupil_id")) {
              fields.pupil_id.was_validated = false;
              fields.pupil_id.description = "Please provide a valid test grade";
            }

            if (fields.error.hasOwnProperty("grade")) {
              fields.grade.was_validated = false;
              fields.grade.description = "Please provide a valid grade";
            }grade
          } else {
            fields.keyRefresh += 1;
            fields.updateTestInfo();
          }
        });
    },


    submitFileUpload: function () {
      let config = {
        headers: {
        'Content-Type': 'multipart/form-data',
          Authorization: "Bearer " + this.token,
        },
      };
      const fields = this;
      fields.success = null;
      fields.error = null;
      console.log(fields.csv_file);
      var form = new FormData()
      form.append('file_upload',fields.csv_file)
      axios
        .put(
          `http://localhost:8000/api/v1/test/${fields.$route.params.id}/result-upload/`,
          form,
          config
        )
        .then(function (response) {
          fields.success = response.data;
          fields.myFileModal = false;
          fields.alert_success = true;

          fields.csv_file.was_validated = null;

          fields.csv_file.description = "";

          fields.csv_file = null;
          fields.keyRefresh += 1;
          fields.updateTestInfo();
          fields.availablePupils();
          fields.success_message = "Result Uploaded Successfully"
        })
        .catch(function (error) {
          if (error.response !== undefined) {
            console.log(error.response);
            fields.error = error.data.message;
            if (fields.error.hasOwnProperty("csv_file")) {
              fields.csv_file.was_validated = false;
              fields.csv_file.description = "Please provide a valid test grade";
            }
          } else {
            fields.keyRefresh += 1;
            fields.updateTestInfo();
          }
          fields.error_message = "Failed to upload test result"
        });
    },
  },
};
</script>
