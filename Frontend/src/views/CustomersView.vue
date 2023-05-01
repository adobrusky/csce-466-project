<template>
  <div class="container">
    <h2 class="title is-2">Customers</h2>
    <p class="subtitle is-4">Viewing {{  customers.length }} customers</p>
    <br>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <td colspan="3">
              <input type="text" placeholder="Search customer" class="input" v-model="searchQuery" />
          </td>
          <td colspan="6"></td>
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
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td></td>
          <td>
            <input class="input is-small" v-model="newCustomer.first_name"/>
            <input class="input is-small" v-model="newCustomer.last_name"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.address"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.city"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.state"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.country"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.postal_code"/>
          </td>
          <td>
            <input class="input is-small" v-model="newCustomer.email"/>
          </td>
          <td>
            <div class="buttons">
              <a class="button is-small is-success" @click="createCustomer" :disabled="canSave?undefined:true">Create</a>
              <a class="button is-small" @click="newCustomer = {}">Cancel</a>
            </div>
          </td>
        </tr>
        <tr v-for="customer in filteredCustomers" :key="customer.id">
          <td>{{ customer.id }}</td>
          <td>
            <input class="input is-small" v-model="edited.first_name" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.first_name }}</span>
            <input class="input is-small" v-model="edited.last_name" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.last_name }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.address" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.address }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.city" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.city }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.state" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.state }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.country" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.country }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.postal_code" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.postal_code }}</span>
          </td>
          <td>
            <input class="input is-small" v-model="edited.email" v-if="edited && edited.id === customer.id" />
            <span v-else>{{ customer.email }}</span>
          </td>
          <td>
            <div class="buttons" v-if="edited && edited.id == customer.id">
              <a class="button is-small is-success" @click="saveEdit">Save</a>
              <a class="button is-small is-danger" @click="deleteEdit">Delete</a>
              <a class="button is-small" @click="edited = undefined">Cancel</a>
            </div>
            <a class="button is-small" v-else @click="startEdit(customer)">Edit</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>

<script setup>

import { ref, onBeforeMount, computed } from 'vue'
import { copyObject, hasValues } from '@/js/util.js'

let customers = ref([])
let searchQuery = ref()
let edited = ref()
let newCustomer = ref({})

function startEdit(customer) {
  edited.value = {
    ...customer
  }
}

async function saveEdit() {
  for(let customer of customers.value) {
    if(customer.id === edited.value.id) {
      const response = await fetch(`/api/customers`, {
        headers: {"Content-Type": "application/json"},
        method: 'POST',
        body: JSON.stringify(edited.value)
      })
      if(response.ok) {
        copyObject(edited.value, customer)
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

async function deleteEdit() {
  if(!confirm("Are you sure you want to delete this customer?")) return
  for(let customer of customers.value) {
    if(customer.id === edited.value.id) {
      const response = await fetch(`/api/customers/${edited.value.id}`, {
        method: 'DELETE'
      })
      if(response.ok) {
        await getCustomers()
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

const canSave = computed(() => {
  return hasValues(newCustomer.value, ["first_name", "last_name", "address", "email", "city", "state", "country", "postal_code"])
})

async function createCustomer() {
  const response = await fetch(`/api/customers`, {
    headers: {"Content-Type": "application/json"},
    method: 'POST',
    body: JSON.stringify(newCustomer.value)
  })
  if(response.ok) {
    await getCustomers()
    newCustomer.value = {}
  } else {
    alert(response.statusText)
  }
}

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
