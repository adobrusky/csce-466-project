<template>
  <div class="container">
    <h2 class="title is-2">Products</h2>
    <p class="subtitle is-4">Subtitle</p>
    <br>
    <table class="table">
      <thead>
        <tr>
          <td colspan="3">
              <input type="text" placeholder="Search product" class="input" v-model="searchQuery" />
          </td>
          <td colspan="6"></td>
        </tr>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Price</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.id">
          <td>{{ product.id }}</td>
          <td>
              <input class="input is-small" v-model="edited.name" v-if="edited && edited.id === product.id" />
              <span v-else>{{ product.name }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.price" v-if="edited && edited.id === product.id" />
            <span v-else>{{ product.price }}</span>
          </td>
          <td>
            <div class="buttons" v-if="edited && edited.id == product.id">
              <a class="button is-small is-success" @click="saveEdit">Save</a>
              <a class="button is-small is-danger" @click="deleteEdit">Delete</a>
              <a class="button is-small" @click="edited = undefined">Cancel</a>
            </div>
            <a class="button is-small" v-else @click="startEdit(product)">Edit</a>
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
  if(!confirm("Are you sure you want to delete this product?")) return

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


function startEdit(product) {
  edited.value = {
    ...product
  }
}

const filteredProducts = computed(() => {
  const query = searchQuery.value?.toLowerCase()
  if(!query) return products.value || []
  return products.value.filter(product => {
    return product.id?.toLowerCase().includes(query)
      || product.name?.toLowerCase().includes(query)
      || product.price?.toLowerCase().includes(query)
  })
})

onBeforeMount(() => {
  getProducts()
})

</script>
