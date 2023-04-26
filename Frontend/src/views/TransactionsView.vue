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
              <input class="input is-small" v-model="edited.date" v-if="edited && edited.id === transaction.id" />
              <span v-else>{{ transaction.first_name }}</span>
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

<script>
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
    body: JSON.stringify(created.value)
  })
  if(response.ok) {
    await getTransactions()
  } else {
    alert(response.statusText)
  }
  created.value = undefined
}

async function getTransactions() {
  const response = await fetch("/api/orders")
  if(response.ok) {
    const json = await response.json()
    transactions.value = json
  }
}
</script>