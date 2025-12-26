import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faPlus } from "@fortawesome/free-solid-svg-icons";

export default function VilleModal({
  mode, // "view" | "edit" | "add"
  ville,
  setVille,
  onClose,
  onSave,
}) {
  const isViewing = mode === "view";
  const isAdding = mode === "add";

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>
          {isAdding
            ? "Ajouter une ville"
            : isViewing
            ? `Ville : ${ville.nom}`
            : `Modifier : ${ville.nom}`}
        </h2>

        <div className="modal-fields">
          <label>Nom</label>
          <input
            type="text"
            value={ville.nom || ""}
            readOnly={isViewing}
            onChange={(e) =>
              setVille({ ...ville, nom: e.target.value })
            }
          />

          {!isAdding && (
            <>
              <label>Description</label>
              <textarea
                value={ville.description || ""}
                readOnly={isViewing}
                onChange={(e) =>
                  setVille({ ...ville, description: e.target.value })
                }
              />

              <label>Climat</label>
              <input
                value={ville.climat || ""}
                readOnly={isViewing}
                onChange={(e) =>
                  setVille({ ...ville, climat: e.target.value })
                }
              />

              <label>Meilleure saison</label>
              <input
                value={ville.meilleure_saison || ""}
                readOnly={isViewing}
                onChange={(e) =>
                  setVille({
                    ...ville,
                    meilleure_saison: e.target.value,
                  })
                }
              />

              <label>Population</label>
              <input
                type="number"
                value={ville.population || ""}
                readOnly={isViewing}
                onChange={(e) =>
                  setVille({ ...ville, population: e.target.value })
                }
              />

              {/* RECETTES */}
              <h3>Recettes</h3>
              {ville.recettes?.map((r, idx) => (
                <div key={idx} className="modal-item">
                  <input
                    value={r.nom}
                    readOnly={isViewing}
                    onChange={(e) => {
                      const recettes = [...ville.recettes];
                      recettes[idx].nom = e.target.value;
                      setVille({ ...ville, recettes });
                    }}
                  />
                  {!isViewing && (
                    <button
                      onClick={() =>
                        setVille({
                          ...ville,
                          recettes: ville.recettes.filter(
                            (_, i) => i !== idx
                          ),
                        })
                      }
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </button>
                  )}
                </div>
              ))}
              {!isViewing && (
                <button
                  className="add-btn"
                  onClick={() =>
                    setVille({
                      ...ville,
                      recettes: [...(ville.recettes || []), { nom: "" }],
                    })
                  }
                >
                  <FontAwesomeIcon icon={faPlus} /> Ajouter une recette
                </button>
              )}

              {/* ATTRACTIONS */}
              <h3>Attractions</h3>
              {ville.attractions?.map((a, idx) => (
                <div key={idx} className="modal-item">
                  <input
                    value={a.nom}
                    readOnly={isViewing}
                    onChange={(e) => {
                      const attractions = [...ville.attractions];
                      attractions[idx].nom = e.target.value;
                      setVille({ ...ville, attractions });
                    }}
                    placeholder="Nom"
                  />
                  <input
                    value={a.description}
                    readOnly={isViewing}
                    onChange={(e) => {
                      const attractions = [...ville.attractions];
                      attractions[idx].description = e.target.value;
                      setVille({ ...ville, attractions });
                    }}
                    placeholder="Description"
                  />
                  {!isViewing && (
                    <button
                      onClick={() =>
                        setVille({
                          ...ville,
                          attractions: ville.attractions.filter(
                            (_, i) => i !== idx
                          ),
                        })
                      }
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </button>
                  )}
                </div>
              ))}
              {!isViewing && (
                <button
                  className="add-btn"
                  onClick={() =>
                    setVille({
                      ...ville,
                      attractions: [
                        ...(ville.attractions || []),
                        { nom: "" },
                      ],
                    })
                  }
                >
                  <FontAwesomeIcon icon={faPlus} /> Ajouter une attraction
                </button>
              )}
            </>
          )}
        </div>

        <div className="modal-buttons">
          <button onClick={onClose} className="add-btn close-btn">Fermer</button>
          {!isViewing && (
            <button onClick={onSave} className="add-btn save-btn">
              {isAdding ? "Ajouter" : "Enregistrer"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
