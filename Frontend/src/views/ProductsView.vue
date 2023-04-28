<template>
  <div class="container">
    <h2 class="title is-2">Products</h2>
    <p class="subtitle is-4">Subtitle</p>
    <br>
    <table class="table">
      <thead>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>
              <input class="input is-small" v-model="edited.name" v-if="edited && edited.id === product.id" />
              <span v-else>{{ product.name }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.price" v-if="edited && edited.id === product.id" />
            <span v-else>{{ product.price }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>

import { ref, onBeforeMount, computed } from 'vue'
import InlineField from '@/components/InlineField.vue';
import { copyObject } from '@/js/util.js'

let products = ref()
let searchQuery = ref()
let edited = ref()

async function getProducts() {
  const response = await fetch("/api/inventory")
  if(response.ok) {
    const json = await response.json()
    products.value = json
  }
}

async function saveEdit() {
  for(let product of products.value) {
    if(product.id === edited.value.id) {
      const response = await fetch(`/api/inventory`, {
        headers: {"Content-Type": "application/json"},
        method: 'POST',
        body: JSON.stringify(edited.value)
      })
      if(response.ok) {
        copyObject(edited.value, product)
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

async function deleteEdit() {
  for(let product of products.value) {
    if(product.id === edited.value.id) {
      const response = await fetch(`/api/inventory/${edited.value.id}`, {
        method: 'DELETE'
      })
      if(response.ok) {
        await getProducts()
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

async function createProduct() {
  const response = await fetch(`/api/inventory`, {
    headers: {"Content-Type": "application/json"},
    method: 'POST',
    body: JSON.stringify(created.value)
  })
  if(response.ok) {
    await getProducts()
  } else {
    alert(response.statusText)
  }
  created.value = undefined
}

onBeforeMount(() => {
  getProducts()
})

</script>
