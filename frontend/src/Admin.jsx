import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./admin.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faTrash,
  faEye,
  faEdit,
  faChevronUp,
  faChevronDown,
  faPlus,
  faFileImport,
} from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

const fetchCoordinatesFromNominatim = async (ville) => {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
      ville,
    )}&format=json&limit=1`,
    {
      headers: {
        Accept: "application/json",
        "User-Agent": "JapanInsideAdmin/1.0",
      },
    },
  );

  const data = await res.json();

  if (!data || data.length === 0) {
    return null;
  }

  return {
    latitude: parseFloat(data[0].lat),
    longitude: parseFloat(data[0].lon),
  };
};

const Admin = () => {
  const [villes, setVilles] = useState([]);
  const [selectedVille, setSelectedVille] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [isViewing, setIsViewing] = useState(false);

  useEffect(() => {
    fetchVilles();
  }, []);

  const fetchVilles = async () => {
    try {
      const res = await fetch("/api/villes");
      const data = await res.json();
      setVilles(data);
    } catch (err) {
      console.error(err);
    }
  };

  const moveVille = async (index, direction) => {
    const newVilles = [...villes];
    const targetIndex = index + direction;
    if (targetIndex < 0 || targetIndex >= newVilles.length) return;
    [newVilles[index], newVilles[targetIndex]] = [
      newVilles[targetIndex],
      newVilles[index],
    ];

    try {
      console.log(newVilles.map((v, i) => ({ id: v.id, position: i + 1 })));

      const res = await fetch("/api/villes/reorder", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          newVilles.map((v, i) => ({ id: v.id, position: i + 1 })),
        ),
      });
      setVilles(newVilles);
      toast.success("Ordre des villes mis à jour !");
      console.log(res);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteVille = async (id) => {
    if (!confirm("Supprimer cette ville ?")) return;
    try {
      await fetch(`/api/villes/${id}`, { method: "DELETE" });
      setVilles(villes.filter((v) => v.id !== id));
      toast.success("Ville supprimée !");
    } catch (err) {
      console.error(err);
    }
  };

  const openViewModal = (ville) => {
    setSelectedVille({
      ...ville,
      recettes: ville.recettes || [],
      attractions: ville.attractions || [],
    });
    setShowModal(true);
    setIsViewing(true);
    setIsAdding(false);
  };

  const openEditModal = (ville) => {
    setSelectedVille({
      ...ville,
      recettes: ville.recettes || [],
      attractions: ville.attractions || [],
    });
    setShowModal(true);
    setIsViewing(false);
    setIsAdding(false);
  };

  const openAddModal = () => {
    setSelectedVille({
      nom: "",
      recettes: [],
      attractions: [],
    });
    setShowModal(true);
    setIsAdding(true);
    setIsViewing(false);
  };
  const handleSave = async () => {
    if (!selectedVille.nom || selectedVille.nom.trim() === "") {
      toast.error("Le nom de la ville est obligatoire");
      return;
    }

    try {
      const villeCoords = await fetchCoordinatesFromNominatim(
        selectedVille.nom,
      );

      if (!villeCoords) {
        toast.error("Ville introuvable. Vérifiez l’orthographe.");
        return;
      }

      const attractionsWithCoords = [];

      for (const attraction of selectedVille.attractions || []) {
        if (!attraction.nom || attraction.nom.trim() === "") continue;

        const coords = await fetchCoordinatesFromNominatim(
          attraction.nom,
          selectedVille.nom,
        );

        if (!coords) {
          toast.error(
            `Attraction introuvable : "${attraction.nom}". Corrigez ou supprimez-la.`,
          );
          return;
        }

        attractionsWithCoords.push({
          ...attraction,
          latitude: coords.latitude,
          longitude: coords.longitude,
        });
      }

      const villeToSend = {
        ...selectedVille,
        latitude: villeCoords.latitude,
        longitude: villeCoords.longitude,
        attractions: attractionsWithCoords,
      };

      const method = isAdding ? "POST" : "PUT";
      const url = isAdding ? "/api/villes" : `/api/villes/${selectedVille.id}`;

      await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(villeToSend),
      });

      setShowModal(false);
      fetchVilles();
      toast.success(isAdding ? "Ville ajoutée !" : "Ville mise à jour !");
    } catch (err) {
      console.error(err);
      toast.error("Erreur lors de la sauvegarde");
    }
  };
  const importTemplate = async () => {
    const confirmFlush = window.confirm(
      "⚠️ Cette opération va réinitialiser la base de données et supprimer toutes vos données actuelles. Continuer ?",
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
      <ToastContainer position="top-right" autoClose={3000} />
      <div className="admin-header">
        <h1>Administration</h1>
        <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
          <button className="add-btn" onClick={openAddModal}>
            <FontAwesomeIcon icon={faPlus} /> Ajouter une ville
          </button>
          <button className="add-btn" onClick={importTemplate}>
            <FontAwesomeIcon icon={faFileImport} /> Importer le template
          </button>
          <Link to={"/"} className="add-btn">
            <FontAwesomeIcon icon={faFileImport} /> Retour à l'accueil
          </Link>
        </div>
      </div>

      <div className="ville-list">
        {villes.map((ville, index) => (
          <div key={ville.id} className="ville-item">
            <div className="ville-controls">
              <button onClick={() => moveVille(index, -1)}>
                <FontAwesomeIcon icon={faChevronUp} />
              </button>
              <button onClick={() => moveVille(index, 1)}>
                <FontAwesomeIcon icon={faChevronDown} />
              </button>
            </div>
            <div className="ville-name">{ville.nom}</div>
            <div className="ville-actions">
              <button onClick={() => openViewModal(ville)}>
                <FontAwesomeIcon icon={faEye} />
              </button>
              <button onClick={() => openEditModal(ville)}>
                <FontAwesomeIcon icon={faEdit} />
              </button>
              <button onClick={() => deleteVille(ville.id)}>
                <FontAwesomeIcon icon={faTrash} />
              </button>
            </div>
          </div>
        ))}
      </div>

      {showModal && selectedVille && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>
              {isAdding
                ? "Ajouter une ville"
                : isViewing
                ? `Ville: ${selectedVille.nom}`
                : `Modifier: ${selectedVille.nom}`}
            </h2>
            <div className="modal-fields" style={{ marginTop: "25px" }}>
              <label>Nom</label>
              <input
                type="text"
                placeholder="Nom"
                value={selectedVille.nom || ""}
                readOnly={isViewing}
                onChange={(e) =>
                  setSelectedVille({ ...selectedVille, nom: e.target.value })
                }
              />
              {!isAdding && (
                <>
                  <label>Description</label>
                  <textarea
                    placeholder="Description"
                    value={selectedVille.description || ""}
                    readOnly={isViewing}
                    onChange={(e) =>
                      setSelectedVille({
                        ...selectedVille,
                        description: e.target.value,
                      })
                    }
                  />
                  <label>Climat</label>
                  <input
                    type="text"
                    placeholder="Climat"
                    value={selectedVille.climat || ""}
                    readOnly={isViewing}
                    onChange={(e) =>
                      setSelectedVille({
                        ...selectedVille,
                        climat: e.target.value,
                      })
                    }
                  />
                  <label>Meilleure saison</label>
                  <input
                    type="text"
                    placeholder="Meilleure saison"
                    value={selectedVille.meilleure_saison || ""}
                    readOnly={isViewing}
                    onChange={(e) =>
                      setSelectedVille({
                        ...selectedVille,
                        meilleure_saison: e.target.value,
                      })
                    }
                  />

                  <label>Population</label>
                  <input
                    type="number"
                    placeholder="Population"
                    value={selectedVille.population || ""}
                    readOnly={isViewing}
                    onChange={(e) =>
                      setSelectedVille({
                        ...selectedVille,
                        population: e.target.value,
                      })
                    }
                  />

                  {/* Recettes */}
                  <h3>Recettes</h3>
                  {selectedVille.recettes?.map((r, idx) => (
                    <div key={idx} className="modal-item">
                      <input
                        type="text"
                        placeholder="Nom de la recette"
                        value={r.nom}
                        readOnly={isViewing}
                        onChange={(e) => {
                          const newRecettes = [...selectedVille.recettes];
                          newRecettes[idx].nom = e.target.value;
                          setSelectedVille({
                            ...selectedVille,
                            recettes: newRecettes,
                          });
                        }}
                      />
                      {!isViewing && (
                        <button
                          className="delete-btn"
                          onClick={() => {
                            const newRecettes = selectedVille.recettes.filter(
                              (_, i) => i !== idx,
                            );
                            setSelectedVille({
                              ...selectedVille,
                              recettes: newRecettes,
                            });
                          }}
                        >
                          <FontAwesomeIcon icon={faTrash} />
                        </button>
                      )}
                    </div>
                  ))}
                  {!isViewing && (
                    <button
                      className="add-btn"
                      onClick={() => {
                        const newRecettes = selectedVille.recettes
                          ? [...selectedVille.recettes, { nom: "" }]
                          : [{ nom: "" }];
                        setSelectedVille({
                          ...selectedVille,
                          recettes: newRecettes,
                        });
                      }}
                    >
                      <FontAwesomeIcon icon={faPlus} /> Ajouter une recette
                    </button>
                  )}

                  {/* Attractions */}
                  <h3>Attractions</h3>
                  {selectedVille.attractions?.map((a, idx) => (
                    <div key={idx} className="modal-item">
                      <input
                        type="text"
                        placeholder="Nom de l'attraction"
                        value={a.nom}
                        readOnly={isViewing}
                        onChange={(e) => {
                          const newAttractions = [...selectedVille.attractions];
                          newAttractions[idx].nom = e.target.value;
                          setSelectedVille({
                            ...selectedVille,
                            attractions: newAttractions,
                          });
                        }}
                      />
                      {!isViewing && (
                        <button
                          className="delete-btn"
                          onClick={() => {
                            const newAttractions =
                              selectedVille.attractions.filter(
                                (_, i) => i !== idx,
                              );
                            setSelectedVille({
                              ...selectedVille,
                              attractions: newAttractions,
                            });
                          }}
                        >
                          <FontAwesomeIcon icon={faTrash} />
                        </button>
                      )}
                    </div>
                  ))}
                  {!isViewing && (
                    <button
                      className="add-btn"
                      onClick={() => {
                        const newAttractions = selectedVille.attractions
                          ? [...selectedVille.attractions, { nom: "" }]
                          : [{ nom: "" }];
                        setSelectedVille({
                          ...selectedVille,
                          attractions: newAttractions,
                        });
                      }}
                    >
                      <FontAwesomeIcon icon={faPlus} /> Ajouter une attraction
                    </button>
                  )}
                </>
              )}
            </div>

            <div className="modal-buttons">
              <button
                onClick={() => setShowModal(false)}
                className="action-button"
              >
                Fermer
              </button>
              {!isViewing && (
                <button onClick={handleSave} className="action-button">
                  {isAdding ? "Ajouter" : "Enregistrer"}
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Admin;
