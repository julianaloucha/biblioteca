<template>
    <div class='card-wrapper'>
      <h2 class='call-to-action'>Cadastro</h2>
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
          await registerUser(user);
          this.email = "";
          this.password = "";
          this.name = "";
          this.curso = "";
          this.ra = "";
          alert('Aguarde a aprovação do seu usuário');
        } catch (error) {
          console.error(error);
          alert('Registro falhou');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  *{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

input {
    padding: 1rem;
    margin-bottom: 1rem;
    border: none;
    background-color: #D1FAFF;
    font-family: monospace;
    font-size: 20px;
    color: #1F271B;
    border-bottom: #1F271B 1px solid;
    width: 80%;
    margin: 1.5rem auto 0;

  }
select{
  padding: 1rem;
  margin-bottom: 1rem;
  border: none;
  background-color: #D1FAFF;
  font-family: monospace;
  font-size: 20px;
  color: #1F271B;
  border-bottom: #1F271B 1px solid;
  width: 80%;
  margin: 1.5rem auto 0;
}
.card-wrapper{
  min-height: 350px;
  min-width: 350px;
  border-radius: 20px;
  position:absolute;
  left: 50%;
  bottom: 30;
  margin-top: 30px;
  transform: translateX(-50%);
  background:#D1FAFF;
  box-shadow: 0 0 20px -2px black;
  display:flex;
  justify-content:center;
  flex-direction: column;
  padding: 20px 0;
  color: #1F271B;
}

.call-to-action{
  font-family:monospace;
  font-size: 40px;
  text-align:center;
  padding: 10px 0;
  color: #1F271B;
}

.card-wrapper form{
  display:flex;
  flex-direction:column;
}
.card-wrapper form .field{
  font-family:monospace;
  width: 100%;
  position: relative;
  font-size: 18px;
  padding: 7px 30px;
  white-space: no-wrap;
}
.card-wrapper form .field::after{
  content : "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 100%;
  height: 1px;
  width: 85%;
  padding-top: 5px;
  border-top:1px solid #1F271B;
}
.card-wrapper form a span{
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}
.card-wrapper form .field input{
  border: 0;
  background: transparent;
  padding:0 5px;
  color: inherit;
  font-family: monospace;
  font-size: 18px ;
  height: 30px;
  width: calc(100% - 50px);
  vertical-align: middle;
}
.card-wrapper form .field input:focus{
  outline:none;
}
.card-wrapper form .field input::placeholder{
  color: #1F271B;
}

button {
    font-family: monospace;
    font-style: bold;
    width: 60%;
    padding: 0.5rem;
    margin: 1.5rem auto 0;
    background-color: #0B4F6C;
    color: #D1FAFF;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s ease;

}
button:hover {
    background-color: #A9D3FF;
    color: #1F271B;
  }

  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

</style>