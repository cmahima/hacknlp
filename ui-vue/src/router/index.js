import Vue from 'vue'
import VueRouter from 'vue-router'
import PatientPage from '@/pages/patient/PatientPage.vue';
import PatientTable from '@/pages/patient/components/PatientTable.vue';

Vue.use(VueRouter)

const routes = [
    {
        path: '/patient',
        component: PatientPage,
        children: [
            {
                path: '',
                name: 'PatientTable',
                component: PatientTable
            },
            {
                path: ':id',
                name: 'PatientDetail',
                props: ({params}) => ({...params, ...{id: parseInt(params.id, 10)}}),
                component: () => import(/* webpackChunkName: "patient-detail" */ '../pages/patient/components/PatientDetail.vue')
            },
            {path: '*', redirect: '/patient'}
        ]
    },
    {
        path: '/iris-example',
        name: 'Iris',
        // route level code-splitting
        // this generates a separate chunk (iris-example.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "iris-example" */ '../pages/iris-example/IrisExample.vue')
    },
    {
        path: '/summary',
        name: 'Summary',
        // route level code-splitting
        // this generates a separate chunk (iris-example.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "iris-example" */ '../pages/summary/summaryExample.vue')
    },
    {
        path: '/home',
        name: 'HomePage',
        // route level code-splitting
        // this generates a separate chunk (home.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '../pages/home/Home.vue')
    },
    {path: '*', redirect: '/patient'}

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
