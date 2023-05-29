<template>
  <main class="main">
    <header class="headernotif">
      <button class="notification-button" :class="{ 'has-notifications': notifications.length > 0 }" @click="toggleNotificationBox">{{ showNotificationBox ? 'Fechar' : 'Notificações' }}</button>
    </header>
    <div class="notification-box" v-show="showNotificationBox">
      <h3>Notificações</h3>
      <ul>
        <li v-for="notification in notifications" :key="notification" class="notif">{{ notification }}</li>
      </ul>
    </div>
    <div class="row">
      <div class="columnleft">
        <h2>Regras</h2>
        <p>
          - 5 dias com o livro
          - 1 mês de suspensão
        </p>
      </div>
      <div id="monitorias-disponiveis" class="columnright">
        <h1>Minhas Reservas</h1>

        <table class="table table-hover">
          <thead>
            <tr>
              <th>Título</th>
              <th>Data</th>
              <th>Data Devolução</th>
              <th>QR Code</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book._id">
              <td>{{ book.title }}</td>
              <td>{{ book.date }}</td>
              <td>{{ book.return }}</td>
              <td>
                <img :src="book.qrcodeImage" alt="QR Code" />
              </td>
            </tr>
          </tbody>
        </table>
        <p class=paragrafo v-if="isReservationFull()">Limite máximo de reservas atingido</p>
      </div>
    </div>
    <div class="todoslivros">
      <h2>Livros</h2>
      <div class="search-bar">
        <input class="barra" type="text" v-model="searchTerm" placeholder="Pesquisar livros" />
      </div>
      <ul>
        <li v-for="book in filteredBooks" :key="book._id">
          <div class="monitoria-title">
            {{ book.title }}
            <br>
            {{ book.author }}
            <br>
            <img :src="book.image"  class="capa" />
            <br>
            <br>
            <button @click="showDetails(book)">Detalhes</button>
          </div>
          <div v-if="bookDetails && bookDetails._id === book._id" class="edit">
            <h3>Detalhes</h3>
            <div class="monitoria-title">
              {{ bookDetails.title }}
              <br>
              {{ bookDetails.description }}
              <br>
              {{ bookDetails.user_id }}
            </div>
            <template v-if="!bookDetails.user_id && !isReservationFull() && isReturnDatePassed(book)">
              <button @click="reserveBook()">Reservar</button>
            </template>
            <template v-else>
              <button disabled class="reserved-button">Reservar</button>
            </template>
            <button type="button" @click="bookDetails = null">Fechar</button>
          </div>
        </li>
      </ul>
    </div>
  </main>
</template>

<script>
import { getMonitorias, updateMonitoria, getAllMonitorias } from "../api";
import QRCode from "qrcode";

export default {
  data() {
    return {
      books: [],
      allBooks: [],
      title: "",
      date: "",
      return: "",
      description: "",
      bookDetails: null,
      userId: null,
      qrcodeImage: null,
      notifications: [], // Array to store notifications
      showNotificationBox: false, 
      searchTerm: "",
    };
  },
  methods: {
    async loadUserMonitorias(userId) {
      this.userId = userId;
      this.books = await getMonitorias(userId);
      this.showNotifications();
    },
    async loadAllMonitorias() {
      this.allBooks = await getAllMonitorias();
    },
    showDetails(book) {
      this.bookDetails = book;
    },
    async reserveBook() {
      if (!this.bookDetails.user_id) {
        this.bookDetails.user_id = this.userId;

        // Add today's date to bookDetails.date
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        this.bookDetails.date = `${year}-${month}-${day}`;

        //Add today's date + 5 days
        const returnDate = new Date();
        returnDate.setDate(returnDate.getDate() + 5);
        const returnYear = returnDate.getFullYear();
        const returnMonth = String(returnDate.getMonth() + 1).padStart(2, '0');
        const returnDay = String(returnDate.getDate()).padStart(2, '0');
        this.bookDetails.return = `${returnYear}-${returnMonth}-${returnDay}`;

        // Add new QRCode
        const qrCodeData = JSON.stringify(this.bookDetails.user_id, this.bookDetails.isbn,this.bookDetails.date);
        this.bookDetails.qrcodeImage = await QRCode.toDataURL(qrCodeData);

        await updateMonitoria(this.bookDetails._id, this.bookDetails);
        this.bookDetails = null;
        this.loadUserMonitorias(this.userId);
      }
    },
    isReservationFull() {
      return this.books.length >= 3;
    },
    toggleNotificationBox() {
      this.showNotificationBox = !this.showNotificationBox;
    },
    showNotifications() {
      // Clear existing notifications
      this.notifications = [];

      // Get the current date
      const currentDate = new Date();

      // Loop through the books and check if any have a return date in two days
      this.books.forEach((book) => {
        const returnDate = new Date(book.return);
        if (returnDate <= currentDate) {
        this.notifications.push(`Book '${book.title}' has a return date that has passed.`);
      } else {
        const timeDifference = returnDate.getTime() - currentDate.getTime();
        const daysDifference = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));

        if (daysDifference <= 2) {
          this.notifications.push(`Book '${book.title}' has a return date in ${daysDifference} days.`);
        }
      }
      });
      this.notifications.forEach((notification) => {
        console.log(notification);
      });
    },
    isReturnDatePassed(book) {
      if (book.user_id === this.user_id) {
        const currentDate = new Date();
        return new Date(book.return) <= currentDate;
      }
      return true
    }   
  },
  created() {
    this.showNotifications(); // Call the method when the component is created
  },
    computed: {
      filteredBooks() {
        const searchTerm = this.searchTerm.toLowerCase();
        return this.allBooks.filter(
          (book) =>
            book.title.toLowerCase().includes(searchTerm) ||
            book.author.toLowerCase().includes(searchTerm) ||
            book.isbn.toLowerCase().includes(searchTerm)
        );
      },
    },
};
</script>
  
<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
header{
  background-color: #D1FAFF;
  padding: 1rem;
  text-align: center;
}

div {
  display: flex;
  flex-direction: column;
  align-items: left;
  padding: 0.2rem; 
  font-family:monospace;
  width: 100%;
}

h1, h2, h3 {
  color: #1F271B;
  margin-bottom: 1rem;
  font-family:monospace;
}

.notification-button{
  font-family: monospace;
  font-style: bold;
  width: 10%;
  padding: 0.5rem;
  margin: 0.5rem;
  background-color: #0B4F6C;
  color: #D1FAFF;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.notification-button:hover {
  background-color: #A9D3FF;
  color: #1F271B;
}
button{
  font-family: monospace;
  font-style: bold;
  width: 80%;
  padding: 0.5rem;
  margin: 0.5rem;
  background-color: #0B4F6C;
  color: #D1FAFF;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #D1FAFF;
    color: #1F271B;
}

.reserved-button {
  background-color: #847577;
  cursor: default;
}

.reserved-button:hover {
  background-color: #847577;
  color: #D1FAFF;
}

ul {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 0;
  justify-content: start;
  align-items: flex-start;
  width: 100%;
  gap: 4rem;
}

li {
  display: flex;
  flex-direction:row;
  background-color: #A9D3FF;
  padding: 0px;
  border-radius: 5px;
  margin-bottom: 1px;
  flex-basis: 16%; 
}

.monitoria-title {
  margin-bottom: 0.1rem;
  align-items: center;
  text-align: center;
}

.actions {
  display: flex;   
  flex-direction: row;  
  justify-content: center;
  gap: 0.5rem;  
}

li:nth-child(3n) {
  margin-right: 0;
}

li:nth-child(odd) {
  background-color: #A9D3FF;
}

.row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

.columnleft {
  flex: 1;
  justify-content: center;
}

.columnright {
  flex: 1;
  justify-content: center;
}

.edit {  
  align-items: center;
}

table {
  margin-top: 2rem;
  margin-right: 2rem;
  background-color: #A9D3FF;
  border-radius: 5px;
  padding: 2rem;
}

th {
  background-color: #0B4F6C;
  color: #D1FAFF;
  text-transform: capitalize;
  border-radius: 5px;
}

.capa {
  width: 10rem;
  margin: 0.5rem;
}

.has-notifications {
  background-color: red;
}

.notification-box {
  position: absolute;
  top: 19.5rem;
  right: 20px;
  width: 200px;
  background-color: #A9D3FF;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notification-box h3 {
  margin: 0 0 10px;
}

.notification-box ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notification-box li {
  margin-bottom: 5px;
}

.notif {
  flex-basis: 100%;
}

.headernotif {
  justify-content: right;
}

.todoslivros {
  margin-left: 2rem;
}

.search-bar{
  padding-right: 5rem;
  padding-bottom: 3rem;
  height: 2rem;
}

</style>

