<template>
  <div>
    <div class="ysArea">
<div id="viz"></div>
      <!-- 攻击区<el-input v-model="gj" label="s">2</el-input>
      倍率区<el-input v-model="bl" label="s">2</el-input>
      增伤区<el-input v-model="zs" label="s">2</el-input>
      爆伤区<el-input v-model="bs" label="s">2</el-input>
      防御区<el-input v-model="fy" label="s">2</el-input>
      抗性区<el-input v-model="kx" label="s">2</el-input>
      暴击率<el-input v-model="bj" label="s">2</el-input>
      最大伤害 - {{ gj * bl * zs * bs * fy * kx}}
      <div>
      </div>      期望 - {{ (gj * bl * zs * (1+bj*(bs-1)) * fy * kx)}} -->
        
    </div>
  </div>
</template>

<script lang="ts" setup>

import NeoVis from "neovis.js/dist/neovis.js";
import { onMounted } from "vue";


0

import {ref} from 'vue'
// let bj = ref(0.369 + 0.15 + 0.15 + 0.20) // 罗莎 双冰 冰套
// let gj = ref(1016 * (1+0.093+0.466 + 0.25 + 0.48 + 0.2 + 0.2)+311+35);//花 攻击沙 风鹰精2 讨龙 千岩 宗室 小公鸡
// let bl =ref(2.021);
// let zs = ref(1.616 + 0.18 + 0.3724);//冰伤杯 冰套 遁地 万叶
// let bs =ref(3.275);
// let fy = ref((90+100)/(90+95+200));
// let kx =ref(1.15);
//该配置实际 24322
//最大值 25071
//期望 22789（冻不住） 25071（冻得住）



// let bj = ref(0.524 + 0.15 + 0.15) // 罗莎 双冰
// let gj = ref(1016 * (1+0.163+0.466 + 0.105 + 0.25 + 0.18 + 0.48 + 0.2 + 0.2)+311+19);//花 攻击沙 头 风鹰精2 追忆2 讨龙 千岩 宗室 小公鸡
// let bl =ref(2.021);
// let zs = ref(1.616  + 0.3724 + 0.2);//冰伤杯 冰套 遁地 万叶 宗室2
// let bs =ref(3.275);
// let fy = ref((90+100)/(90+95+200));
// let kx =ref(1.15);
//该配置实际 28072
//最大值 28136
//期望 24696



</script>
<style>
.ysArea{
  position: absolute;
  left: 270px;
  top: 112px;
  width: 200px;
  height: 200px;
  background:wheat;
}
</style>