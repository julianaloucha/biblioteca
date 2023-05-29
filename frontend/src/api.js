// src/api.js
const API_URL = "http://localhost:5000/api";

async function fetchData(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const responseBody = await response.text();
    throw new Error(`${responseBody} ${response.status}`);
  }
  return response.json();
}

export async function getMonitorias(userId) {
  return fetchData(`${API_URL}/monitorias/${userId}`);
}

export async function getAllMonitorias() {
  return fetchData(`${API_URL}/monitorias`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(),
  });
}

export async function createMonitoria(monitoria, userId) {
  monitoria.user_id = null;  // Adicione o user_id à tarefa
  return fetchData(`${API_URL}/monitorias`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(monitoria),
  });
}



export async function updateMonitoria(monitoriaId, monitoria) {
  return fetchData(`${API_URL}/monitorias/${monitoriaId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(monitoria),
  });
}

export async function deleteMonitoria(monitoriaId) {
  return fetchData(`${API_URL}/monitorias/${monitoriaId}`, {
    method: "DELETE",
  });
}

export async function loginUser(user) {
  const response = await fetchData(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  return response.user_id;
}

export async function registerUser(user) {
  const response = await fetchData(`${API_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  return response._id;
}

export async function loginAdm(user) {
  const response = await fetchData(`${API_URL}/loginadm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  return response.user_id;
}

export async function registerAdm(user) {
  const response = await fetchData(`${API_URL}/adm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  return response._id;
}

export async function getUsers() {
  return fetchData(`${API_URL}/allusers`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(),
  });
}

export async function updateUser(userId, user) {
  return fetchData(`${API_URL}/allusers/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
}
