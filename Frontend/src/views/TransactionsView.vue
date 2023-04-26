<template>
  <div class="container">
    <h2 class="title is-2">Transactions</h2>
    <p class="subtitle is-4">Subtitle</p>
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
          <th>Customer Id</th>
          <th>Date</th>
          <th>Product</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="transaction in filteredTransactions" :key="transaction.id">
          <tr>
            <td>{{ transaction.id }}</td>
            <td>
              <input class="input is-small" v-model="edited.first_name" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.first_name }}</span>
              <input class="input is-small" v-model="edited.last_name" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.last_name }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.address" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.address }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.city" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.city }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.state" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.state }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.country" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.country }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.postal_code" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.postal_code }}</span>
            </td>
            <td>
              <input class="input is-small" v-model="edited.email" v-if="edited && edited.id === customer.id" />
              <span v-else>{{ transaction.email }}</span>
            </td>
            <td>
              <div class="buttons" v-if="edited && edited.id == customer.id">
                <a class="button is-small is-success" @click="saveEdit">Save</a>
                <a class="button is-small" @click="edited = undefined">Cancel</a>
              </div>
              <a class="button is-small" v-else @click="startEdit(customer)">Edit</a>
            </td>
          </tr>
          <tr>
            <table class="table">
              <thead>
                <tr>
                  <th>Product Id</th>
                  <th>Quanity</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in transaction.orders" :key="order.id">
                  <td>{{ order.product_id }}</td>
                  <td>{{ order.quantity }}</td>
                </tr>
              </tbody>
            </table>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
  </template>