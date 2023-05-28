<template>
<main>
  <button @click="goToNewAdmPage">Create New Administrator</button>
  <div class="row">
    <div id="monitorias-disponiveis" class="columnleft">
      <h1>Monitorias Administrator</h1>

      <table class="table table-hover">
        <thead>
          <tr>
            <th>Nome</th>
            <th>RA</th>
            <th>Curso</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>  
          <tr v-for="user in users" :key="user._id">
            <td>{{ user.name }}</td>
            <td>{{ user.ra }}</td>
            <td>{{ user.curso }}</td>
            <td>{{ user.status }}</td>
            <td><button @click="updateUser(user)">Autorizar</button></td>
          </tr>        
        </tbody>
      </table>
    </div>
    <div class="columnright">
      <h2>Cadastrar novo livro</h2>
      <form @submit.prevent="addMonitoria">
        <input type="text" v-model="title" placeholder="Título do livro" required />
        <input type="text" v-model="author" placeholder="Autor" required />
        <input type="text" v-model="isbn" placeholder="ISBN" required />
        <input type="text" v-model="description" placeholder="Descrição" required />
        <input type="file" @change="handleImageUpload" accept="image/*" placeholder="Imagem da capa" required />
        <button type="submit">Adicionar</button>
      </form>
    </div>
  </div>
  <ul>
    <li v-for="book in allBooks" :key="book._id">
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
        <button @click="deleteMonitoria(book._id)">Excluir</button>
        <button @click="showUpdateForm(book)">Atualizar</button>
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
</main>
</template>

<script>
import { getMonitorias, createMonitoria, updateMonitoria, deleteMonitoria, getAllMonitorias, getUsers, updateUser } from "../api";

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
    async updateUser(user) {
      console.log("userUpdate: " + user.name);
      user.status = "approved"
      await updateUser(user._id, user);
      this.loadUsers();
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
  flex-direction: column;
  background-color: #f0f0f0;
  padding: 0px;
  border-radius: 5px;
  margin-bottom: 1px;
  flex-basis: 10%; 
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

.capa {
  width: 10rem;
  margin: 0.5rem;
}

</style>

