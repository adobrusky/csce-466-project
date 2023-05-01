<template>
  <div class="container">
    <h2 class="title is-2">Transactions</h2>
    <p class="subtitle is-4">Viewing {{  transactions.length }} transactions</p>
    <br>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <td colspan="3">
            <input type="text" placeholder="Search transaction" class="input" v-model="searchQuery" />
          </td>
          <td colspan="6"></td>
        </tr>
        <tr>
          <th>Id</th>
          <th>Customer Id</th>
          <th>Date</th>
          <th>Product ID</th>
          <th>Quanity</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td></td>
          <td>
            <input class="input is-small" v-model="newTransact.customer_id" />
          </td>
          <td>
            {{ newTransact.date }}
          </td>
          <td>
            <input class="input is-small" v-model="newOrder.inventory_id" />
          </td>
          <td>
            <input class="input is-small" v-model="newOrder.quantity" />
          </td>
          <td>
            <div class="buttons">
              <a class="button is-small" @click="addProduct" :disabled="canAdd?undefined:true">Add Product</a>
              <a class="button is-small is-success" @click="createTransaction" :disabled="canSave?undefined:true">Create</a>
              <a class="button is-small" @click="reset">Cancel</a>
            </div>
          </td>
        </tr>
        <tr v-for="(order, i) in newTransact.inventory" :key="i">
          <td></td>
            <td></td>
            <td></td>
            <td>
              <input class="input is-small" v-model="newTransact.inventory[i].inventory_id" />
            </td>
            <td>
              <input class="input is-small" v-model="newTransact.inventory[i].quantity" />
            </td>
        </tr>
        <!-- eslint-disable vue/no-v-for-template-key : valid for vue3 -->
        <template v-for="transaction of transactions" :key="transaction.id">
          <tr>
            <td>{{ transaction.id }}</td>
            <td>
              <input class="input is-small" v-model="edited.customer_id" v-if="edited && edited.id === transaction.id" />
              <span v-else>{{ transaction.customer_id }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.date" v-if="edited && edited.id === transaction.id" />
              <span v-else>{{ transaction.date }}</span>
            </td>
            <td>

            </td>
            <td>

            </td>
            <td>
              <div class="buttons" v-if="edited && edited.id == transaction.id">
                <a class="button is-small is-success" @click="saveEdit">Save</a>
                <a class="button is-small is-danger" @click="deleteEdit">Delete</a>
                <a class="button is-small" @click="edited = undefined">Cancel</a>
              </div>
              <a class="button is-small" v-else @click="startEdit(transaction)">Edit</a>
            </td>
          </tr>
          <tr v-for="(order, i) in transaction.inventory" :key="order.id">
            <td></td>
            <td></td>
            <td></td>
            <td>
              <input class="input is-small" v-model="edited.inventory[i].inventory_id" v-if="edited && edited.id === transaction.id" />
              <span v-else>{{ order.inventory_id }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.inventory[i].quantity" v-if="edited && edited.id === transaction.id" />
              <span v-else>{{ order.quantity }}</span>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script setup>

import { ref, onBeforeMount, computed } from 'vue'
import { copyObject, hasValues } from '@/js/util.js'

let transactions = ref([])
let searchQuery = ref()
let edited = ref()
let newTransact = ref({
  inventory: []
})
let newOrder = ref({})

const canSave = computed(() => {
  return hasValues(newTransact.value, ["customer_id"])
})
const canAdd = computed(() => {
  return hasValues(newOrder.value, ["inventory_id", "quantity"])
})

function reset() {
  newTransact.value = {
    inventory: [],
    date: new Date().toISOString().substring(0, 10)
  }
}
function addProduct() {
  newTransact.value.inventory.push(newOrder.value)
  newOrder.value = {}
}
reset()


async function saveEdit() {
  for(let transaction of transactions.value) {
    if(transaction.id === edited.value.id) {
      const response = await fetch(`/api/orders`, {
        headers: {"Content-Type": "application/json"},
        method: 'POST',
        body: JSON.stringify(edited.value)
      })
      if(response.ok) {
        copyObject(edited.value, transaction)
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

async function deleteEdit() {
  if(!confirm("Are you sure you want to delete this transaction?")) return
  for(let transaction of transactions.value) {
    if(transaction.id === edited.value.id) {
      const response = await fetch(`/api/orders/${edited.value.id}`, {
        method: 'DELETE'
      })
      if(response.ok) {
        await getTransactions()
      } else {
        alert(response.statusText)
      }
      break;
    }
  }
  edited.value = undefined
}

async function createTransaction() {
  const response = await fetch(`/api/orders`, {
    headers: {"Content-Type": "application/json"},
    method: 'POST',
    body: JSON.stringify(newTransact.value)
  })
  if(response.ok) {
    await getTransactions()
    reset()
  } else {
    alert(response.statusText)
  }
}

async function getTransactions() {
  const response = await fetch("/api/orders")
  if(response.ok) {
    const json = await response.json()
    transactions.value = json
  }
}

function startEdit(order) {
  edited.value = {
    ...order
  }
}

onBeforeMount(() => {
  getTransactions()
})
</script>
