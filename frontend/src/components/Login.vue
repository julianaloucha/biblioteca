<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input type="email" v-model="email" placeholder="E-mail" required />
        <input type="password" v-model="password" placeholder="Senha" required />
        <button type="submit">Login</button>
      </form>
      <button @click="$emit('go-to-register')">Sign up</button>
      <button @click="$emit('go-to-adm')">Adm</button>
    </div>
  </template>
  
  <script>
  import { loginUser } from "../api";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const user = {
            email: this.email,
            password: this.password,
          };
          const userId = await loginUser(user); // Armazenar o retorno da chamada
          this.$emit('login-success', userId);  // Emitir o userId no evento
        } catch (error) {
          console.error(error);
          alert(error);
        }
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
    margin-bottom: 1rem;
  }
  
  input {
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: none;
    border-radius: 5px;
    border: 1px solid #e1e1e1;
  }
  
  button {
    padding: 0.5rem;
    background-color: purple;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  button:hover {
    background-color: #103c5c;
  }
  
  button:last-child {
    background-color: #e1e1e1;
    color: #333;
  }
  
  button:last-child:hover {
    background-color: #c4c4c4;
  }
  </style>
  
  