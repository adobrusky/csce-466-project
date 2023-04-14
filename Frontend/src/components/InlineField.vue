<template>
<input type="text" class="input" v-model="editedValue" v-if="editable" @change="emit('update:modelValue', editedValue)">
<span v-else>{{ value }}</span>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue'
const emits = defineEmits(["update:modelValue"])

const props = defineProps({
  modelValue: String,
  editable: Boolean
})
let editedValue = ref(props.value)
watch(() => props.value, () => editedValue.value = props.value)

</script>
