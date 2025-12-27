import tokenStorageService from "./tokenStorageService"
export const getVilles = () =>
  fetch("/api/villes").then(res => res.json());

export const createVille = (ville) =>
  fetch("/api/villes", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${tokenStorageService.getToken()}` },
    
    body: JSON.stringify(ville),
  });
export const updateVille = (id, ville) => {
  return fetch(`/api/villes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json","Authorization": `Bearer ${tokenStorageService.getToken()}` },
    body: JSON.stringify(ville),
  }).then(res => {
    if (!res.ok) return "";
    return res.json();
  });
};
 
 

export const deleteVilleById = (id) =>
  fetch(`/api/villes/${id}`, { method: "DELETE", headers: {"Authorization": `Bearer ${tokenStorageService.getToken()}`} });

export const reorderVilles = (payload) => 
  fetch("/api/villes/reorder", {
    method: "PUT",
    headers: { "Content-Type": "application/json","Authorization": `Bearer ${tokenStorageService.getToken()}` },
    body: JSON.stringify(payload),
  });

export const flushAndInsertTemplate = async () => {
  await fetch("/api/flushDB", { method: "POST", headers: {"Authorization": `Bearer ${tokenStorageService.getToken()}`} });
  await fetch("/api/insertDATA", { method: "POST", headers: {"Authorization": `Bearer ${tokenStorageService.getToken()}`} });
};
