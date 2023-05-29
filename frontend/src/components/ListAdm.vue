<template>
  <main>
    <header>
      <button class="adm-button" @click="goToNewAdmPage">Criar Novo Administrador</button>
      <button class="notification-button" :class="{ 'has-notifications': notifications.length > 0 }" @click="toggleNotificationBox">{{ showNotificationBox ? 'Fechar' : 'Notificações' }}</button>
    </header>
      <div class="notification-box" v-show="showNotificationBox">
        <h3>Notificações</h3>
        <ul>
          <li v-for="notification in notifications" :key="notification" class="notif">{{ notification }}</li>
        </ul>
      </div>
    <div class="row">
      <div id="monitorias-disponiveis" class="columnleft">
        <h1>Usuários</h1>

        <div id="table-wrapper">
          <div id="table-scroll">
            <div class="fixTableHead">
        <table class="usertable">
          <thead>
            <tr>
              <th>Nome</th>
              <th>RA</th>
              <th>Curso</th>
              <th>Status</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>  
            <tr v-for="user in users" :key="user._id">
              <td>{{ user.name }}</td>
              <td>{{ user.ra }}</td>
              <td>{{ user.curso }}</td>
              <td>{{ user.status }}</td>
              <td v-if="user.status == 'waiting'"><button @click="approveUser(user)">Autorizar</button></td>
              <td v-if="user.status == 'approved'"><button @click="suspendUser(user)">Suspender</button></td>
              <td v-if="user.status != 'approved' && user.status != 'waiting'"><button @click="approveUser(user)">Retirar suspensão</button></td>
              <td><button @click="deletarUser(user._id)">Deletar</button></td>
            </tr>        
          </tbody>
        </table> 
      </div>
      </div>
    </div>
  </div>
      <div class="columnright">
        <h1>Livros reservados</h1>
        <div id="table-wrapper">
          <div id="table-scroll">
            <div class="fixTableHead">
        <table class="usertable">
          <thead>
            <tr>
              <th>Título</th>
              <th>ISBN</th>
              <th>Aluno</th>
              <th>Devolução</th>
              <th>QRCode</th>
              <th></th>
            </tr>
          </thead>
          <tbody>  
            <tr v-for="book in books" :key="book._id">
              <td>{{ book.title }}</td>
              <td>{{ book.isbn }}</td>
              <td>{{ book.userRA }}</td>
              <td>{{ book.return }}</td>
              <td>
                <img :src="book.qrcodeImage" alt="QR Code" />
              </td>
              <td><button @click="returned(book)">Devolvido</button></td>
            </tr>        
          </tbody>
        </table>
      </div>
      </div>
    </div>
      </div>
    </div>
    <div class="spacebefore">
      <h2>Cadastrar novo livro</h2>
      <form @submit.prevent="addMonitoria">
        <input type="text" v-model="title" placeholder="Título do livro" required />
        <input type="text" v-model="author" placeholder="Autor" required />
        <input type="text" v-model="isbn" placeholder="ISBN" required />
        <input type="text" v-model="description" placeholder="Descrição" required />
        <input type="file" @change="handleImageUpload" accept="image/*" placeholder="Imagem da capa" required />
        <button class="adc" type="submit">Adicionar</button>
      </form>
      <h2>Livros</h2>
      <div class="search-bar">
        <input type="text" v-model="searchTerm" placeholder="Pesquisar livros" />
      </div>
      <ul>
        <li v-for="book in filteredBooks" :key="book._id">
          <div class="monitoria-title">
            {{ book.title }}
          </div>
          <div class="monitoria-title">
            {{ book.author }}
          </div>
          <div class="monitoria-title">
            <img :src="book.image"  class="capa" />
          </div>
          <div class="actions">
            <button class="delete" @click="deleteMonitoria(book._id)">Excluir</button>
            <button class="novo" @click="showUpdateForm(book)">Atualizar</button>
          </div>
          <div v-if="beingEdited && beingEdited._id === book._id" class="edit">
            <h3>Editar Tarefa</h3>
            <form @submit.prevent="updateAndHide">
              <input type="text" v-model="beingEdited.title" placeholder="Título do livro" required />
              <input type="text" v-model="beingEdited.author" placeholder="Autor" required />
              <input type="text" v-model="beingEdited.isbn" placeholder="ISBN" required />
              <input type="text" v-model="beingEdited.description" placeholder="Imagem da capa" required />
              <button type="submit">Salvar</button>
              <button type="button" @click="beingEdited = null">Cancelar</button>
            </form>
          </div>
        </li>
      </ul>
    </div>
  </main>
</template>

<script>
import { getMonitorias, createMonitoria, updateMonitoria, deleteMonitoria, getAllMonitorias, getUsers, updateUser, deleteUser } from "../api";

export default {
  data() {
    return {
      users: [],
      books: [],
      allBooks: [],
      title: "",
      author: "",
      isbn: "",
      description: "",
      beingEdited: null,
      userId: null,
      imageData: null,
      userEdited: null,
      notifications: [], // Array to store notifications
      showNotificationBox: false, 
      searchTerm: "",
    };
  },
  methods: {
    async loadUserMonitorias(userId) {
      this.userId = userId;
      this.books = await getMonitorias(userId);
    },
    async loadAllMonitorias() {
      this.allBooks = await getAllMonitorias();
      this.books = this.allBooks.filter(book => book.user_id !== null);

      await this.loadUsers();
      // Attach the user's RA to each book
      this.books.forEach((book) => {
        const user = this.users.find((user) => user._id === book.user_id);
        book.userRA = user.ra;

        // Check if today's date is greater than the return date
        const returnDate = new Date(book.return);
        const currentDate = new Date();
        const suspensionDate = new Date(returnDate.getTime() + (5 * 24 * 60 * 60 * 1000));
        if (currentDate > suspensionDate) {
          const user = this.users.find((user) => user._id === book.user_id);
          if (user) {
            // Add one month to the user's status
            const newStatusDate = suspensionDate;
            newStatusDate.setMonth(newStatusDate.getMonth() + 1);
            user.status = newStatusDate.toISOString();

            // Format the date to have only year, month, and day
            const formattedDate = newStatusDate.toISOString().split('T')[0];
            user.status = formattedDate;

            updateUser(user._id, user); // Update the user's status in the database
          }
        }

      });

      this.users.forEach((user) => {
        // Check if today's date is greater than or equal to the status date
        const statusDate = new Date(user.status);
        const currentDate = new Date();
        if (currentDate >= statusDate) {
          user.status = "approved";
          updateUser(user._id, user); // Update the user's status in the database
        }
      })

      this.showNotifications();
    },
    async loadUsers() {
      this.users = await getUsers();
    },
    async addMonitoria() {
      const book = {
        title: this.title,
        author: this.author,
        isbn: this.isbn,
        description: this.description,
        image: this.imageData, // Store the image data in the book.image field
      };
      const created = await createMonitoria(book, this.userId);
      this.books.push(created);
      this.title = "";
      this.author = "";
      this.isbn = "";
      this.description = "";
      this.imageData = null; // Reset the imageData after submission
      this.loadAllMonitorias();
    },
    async deleteMonitoria(bookId) {
      await deleteMonitoria(bookId);
      this.allBooks = this.allBooks.filter((book) => book._id !== bookId);
      this.loadAllMonitorias();
    },
    showUpdateForm(book) {
      this.beingEdited = book;
    },
    async updateAndHide() {
      await updateMonitoria(this.beingEdited._id, this.beingEdited);
      this.beingEdited = null;
      this.loadAllMonitorias();
    },
    async approveUser(user) {
      user.status = "approved"
      await updateUser(user._id, user);
      this.loadUsers();
    },
    async suspendUser(user) {
      user.status = "suspended";
      await updateUser(user._id, user);
      this.loadUsers();
    },
    async returned(book) {
      book.user_id = null;
      book.date = null;
      book.return = null;
      book.qrcodeImage = null;
      await updateMonitoria(book._id, book);
      this.loadUsers();
      this.loadAllMonitorias();
      this.showNotifications();
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageData = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    goToNewAdmPage() {
      this.$emit('go-to-new-adm'); // Emit a custom event to the parent component (App.vue)
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
    async deletarUser(userId) {
      await deleteUser(userId);
      this.loadAllMonitorias();
      this.loadUsers();
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
  .fixTableHead thead th {
    position: sticky;
    top: 0;
  }
  #table-wrapper {
  position:relative;
}
.usertable {
  text-align: center;
}
td:first-child {
  text-align: left;
  padding-left: 6px;
}
#table-scroll {
  height:400px;
  overflow:auto;  

}
#table-wrapper table {
  width:100%;
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
    margin-left: 1rem;
    font-family:monospace;
  }
  
  form {
    display: flex;
    flex-direction: column;
    width: 75%;
    margin-bottom: 1rem;
    font-family:monospace;
  }
  
  input {
    flex-grow: 1;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    border: none;
    border-radius: 5px;
    border: 3px solid #ccc;
    font-family:monospace;
  }
  .notification-button{
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  .notification-button:hover{
    background-color: #A9D3FF;
    color: #1F271B;
  }
  .adm-button{
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  .adm-button:hover{
    background-color: #A9D3FF;
    color: #1F271B;
  }
  .adc{
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  .adc:hover{
    background-color: #A9D3FF;
    color: #1F271B;
  }
  .delete{
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  .delete:hover{
    background-color: #D1FAFF;
    color: #1F271B;
  }
  .novo{
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  .novo:hover{
    background-color: #D1FAFF;
    color: #1F271B;
  }
  
  button {
    padding: 0.5rem 1rem;
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
    font-family:monospace;
  }
  
  button:hover {
    background-color: #D1FAFF;
    color: #1F271B;
  }
  
  ul {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    padding: 0;
    justify-content: start;
    align-items: flex-start;
    width: 100%;
    gap: 2rem;
    font-family:monospace;
  }
  
  li {
    display: flex;
    flex-direction: column;
    background-color: #A9D3FF;
    padding: 0px;
    border-radius: 5px;
    margin-bottom: 1px;
    flex-basis: 18%; 
  }
  
  .monitoria-title {
    margin-bottom: 0.1rem;
    align-items: center;
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
    font-size: 15px;
    margin-right: 2rem;
    background-color: #A9D3FF;
    border-radius: 5px;
    padding: 1rem;
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
    z-index: 999;
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

  .spacebefore {
    padding: 2rem;
  }
  
  </style>
  