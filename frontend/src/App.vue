<script setup lang="ts">
</script>

<template>
  <div id="app">
    <header>
      <img alt="Vue logo" src="./booklogo.png" height="50" class="logo">
      <h1>Biblioteca</h1>
      <button class="sair" @click="refreshPage">Sair</button>
    </header>
    <main>
      <login v-if="!loggedIn && !showRegister && !showAdm" @login-success="loginSuccess" @go-to-register="showRegister = true" @go-to-adm="showAdm = true" />
      <sign-up v-if="!loggedIn && showRegister && !showAdm" @register-success="loginSuccess" @go-to-login="showRegister = false" />
      <adm-login v-if="!loggedInAdm && !showRegister && showAdm" @login-success="loginSuccessAdm" />
      <div class="container" v-if="loggedIn">
        <list ref="listMonitorias" />
      </div>
      <div class="container" v-if="loggedInAdm && !showNewAdmPage && !showRegister">
        <list-adm ref="listAdm" @go-to-new-adm="showNewAdmPage = true" />
      </div>
      <div class="container" v-if="showNewAdmPage">
        <create-adm @go-back="goBack" />
      </div>
    </main>
  </div>
</template>

<script>
import Login from "./components/Login.vue";
import AdmLogin from "./components/AdmLogin.vue";
import SignUp from "./components/SignUp.vue";
import CreateAdm from "./components/CreateAdm.vue";
import List from "./components/List.vue";
import ListAdm from "./components/ListAdm.vue";

export default {
  components: {
    Login,
    AdmLogin,
    SignUp,
    CreateAdm,
    List,
    ListAdm,
  },
  data() {
    return {
      loggedIn: false,
      loggedInAdm: false,
      showRegister: false,
      showAdm: false,
      showNewAdmPage: false,
    };
  },
  methods: {
    loginSuccess(userId) {
    this.loggedIn = true;
    this.$nextTick(() => {
      console.log("next Tick" );
      this.$refs.listMonitorias.loadUserMonitorias(userId);
      this.$refs.listMonitorias.loadAllMonitorias();
    });
  },
    loginSuccessAdm(userId) {
    this.loggedInAdm = true;
    this.$nextTick(() => {
      console.log("next Tick" );
      this.$refs.listAdm.loadUserMonitorias(userId);
      this.$refs.listAdm.loadAllMonitorias();
      this.$refs.listAdm.loadUsers();
    });
  },
    goBack(userId) {
    this.showNewAdmPage = false; 
    this.$nextTick(() => {
      console.log("next Tick" );
      this.$refs.listAdm.loadUserMonitorias(userId);
      this.$refs.listAdm.loadAllMonitorias();
      this.$refs.listAdm.loadUsers();
    });
  },
    refreshPage() {
      window.location.reload();
    },
  },
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.sair {
  background-color: white;
  color: #103c5c;
  margin-right: 2rem;
  padding: 0.5rem;
  border-radius: 0.7rem;
  font-weight: bolder;
}

body {
  font-family: Arial, sans-serif;
  background-color: #ffffff;
  opacity: 1;
  height: 100vh;
  width: 100vw;
}

.container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: stretch;
  width: 100%;
  padding: 1rem;
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100vw;
  background-color: purple;
  padding: 20px 0;
  color: white;
  text-transform: uppercase;
}

.logo {
  margin-left: 2rem;
}

h1 {
  margin: 0;
  font-size: 1.5rem;
}

main {
  display: flex;
  flex-direction: column;
  align-items: certer;
  width: 100%;
  /*padding: 1rem;
  margin-top: 0.5rem;*/
}

</style>


