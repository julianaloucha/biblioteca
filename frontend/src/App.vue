<script setup lang="ts">
</script>

<template>
  <div id="app">
    <header>
      <p class="spacelogo">.......Sair.</p>
      <img alt="Vue logo" src="./BIBLIOTECA.png" height="200" class="logo">
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
body{
  background-color: #D1FAFF;
}
.sair {
  background-color: #0B4F6C;
  color: #D1FAFF;
  margin-right: 2rem;
  padding: 0.5rem;
  border-radius: 15px;
  font-family: monospace;
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
  padding: 20px 0;
  text-transform: uppercase;
  font-family: monospace;
}

.logo {
  margin-left: 0rem;
}

main {
  display: flex;
  flex-direction: column;
  align-items: certer;
  width: 100%;
  /*padding: 1rem;
  margin-top: 0.5rem;*/
}

.spacelogo{
  color: #D1FAFF;
}

</style>


