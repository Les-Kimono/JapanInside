import "./infoPanel.css";

const VilleInfoPanel = ({ ville, onClose }) => {
  if (!ville) return null;

  return (
    <div id="infoPanel" className="info-panel">
      <div className="info-header">
        <h3>{ville.nom}</h3>
        <span className="close-btn" onClick={onClose}>×</span>
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
              <div className="info-item">
                <strong>📍 Coordonnées:</strong> {ville.latitude.toFixed(4)}°N, {ville.longitude.toFixed(4)}°E
              </div>
              <div className="info-item">
                <strong>🌤️ Climat:</strong> {ville.climat}
              </div>
              <div className="info-item">
                <strong>🌸 Meilleure saison:</strong> {ville.meilleure_saison}
              </div>
            </div>

            <p><strong>🥡 Spécialités culinaires:</strong></p>
            <ul className="attractions-list">
              {ville.recettes?.map((r) => <li key={r.id}>{r.nom}</li>)}
            </ul>

            <p><strong>🏛️ Attractions principales:</strong></p>
            <ul className="attractions-list">
              {ville.attractions?.map((a) => <li key={a.id}>{a.nom}</li>)}
            </ul>

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
  );
};

export default VilleInfoPanel;
