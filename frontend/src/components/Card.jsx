import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const Card = ({ ville }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    if (!ville) return;

    // Initialiser la carte
    const map = L.map(mapRef.current, {
      center: [ville.latitude, ville.longitude],
      zoom: 12,
    });

    // Ajouter les tuiles OSM
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
      maxZoom: 19,
    }).addTo(map);

    // Ajouter un marqueur pour chaque attraction
    ville.attractions.forEach((attraction) => {
      if (attraction.latitude && attraction.longitude) {
        L.marker([attraction.latitude, attraction.longitude])
          .addTo(map)
          .bindPopup(`<b>${attraction.nom}</b><br>${attraction.description}`);
      }
    });

    // Ajuster la vue pour inclure tous les marqueurs
    const latLngs = ville.attractions
      .filter((a) => a.latitude && a.longitude)
      .map((a) => [a.latitude, a.longitude]);
    if (latLngs.length) {
      const bounds = L.latLngBounds(latLngs);
      map.fitBounds(bounds, { padding: [50, 50] });
    }

    return () => map.remove();
  }, [ville]);

  return (
    <div className="container">
      <div className="header">
        <h1>🇯🇵 {ville.nom}</h1>
        <p>{ville.description}</p>
      </div>

      <div className="content">
        <div className="info-section">
          <h2>📊 Informations</h2>
          <p>
            <strong>Population:</strong> {ville.population}
          </p>
          <p>
            <strong>Coordonnées:</strong> {ville.latitude}°N, {ville.longitude}
            °E
          </p>

          <div style={{ marginTop: "20px" }}>
            <h3>🌤️ Climat</h3>
            <p>
              <strong>Climat:</strong> {ville.climat}
            </p>
            <p>
              <strong>Meilleure saison:</strong> {ville.meilleure_saison}
            </p>
          </div>
          <div className="food-section" style={{ flex: 1, marginTop: "25px" }}>
            <h2>🥡 Spécialités culinaires</h2>
            {ville.recettes.map((recette, idx) => (
              <div
                key={idx}
                className="recette-card"
                style={{
                  marginBottom: "15px",
                  padding: "10px",
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  marginTop: "25px",
                }}
              >
                <h4>{recette.nom}</h4>
                <p>{recette.description}</p>
                <div
                  className="ingredients"
                  style={{ display: "flex", flexWrap: "wrap", gap: "5px" }}
                >
                  {recette.ingredients
                    .replace(/[{}]/g, "")
                    .split(",")
                    .map((ing, i) => (
                      <span
                        key={i}
                        className="ingredient-tag"
                        style={{
                          background: "#eef",
                          padding: "3px 8px",
                          borderRadius: "12px",
                          fontSize: "0.85rem",
                        }}
                      >
                        {ing.replace(/^"|"$/g, "").trim()}
                      </span>
                    ))}
                </div>
              </div>
            ))}
          </div>
          <Link to="/" className="back-btn">
            ← Retour à la carte
          </Link>
        </div>

        <div className="attractions-section">
          <h2>📍Points d'intérêts</h2>
          <ul className="attractions-list">
            {ville.attractions.map((attraction) => (
              <li key={attraction.id} className="attraction-item">
                <h4 className="attraction-name">{attraction.nom}</h4>
                <p className="attraction-description">
                  {attraction.description}
                </p>
                {attraction.latitude && attraction.longitude && (
                  <a
                    href={`https://www.google.com/maps?q=${attraction.latitude},${attraction.longitude}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Y aller
                  </a>
                )}
              </li>
            ))}
          </ul>

          <div
            className="map-container"
            style={{ height: "400px", marginTop: "20px" }}
            ref={mapRef}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default Card;
