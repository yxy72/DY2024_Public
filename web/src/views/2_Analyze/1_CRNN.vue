<template>
  <TimeSeriesModelView
    model-name="crnn"
    :state="store.state.analyze.crnn"
    :menu-route="store.state.router.page_analyze_crnn"
  />
</template>

<script lang="ts" setup>
import { useStore } from 'vuex';
import TimeSeriesModelView from '@/components/TimeSeriesModelView.vue';

const store = useStore()
</script>
