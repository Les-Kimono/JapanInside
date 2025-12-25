import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./Admin.css";

import AdminHeader from "./components/AdminHeader";
import VilleList from "./components/VilleList";
import VilleModal from "./components/VilleModal";

import { useVilles } from "./hooks/useVilles";
import { fetchCoordinatesFromNominatim } from "./services/geocodingService";
import * as villeService from "./services/villeService";

export default function Admin() {
  const { villes, fetchVilles, deleteVille, moveVille } = useVilles();

  const [modalMode, setModalMode] = useState(null); // view | edit | add
  const [selectedVille, setSelectedVille] = useState(null);

  const openModal = (mode, ville = null) => {
    setModalMode(mode);
    setSelectedVille(
      ville
        ? { ...ville, recettes: ville.recettes || [], attractions: ville.attractions || [] }
        : { nom: "", recettes: [], attractions: [] }
    );
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

      modalMode === "add"
        ? await villeService.createVille(payload)
        : await villeService.updateVille(selectedVille.id, payload);

      setModalMode(null);
      fetchVilles();
     
      toast.success("Sauvegarde réussie !");
    } catch {
      toast.error("Erreur lors de la sauvegarde");
    }
  };

  const importTemplate = async () => {
    const confirmFlush = window.confirm(
    "⚠️ Cette opération va réinitialiser la base de données et supprimer toutes vos données actuelles. Continuer ?"
  );
  
  if (!confirmFlush) return;
  try {
    let res = await fetch("/api/flushDB", { method: "POST" });
    if (!res.ok) throw new Error("Erreur lors du flush de la base");

    res = await fetch("/api/insertDATA", { method: "POST" });
    if (!res.ok) throw new Error("Erreur lors de l'insertion des données");

    toast.success("Base réinitialisée et données insérées avec succès !");
    
    fetchVilles();
  } catch (err) {
    console.error(err);
    toast.error(`Erreur : ${err.message}`);
  }
};

  return (
    <div className="admin-container">
      <ToastContainer />

      <AdminHeader
        onAdd={() => openModal("add")}
        onImport={() => importTemplate()}
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
    </div>
  );
}
