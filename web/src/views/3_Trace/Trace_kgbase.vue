<template>
    <div class="Page">
        <div class="PagePanel">
            <div class="PagePanel_name1">
                知识库
            </div>
            <div class="PagePanel_name2">
            </div>
            <div class="PagePanel_name3">
            </div>
            <div class="PagePanel_name4">
            </div>
        </div>
    </div>
</template>

<script>
import {reactive} from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from "vue-router"
import { useStore } from 'vuex'
import { onMounted } from '@vue/runtime-core'


export default {
    name:'',
    setup(){
        

            const pd = reactive(new Object())
            const $router = useRouter()
            const store = useStore();

            onMounted(()=>{
                //     console.log(networkData)
            });
            function test(){
                pd;
                ElMessage('load')
                $router.replace({
                    // path:'/Predict/Train/network'
                })
            }
        return{
            store,test
        }
    }
}
</script>

<style scoped>
html,body,#app{
 height: 100%;/* precious */
}*{
    margin: 0;
    padding: 0;
}
.Page{
    width: 100%;
    height: 100%;
    background: rgba(255, 0, 0, 0.064);
}
.PagePanel{
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-areas:
  'p1 p2'
  'p3 p4';
  grid-template-columns: 50% 50%;
  grid-template-rows: 50% 50%;
  /* grid-column-gap: 5px;
  grid-row-gap: 5px; */
  overflow: hidden;

}
.PagePanel_name1{
    grid-area: p1;
    background: rgba(255, 0, 0, 0.03);
}
.PagePanel_name2{
    grid-area: p2;
    background: rgba(161, 161, 255, 0.053);
}
.PagePanel_name3{
    grid-area: p3;
    background: rgba(153, 205, 50, 0.094);

}
.PagePanel_name4{
    grid-area: p4;

    background: rgba(210, 180, 140, 0.064);
}
.iconfont{
    font-family:"iconfont" !important;
    font-size:14px;
    font-style:normal;
    font-weight:100;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
    
}
</style>