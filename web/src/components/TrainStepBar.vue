<template>
  <div class="bottomArea">
    <div class="step">
      <el-steps
        :active="active"
        finish-status="success"
        simple>
        <el-step
          v-for="title in steps"
          :key="title"
          :title="title" />
      </el-steps>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  active: {
    type: Number,
    default: 0,
  },
})

const steps = [
  "导入数据",
  "预处理",
  "选择网络",
  "训练模型",
  "完成",
]
</script>

<style scoped lang="less">
.bottomArea{
  width:calc(100% - 220px - 100px - 0px);
  overflow: hidden;
  height: 46px;

  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 8px;
  padding-right: 8px;

  position: absolute;
  bottom: 42px;
  left: calc(220px + 50px - 8px);
  max-width: 1600px;
  align-items: center;
  // background: #509bfe2d;

  .step{
    height: 46px;
    min-width: 810px;
    // background: red;
    box-shadow: 0px 0px 8px 0px rgba(109, 109, 109, 0.205);
  }
}
</style>
