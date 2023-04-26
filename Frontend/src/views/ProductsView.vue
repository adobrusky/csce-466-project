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
import { ref, onBeforeMount } from 'vue'

let products = ref()

async function getProducts() {
  const response = await fetch("/api/inventory")
  if(response.ok) {
    const json = await response.json()
    products.value = json
  }
}

onBeforeMount(() => {
  getProducts()
})

</script>
