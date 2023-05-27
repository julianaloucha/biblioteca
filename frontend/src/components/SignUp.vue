<template>
    <div>
      <h2>Sign up</h2>
      <form @submit.prevent="register">
        <input type="email" v-model="email" placeholder="E-mail" required />
        <input type="password" v-model="password" placeholder="Senha" required />
        <input type="text" v-model="name" placeholder="Nome" required />
        <select v-model="curso" required> 
                    <option value="" disabled selected hidden>Selecione seu curso</option>
                    <option value="Administração">Administração</option>
                    <option value="Design">Design</option>
                    <option value="Direito">Direito</option>
                    <option value="Economia">Economia</option>
                    <option value="Computação">Computação</option>
                    <option value="Produção">Produção</option>
                    <option value="Mecânica">Mecânica</option>
                    <option value="PPM">PPM</option>
                    <option value="RI">RI</option>
        </select>
        <input type="number" v-model="ra" placeholder="RA" required />
        <button type="submit">Registrar</button>
      </form>
    </div>
  </template>
  
  <script>
  import { registerUser } from "../api";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        name: "",
        curso: "",
        ra: "",
      };
    },
    methods: {
      async register() {
        try {
          const user = {
            email: this.email,
            password: this.password,
            name: this.name,
            curso: this.curso,
            ra: this.ra,
          };
          const userId = await registerUser(user); // Armazenar o retorno da chamada
          this.$emit('register-success', userId);  // Emitir o userId no evento
        } catch (error) {
          console.error(error);
          alert('Registro falhou');
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
  
  