<template>
  <TimeSeriesModelView
    model-name="lstm"
    :state="store.state.analyze.lstm"
    :menu-route="store.state.router.page_analyze_lstm"
    load-model-before-mount
    send-training-start-after-state
  />
</template>

<script lang="ts" setup>
import { useStore } from 'vuex';
import TimeSeriesModelView from '@/components/TimeSeriesModelView.vue';

const store = useStore()
</script>
