<template>
  <div class="c-app" :key="componentKey">
    <TheSidebar  :key="componentKey"  v-bind:userObject="componentKey" />
    <CWrapper>
      <TheHeader/>
      <div class="c-body">
        <main class="c-main">
          <CContainer fluid>
            <transition name="fade">
              <router-view></router-view>
            </transition>
          </CContainer>
        </main>
      </div>
      <TheFooter/>
    </CWrapper>
  </div>
</template>

<script>
import TheSidebar from './TheSidebar'
import TheHeader from './TheHeader'
import TheFooter from './TheFooter'
import Vue from 'vue';
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)

export default {
  name: 'TheContainer',
  components: {
    TheSidebar,
    TheHeader,
    TheFooter
  },
  data() {
    return {
      componentKey: "0",
    };
  },
  mounted: function(){
    this.forceRerender();
  },
  methods: {
    forceRerender() {
      const is_superuser = Vue.$cookies.get('is_superuser')
      const is_teacher = Vue.$cookies.get('is_teacher')
      const is_student = Vue.$cookies.get('is_student')
      console.log(Vue.$cookies.get('is_superuser'))
      console.log(typeof(is_superuser))
      if(is_superuser === "true"){
        this.componentKey = "admin"
      }
      else if(is_teacher === "true"){
        this.componentKey = "teacher"
      }

      else if(is_student === "true"){
        this.componentKey = "is_student"
      }
      else {
        this.$router.push({ path: `/auth/login`})
      }
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
