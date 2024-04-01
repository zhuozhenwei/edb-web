import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/views/Main'
import Details from '@/views/Details'
import Upload from '@/views/Upload'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main,
    },
    {
      path: '/details',
      name: 'Details',
      component: Details,
      props: (route) => ({ item: route.params.item }),
    },
    {
      path: '/upload',
      name: 'Upload',
      component: Upload,
      props: (route) => ({ item: route.params.item }),
    },
  ]
})
