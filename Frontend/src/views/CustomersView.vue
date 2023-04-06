<template>
  <div class="container">
    <h2 class="title is-2">Customers</h2>
    <p class="subtitle is-4">Subtitle</p>
    <br>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <td colspan="3">
            <input type="text" placeholder="Search customer" class="input" v-model="searchQuery" />
          </td>
          <td colspan="5"></td>
        </tr>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Address</th>
          <th>City</th>
          <th>State</th>
          <th>Country</th>
          <th>Postal</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in filteredCustomers" :key="customer.id">
          <td>{{ customer.id }}</td>
          <td>{{ customer.first_name }} {{ customer.last_name }}</td>
          <td>{{ customer.address }}</td>
          <td>{{ customer.city }}</td>
          <td>{{ customer.state }}</td>
          <td>{{ customer.country }}</td>
          <td>{{ customer.postal_code }}</td>
          <td>{{ customer.email }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>

  <script setup>
  import { ref, onBeforeMount, computed } from 'vue'

  let customers = ref()
  let searchQuery = ref()

  async function getCustomers() {
    const response = await fetch("/api/customers")
    if(response.ok) {
      const json = await response.json()
      customers.value = json
    }
  }

  const filteredCustomers = computed(() => {
    const query = searchQuery.value?.toLowerCase()
    if(!query) return customers.value || []
    return customers.value.filter(customer => {
      return customer.first_name?.toLowerCase().includes(query)
        || customer.last_name?.toLowerCase().includes(query)
        || customer.email?.toLowerCase().includes(query)
        || customer.address?.toLowerCase().includes(query)
    })
  })

  onBeforeMount(() => {
    getCustomers()
  })

  </script>
