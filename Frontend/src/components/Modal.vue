<template>
  <div :class="['modal',{'is-active': active}]">
    <div class="modal-background"></div>
    <slot></slot>
    <button v-if="closable" class="modal-close is-large" aria-label="close" @click="close"></button>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount } from 'vue'
const emit = defineEmits(["close"])
const props = defineProps({
  active: Boolean,
  closable: Boolean
})
onBeforeMount(() => {
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;
    if(e.key == "Escape") {
      close()
    }
  });
})
function close() {
  emit("close")
}
</script>
