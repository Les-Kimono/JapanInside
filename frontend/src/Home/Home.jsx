import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import Map from "./components/Map/Map.jsx";
import VilleInfoPanel from "./components/VilleInfoPanel.jsx";
import SpecialitesModal from "./components/SpecialitesModal.jsx";

const Home = () => {
  const [ville, setVille] = useState(null);
  const [villes, setVilles] = useState([]);
  const [showSpecialitesModal, setShowSpecialitesModal] = useState(false);
  const [specialitesJP, setSpecialitesJP] = useState([]);

 

  const onVilleClick = useCallback((nom) => {
    if (!nom) return setVille(null);

    fetch(`/api/villes/${nom}`)
      .then((res) => res.ok ? res.json() : Promise.reject("Ville non trouvée"))
      .then((data) => setVille({ ...data }))
      .catch((err) => setVille({ nom, error: err.toString() }));
  }, []);

useEffect(() => {
  const fetchVilles = async () => {
    try {
      const res = await fetch("/api/villes");
      const data = await res.json();
      setVilles(data);
    } catch (err) {
      console.error("Erreur récupération villes :", err);
    }
  };

  fetchVilles();
}, []);

  useEffect(() => {
    const fetchSpecialites = async () => {
      try {
        const res = await fetch("https://www.themealdb.com/api/json/v1/1/filter.php?a=japanese");
        const data = await res.json();
        setSpecialitesJP(data.meals || []);
      } catch (err) {
        console.error("Erreur chargement spécialités :", err);
      }
    };
    fetchSpecialites();
  }, []);

  return (
    <>
      <SpecialitesModal show={showSpecialitesModal} onClose={() => setShowSpecialitesModal(false)} specialites={specialitesJP} />
      <Map villes={villes} onVilleClick={onVilleClick} />
      <VilleInfoPanel ville={ville} onClose={() => setVille(null)} />

      <div style={{ position: "absolute", top: 10, right: 10, display: "flex", flexDirection: "column", gap: "10px" }}>
        <button className="specialites-btn" onClick={() => setShowSpecialitesModal(true)}>Spécialités Japonaises</button>
    <Link
          to={'/admin'}
          className="admin-btn"
          style={{
            position: "fixed",
            top:"15px",
            right:"25px",
            zIndex:999,
            background: "#667eea",
            color: "white",
            padding: "8px 12px",
            borderRadius: "6px",
            textDecoration: "none",
            fontWeight: "bold",
            boxShadow: "0 2px 5px rgba(0,0,0,0.2)"
          }}
        >
          Administration
        </Link>
      </div>

      <div className="map-title">
        <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
        <p>{villes.map((v) => v.nom).join(" → ")}</p>
      </div>
    </>
  );
};

export default Home;
