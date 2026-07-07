<template>
  <el-dialog
    :model-value="modelValue"
    append-to-body
    align-center
    @update:model-value="emit('update:modelValue', $event)"
  >
    <template #header>
      <div class="dialogHeader">
        <div class="dialogHeaderIcon">
          <el-icon><Setting /></el-icon>
        </div>
        <div class="dialogHeaderTitle">{{ title }}</div>
      </div>
    </template>
    <slot />
  </el-dialog>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  title: string
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
}>()
</script>

<style scoped lang="less">
.dialogHeader {
  margin-bottom: -20px;
  display: flex;
}

.dialogHeaderIcon {
  margin-left: 0;
  font-size: 23px;
  margin-top: 0;
}

.dialogHeaderTitle {
  margin-left: 4px;
  font-size: 20px;
}
</style>
