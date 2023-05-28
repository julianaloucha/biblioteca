<template>
  <main class="main">
    <header>botões edit user {{ userId }}</header>
    <div class="row">
      <div class="columnleft">
        <h2>Todos os livros</h2>
        <ul>
          <li v-for="book in allBooks" :key="book._id">
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
                {{ bookDetails.date }}
                <br>
                {{ bookDetails.time }}
                <br>
                {{ bookDetails.description }}
                <br>
                {{ bookDetails.user_id }}
              </div>
              <template v-if="!bookDetails.user_id && !isReservationFull()">
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
      <div id="monitorias-disponiveis" class="columnright">
        <h1>Minhas Reservas</h1>

        <table class="table table-hover">
          <thead>
            <tr>
              <th>Título</th>
              <th>Data</th>
              <th>Horário</th>
              <th>QR Code</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book._id">
              <td>{{ book.title }}</td>
              <td>{{ book.date }}</td>
              <td>{{ book.time }}</td>
              <td>
                <img :src="book.qrcodeImage" alt="QR Code" />
              </td>
            </tr>
          </tbody>
        </table>
        <p class=paragrafo v-if="isReservationFull()">Limite máximo de reservas atingido</p>
      </div>
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
      time: "",
      description: "",
      bookDetails: null,
      userId: null,
      qrcodeImage: null,
    };
  },
  methods: {
    async loadUserMonitorias(userId) {
      this.userId = userId;
      this.books = await getMonitorias(userId);
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

        // Add current time to bookDetails.time
        const hours = String(today.getHours()).padStart(2, '0');
        const minutes = String(today.getMinutes()).padStart(2, '0');
        this.bookDetails.time = `${hours}:${minutes}`;

        // Add new QRCode
        const qrCodeData = JSON.stringify(this.bookDetails.user_id, this.bookDetails.isbn,this.bookDetails.date);
        this.bookDetails.qrcodeImage = await QRCode.toDataURL(qrCodeData);
        console.log("is this working?" + this.bookDetails.user_id)

        await updateMonitoria(this.bookDetails._id, this.bookDetails);
        this.bookDetails = null;
        this.loadUserMonitorias(this.userId);
      }
    },
    isReservationFull() {
      return this.books.length >= 3;
    },
  },
};
</script>
  
<style scoped>
* {
  box-sizing: border-box;
}

div {
  display: flex;
  flex-direction: column;
  align-items: left;
  padding: 0.2rem; 
  font-family: Arial, sans-serif;
  width: 100%;
}

h2, h3 {
  color: #333;
  margin-bottom: 1rem;
}

form {
  display: flex;
  flex-direction: column;
  width: 75%;
  margin-bottom: 1rem;
}

input {
  flex-grow: 1;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border: none;
  border-radius: 5px;
}

input {
  flex-grow: 1;
  padding: 0.5rem 0.5rem;
  margin-bottom: 0.5rem;
  border: 3px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #103c5c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0.5rem;
}

button:hover {
  background-color: #14181d;
  color: white;
  cursor: pointer;
}

.reserved-button {
  background-color: #ccc;
  cursor: default;
}

.reserved-button:hover {
  background-color: #ccc;
}

ul {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 0;
  justify-content: start;
  align-items: flex-start;
  width: 100%;
  gap: 1rem;
}

li {
  display: flex;
  flex-direction:row;
  background-color: #f0f0f0;
  padding: 0px;
  border-radius: 5px;
  margin-bottom: 1px;
  flex-basis: 40%; 
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
  background-color: #e6e6e6;
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
}

th {
  background-color: #103c5c;
  color: white;
  text-transform: capitalize;
}

.paragrafo{
  color: red;
  font-weight: bold;
  margin-top: 1rem;
}

.capa {
  width: 10rem;
  margin: 0.5rem;
}

</style>

