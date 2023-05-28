<template>
    <div>
      <button @click="goBack">Go Back</button>
      <h2>CREATE ADM</h2>
      <form @submit.prevent="register">
        <input type="email" v-model="email" placeholder="E-mail" required />
        <input type="password" v-model="password" placeholder="Senha" required />
        <input type="text" v-model="name" placeholder="Nome" required />
        <button type="submit">Registrar</button>
      </form>
    </div>
  </template>
  
  <script>
  import { registerAdm } from "../api";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        name: "",
      };
    },
    methods: {
      async register() {
        try {
          const adm = {
            email: this.email,
            password: this.password,
            name: this.name,
          };
          await registerAdm(adm); // Armazenar o retorno da chamada
          this.email = "";
          this.password = "";
          this.name = "";
        } catch (error) {
          console.error(error);
          alert('Registro falhou');
        }
      },
        goBack() {
            this.$emit('go-back'); // Emit a custom event to go back to the ListAdm page
        },
    },
  };
  </script>
  
  <style scoped>
  div {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    font-family: Arial, sans-serif;
  }
  
  h2 {
    color: #333;
    margin-bottom: 1.5rem;
  }
  
  form {
    display: flex;
    flex-direction: column;
    width: 300px;
    padding: 1rem;
    border: 1px solid #e1e1e1;
    border-radius: 5px;
  }
  
  select, input {
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: none;
    border-radius: 5px;
    border: 1px solid #e1e1e1;
  }

  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  button {
    padding: 0.5rem;
    background-color: #103c5c;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  button:hover {
    background-color: #103c5c;
  }
  </style>
  
  