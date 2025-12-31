import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./Admin.css";

import AdminHeader from "./components/AdminHeader";
import VilleList from "./components/VilleList";
import VilleModal from "./components/VilleModal";

import { useVilles } from "./hooks/useVilles";
import { fetchCoordinatesFromNominatim } from "./services/geocodingService";
import * as villeService from "./services/villeService";
import tokenStorageService from "./services/tokenStorageService";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faPlus } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
export default function Admin() {
  const { villes, fetchVilles, deleteVille, moveVille } = useVilles();

  const [modalMode, setModalMode] = useState(null); // view | edit | add
  const [selectedVille, setSelectedVille] = useState(null);

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginModalOpen, setLoginModalOpen] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


  const checkToken = async (token) => {
      if (!token) {
    setIsAuthenticated(false);
    return;
  }
        const res = await fetch("/api/verify-token", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
            }
        });
        if (!res.ok) setIsAuthenticated(false);
        if(res.ok) setIsAuthenticated(true);
       
    };


useEffect(() => {
 checkToken(tokenStorageService.getToken())
  document.body.style.background = "#FEFEFE";
}, [])
 
  const openModal = (mode, ville = null) => {
    setModalMode(mode);
    setSelectedVille(
      ville
        ? { ...ville, recettes: ville.recettes || [], attractions: ville.attractions || [] }
        : { nom: "", recettes: [], attractions: [] }
    );
  };
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const data = await loginAdmin(username, password);
            tokenStorageService.setToken(data.token);
           
            setIsAuthenticated(true);
            setLoginModalOpen(false);
            toast.success("Connexion réussie !");
        } catch (err) {
          console.error(err)
            toast.error("Mot de passe incorrect");
        }
    };

  const handleSave = async () => {
    if (!selectedVille.nom?.trim()) {
      toast.error("Le nom est obligatoire");
      return;
    }

    try {
      const coords = await fetchCoordinatesFromNominatim(selectedVille.nom);
      if (!coords) {
        toast.error("Ville introuvable");
        return;
      }

      const attractions = [];
      for (const a of selectedVille.attractions) {
        if (!a.nom) continue;
        const aCoords = await fetchCoordinatesFromNominatim(a.nom);
       
        attractions.push({ ...a, ...aCoords, ville_id: selectedVille.id });
      }

      const payload = {
        ...selectedVille,
        ...coords,
        attractions,
      };
      
     if (modalMode === "add") {
  payload.position = villes.length+1;
  await villeService.createVille(payload);
} else {
  await villeService.updateVille(selectedVille.id, payload);
}
      setModalMode(null);
      fetchVilles();
     
      toast.success("Sauvegarde réussie !");
    } catch {
      toast.error("Erreur lors de la sauvegarde");
    }
  };
    const loginAdmin = async (username, password) => {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify({ password })
        });
        if (!res.ok) throw new Error("Mot de passe incorrect");
   
        return res.json();
    };

    const importTemplate = async () => {
    const confirmFlush = window.confirm(
    "⚠️ Cette opération va réinitialiser la base de données et supprimer toutes vos données actuelles. Continuer ?"
  );
  
  if (!confirmFlush) return;
  try {
    let res = await fetch("/api/flushDB", { method: "POST", headers: {"Authorization": `Bearer ${tokenStorageService.getToken()}`} });
    if (!res.ok) throw new Error("Erreur lors du flush de la base");

    res = await fetch("/api/insertDATA", { method: "POST", headers: {"Authorization": `Bearer ${tokenStorageService.getToken()}`} });
    if (!res.ok) throw new Error("Erreur lors de l'insertion des données");

    toast.success("Base réinitialisée et données insérées avec succès !");
    
    fetchVilles();
  } catch (err) {
    console.error(err);
    toast.error(`Erreur : ${err.message}`);
  }
};
const disconnect = () => {
  tokenStorageService.removeToken();
  setIsAuthenticated(false);
  window.location.reload();
}
  return (
    <div className="admin-container">

      {isAuthenticated ? ( <>
      <AdminHeader
        onAdd={() => openModal("add")}
        onImport={() => importTemplate()}
        onDisconnect={() => disconnect()}
      />

      <VilleList
        villes={villes}
        onMove={moveVille}
        onDelete={deleteVille}
        onView={(v) => openModal("view", v)}
        onEdit={(v) => openModal("edit", v)}
      />

      {modalMode && selectedVille && (
        <VilleModal
          mode={modalMode}
          ville={selectedVille}
          setVille={setSelectedVille}
          onClose={() => setModalMode(null)}
          onSave={handleSave}
        />
      )}

    
           
        </>) : <div>
          
           {loginModalOpen && (
                <div className="modal-overlay" style={{display: "flex", flexDirection: "column", gap: "25px"}}> 
                 <Link className="add-btn" to="/">
        <FontAwesomeIcon icon={faHome} /> Accueil
      </Link>
                    <div className="modal">
                        <h2>Connexion Admin</h2>
                        <form onSubmit={handleLogin} className="modal-fields">
                            <input
                                type="text"
                                placeholder="Nom d'utilisateur"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                            <input
                                type="password"
                                placeholder="Mot de passe"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <div className="modal-buttons">
                                <button type="submit" className="add-btn">Se connecter</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
          
          
          
          </div>}
  
       
              <ToastContainer />

    </div>
  );
}
