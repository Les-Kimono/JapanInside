import { useEffect, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapStyle.css";

const Home = () => {
  const [ville, setVille] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);

  const [villes, setVilles] = useState({});




  const onVilleClick = (nom) => {
    fetch(`/api/villes/${nom}`)
      .then(res => {
        if (!res.ok) throw new Error("Ville non trouvée");
        return res.json();
      })
      .then(data => {
        
        // On ajoute les infos du marker pour l'affichage
        setVille({ ...data});
        if (mapInstance) {
          mapInstance.setView([data.latitude, data.longitude], 10);
        }
      })
      .catch(err => {
        console.error(err);
        setVille({ nom, error: err.message });
      });
  };
async function getVilles() {
  const res = await fetch('/api/villes');
  const data = await res.json();
  setVilles(data);
  return data;
}
  useEffect(() => {
    const map = L.map("map").setView([36.2048, 138.2529], 6);
    setMapInstance(map);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
      maxZoom: 12,
      minZoom: 5
    }).addTo(map);

    map.setMaxBounds([[30, 128], [46, 146]]);

    const points = [];
 getVilles().then(villes => {
 
  villes.forEach(v => {

 
      points.push([v.latitude, v.longitude]);

      const icon = L.icon({
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png`,
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [30, 46],
        iconAnchor: [15, 46],
        popupAnchor: [0, -46]
      });

      const marker = L.marker([v.latitude, v.longitude], { icon, title: v.nom }).addTo(map);
      marker.on("click", () => onVilleClick(v.nom));
   })
});
    L.polyline(points, { color: "#667eea", weight: 4, opacity: 0.8, dashArray: "10,10", lineCap: "round" }).addTo(map);

    map.on("click", () => setVille(null));

    return () => map.remove();
  }, []);

  return (
    <>
      <div className="map-title">
        <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
    
<p>
  {villes && villes.map(v => v.nom).join(" → ")}
</p>
      </div>
      <div id="map" style={{ width: "100vw", height: "100vh" }}></div>

      {ville && (
        <div id="infoPanel" className="info-panel">
          <div className="info-header">
            <h3>
              {ville.nom} {ville.icon}
            </h3>
            <span className="close-btn" onClick={() => setVille(null)}>×</span>
          </div>
          <div className="ville-details">
            {ville.error ? (
              <p>Impossible de charger les détails: {ville.error}</p>
            ) : (
              <>
                <p><strong>Description:</strong> {ville.description}</p>
                <p><strong>Population:</strong> {ville.population}</p>
                <p><strong>Étape {ville.position} sur 6</strong></p>
                <div className="info-grid">
                  <div className="info-item"><strong>📍 Coordonnées:</strong> {ville.latitude.toFixed(4)}°N, {ville.longitude.toFixed(4)}°E</div>
                  <div className="info-item"><strong>🌤️ Climat:</strong> {ville.climat}</div>
                  <div className="info-item"><strong>🌸 Meilleure saison:</strong> {ville.meilleure_saison}</div>
                </div>
                <p><strong>🥡 Spécialités culinaires:</strong></p>
                <ul className="attractions-list">{ville.recettes?.map(r => <li key={r.id}>{r.nom}</li>)}</ul>
                <p><strong>🏛️ Attractions principales:</strong></p>
                <ul className="attractions-list">{ville.attractions?.map(a => <li key={a.id}>{a.nom}</li>)}</ul>
                <a href={`https://www.google.com/maps?q=${ville.latitude},${ville.longitude}`} target="_blank" rel="noreferrer">
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
