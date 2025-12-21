import { useEffect, useRef, useState, useCallback } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapStyle.css";
import { Link } from "react-router-dom";

const Home = () => {
  const [ville, setVille] = useState(null);
  const [villes, setVilles] = useState([]);
  const [showSpecialitesModal, setShowSpecialitesModal] = useState(false);

  const mapRef = useRef(null);

  const getVilles = async () => {
    const res = await fetch("/api/villes");
    const data = await res.json();
    setVilles(data);
    return data;
  };

  const onVilleClick = useCallback((nom) => {
    fetch(`/api/villes/${nom}`)
      .then((res) => {
        if (!res.ok) throw new Error("Ville non trouvée");
        return res.json();
      })
      .then((data) => {
        setVille({ ...data });
        if (mapRef.current) {
          mapRef.current.setView([data.latitude, data.longitude], 10);
        }
      })
      .catch((err) => {
        console.error(err);
        setVille({ nom, error: err.message });
      });
  }, []);
useEffect(() => {
  if (mapRef.current) return; 

  const map = L.map("map").setView([36.2048, 138.2529], 6);
  mapRef.current = map;

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
    maxZoom: 12,
    minZoom: 5,
  }).addTo(map);

  map.setMaxBounds([[30, 128], [46, 146]]);
  map.on("click", () => setVille(null));

  (async () => {
    const villesData = await getVilles(); 
    const points = [];

    villesData.forEach((v) => {
      points.push([v.latitude, v.longitude]);

      const icon = L.icon({
        iconUrl:
          "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
        shadowUrl:
          "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [30, 46],
        iconAnchor: [15, 46],
        popupAnchor: [0, -46],
      });

      L.marker([v.latitude, v.longitude], { icon, title: v.nom })
        .addTo(map)
        .on("click", () => onVilleClick(v.nom));
    });

    if (points.length) {
      L.polyline(points, {
        color: "#667eea",
        weight: 4,
        opacity: 0.8,
        dashArray: "10,10",
        lineCap: "round",
      }).addTo(map);
    }
  })();
}, [onVilleClick]);
const [specialitesJP, setSpecialitesJP] = useState([])
const getSpecialitesJP = async () => {
    try {
      const res = await fetch(
        "https://www.themealdb.com/api/json/v1/1/filter.php?a=japanese"
      );
      const data = await res.json();
      console.log(data.meals)
      setSpecialitesJP(data.meals || []);
    } catch (err) {
      console.error("Erreur chargement spécialités :", err);
    }
  };
useEffect(() => {
  getSpecialitesJP()
}, [])

  return (
    <>


{showSpecialitesModal && (
  <div className="modal-overlay">
    <div className="modal">
      <div className="modal-header">
        <h3>Spécialités Japonaises</h3>
        <span
          className="close-btn"
          onClick={() => setShowSpecialitesModal(false)}
        >
          ×
        </span>
      </div>
      <ul className="specialites-list">
        {specialitesJP.map((meal) => (
          <li key={meal.idMeal}>
            <img
              src={meal.strMealThumb}
              alt={meal.strMeal}
              className="meal-thumb"
            />{" "}
            {meal.strMeal}
          </li>
        ))}
      </ul>
    </div>
  </div>
)}



        <div style={{
        position: "absolute",
        top: 10,
        right: 10
      }}>


        <button
  className="specialites-btn"
  onClick={() => setShowSpecialitesModal(true)}
>
  Spécialités Japonaisesss
</button>
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
   
  

      <div id="map" style={{ width: "100vw", height: "100vh" }}></div>

      {ville && (
        <div id="infoPanel" className="info-panel">
          <div className="info-header">
            <h3>
              {ville.nom} {ville.icon}
            </h3>
            <span className="close-btn" onClick={() => setVille(null)}>
              ×
            </span>
          </div>
          <div className="ville-details">
            {ville.error ? (
              <p>Impossible de charger les détails: {ville.error}</p>
            ) : (
              <>
                <p>
                  <strong>Description:</strong> {ville.description}
                </p>
                <p>
                  <strong>Population:</strong> {ville.population}
                </p>
                <p>
                  <strong>Étape {ville.position} sur 6</strong>
                </p>
                <div className="info-grid">
                  <div className="info-item">
                    <strong>📍 Coordonnées:</strong>{" "}
                    {ville.latitude.toFixed(4)}°N, {ville.longitude.toFixed(4)}°E
                  </div>
                  <div className="info-item">
                    <strong>🌤️ Climat:</strong> {ville.climat}
                  </div>
                  <div className="info-item">
                    <strong>🌸 Meilleure saison:</strong>{" "}
                    {ville.meilleure_saison}
                  </div>
                </div>
                <p>
                  <strong>🥡 Spécialités culinaires:</strong>
                </p>
                <ul className="attractions-list">
                  {ville.recettes?.map((r) => (
                    <li key={r.id}>{r.nom}</li>
                  ))}
                </ul>
                <p>
                  <strong>🏛️ Attractions principales:</strong>
                </p>
                <ul className="attractions-list">
                  {ville.attractions?.map((a) => (
                    <li key={a.id}>{a.nom}</li>
                  ))}
                </ul>
                <a
                  href={`https://www.google.com/maps?q=${ville.latitude},${ville.longitude}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  Voir {ville.nom} sur Google Maps
                </a>
                <a className="action-btn" href={`/ville/${ville.nom.toLowerCase()}`}>
                  <i className="fas fa-external-link-alt"></i> Voir la page complète
                </a>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default Home;
