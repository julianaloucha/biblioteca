<template>
<main>
  <div class="row">
    <div id="monitorias-disponiveis" class="columnleft">
        <h1>Monitorias Administrator</h1>

        <table class="table table-hover">
          <thead>
            <tr>
              <th>title</th>
              <th>Data</th>
              <th>Horário</th>
              <th>Local</th>
            </tr>
          </thead>
          <tbody>  
            <tr v-for="monitoria in allMonitorias" :key="monitoria._id">
              <td>{{ monitoria.title }}</td>
              <td>{{ monitoria.date }}</td>
              <td>{{ monitoria.time }}</td>
              <td>{{ monitoria.description }}</td>
            </tr>        
          </tbody>
        </table>
    </div>
    <div class="columnright">
      <h2>Oferecer Monitoria</h2>
      <form @submit.prevent="addMonitoria">
        <input type="text" v-model="title" placeholder="title da monitoria" required />
        <input type="date" v-model="date" placeholder="Data da monitoria" required />
        <input type="time" v-model="time" placeholder="Horário da monitoria" required />
        <input type="text" v-model="description" placeholder="Local da monitoria" required />
        <button type="submit">Adicionar</button>
      </form>
      <ul>
        <li v-for="monitoria in monitorias" :key="monitoria._id">
          <div class="monitoria-title">
            {{ monitoria.title }}
          </div>
          <div class="monitoria-title">
            {{ monitoria.date }}
          </div>
          <div class="monitoria-title">
            {{ monitoria.time }}
          </div>
          <div class="monitoria-title">
            {{ monitoria.description }}
          </div>
          <div class="actions">
            <button @click="deleteMonitoria(monitoria._id)">Excluir</button>
            <button @click="showUpdateForm(monitoria)">Atualizar</button>
          </div>
          <div v-if="beingEdited && beingEdited._id === monitoria._id" class="edit">
            <h3>Editar Tarefa</h3>
            <form @submit.prevent="updateAndHide">
              <input type="text" v-model="beingEdited.title" required />
              <input type="date" v-model="beingEdited.date" required />
              <input type="time" v-model="beingEdited.time" required />
              <input type="text" v-model="beingEdited.description" required />
              <button type="submit">Salvar</button>
              <button type="button" @click="beingEdited = null">Cancelar</button>
            </form>
          </div>
        </li>
      </ul>
    </div>
  </div>
</main>
</template>

<script>
import { getMonitorias, createMonitoria, updateMonitoria, deleteMonitoria, getAllMonitorias } from "../api";

export default {
  data() {
    return {
      monitorias: [],
      allMonitorias: [],
      title: "",
      date: "",
      time: "",
      description: "",
      beingEdited: null,
      userId: null,
    };
  },
  methods: {
    async loadUserMonitorias(userId) {
      this.userId = userId;
      this.monitorias = await getMonitorias(userId);
    },
    async loadAllMonitorias() {
      console.log("allMonitorias: " )
      this.allMonitorias = await getAllMonitorias();
    },
    async addMonitoria() {
      const monitoria = {
        title: this.title,
        date: this.date,
        time: this.time,
        description: this.description,
        done: false,
      };
      const created = await createMonitoria(monitoria, this.userId);
      this.monitorias.push(created);
      this.title = "";
      this.date = "";
      this.time = "";
      this.description = "";
      this.loadAllMonitorias();
    },
    async deleteMonitoria(monitoriaId) {
      await deleteMonitoria(monitoriaId);
      this.monitorias = this.monitorias.filter((monitoria) => monitoria._id !== monitoriaId);
      this.loadAllMonitorias();
    },
    showUpdateForm(monitoria) {
      this.beingEdited = monitoria;
  },
    async updateAndHide() {
      await updateMonitoria(this.beingEdited._id, this.beingEdited);
      this.beingEdited = null;
      this.loadAllMonitorias();
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

</style>

