<template>
  <CSidebar 
    fixed 
    :minimize="minimize"
    :show="show"
    @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
  >
    <CSidebarBrand class="d-md-down-none" to="/">
      <CIcon 
        class="c-sidebar-brand-full" 
        name="logo" 
        size="custom-size" 
        :height="75"
        viewBox="0 0 556 134"
      />
      <CIcon 
        class="c-sidebar-brand-minimized" 
        name="logo" 
        size="custom-size" 
        :height="35"
        viewBox="0 0 110 134"
      />
    </CSidebarBrand>

    <template v-if="renderComponent"> 
      <CRenderFunction flat :key="keyComponent" :content-to-render="navu"/>
    </template>
    <CSidebarMinimizer
      class="d-md-down-none"
      @click.native="$store.commit('set', ['sidebarMinimize', !minimize])"
    />
  </CSidebar>
</template>

<script>
import sidecard from './_nav'
//$options.
export default {
  name: 'TheSidebar',
  navu: sidecard(),
  computed: {
    show () {
      return this.$store.state.sidebarShow 
    },
    minimize () {
      return this.$store.state.sidebarMinimize 
    }
  },
  mounted: function(){
    const new_navu = sidecard()
    console.log('mounted')
    if(this.navu !== new_navu){
      this.navu = new_navu;
      this.keyComponent +=1;
    }
    this.forceRerender()
  },
  data() {
      return {

        keyComponent: 0,
        renderComponent: false,
      };
    },
    methods: {
      forceRerender() {
        // Remove my-component from the DOM
        this.renderComponent = false;
        console.log('--------------------prited')
        this.$nextTick(() => {
          // Add the component back in
          this.renderComponent = true;
        });
      }
    }
}
</script>
