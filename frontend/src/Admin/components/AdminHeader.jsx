import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faFileImport } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

export default function AdminHeader({ onAdd, onImport, onDisconnect }) {
  return (
    <div className="admin-header">
      <h1>Administration</h1>
      <button className="add-btn" onClick={onAdd}>
        <FontAwesomeIcon icon={faPlus} /> Ajouter une ville
      </button>
      <button className="add-btn" onClick={onImport}>
        <FontAwesomeIcon icon={faFileImport} /> Importer le template
      </button>
       <button className="add-btn" onClick={onDisconnect}>
        <FontAwesomeIcon icon={faFileImport} /> Déconnexion
      </button>
      <Link to="/" className="add-btn">Retour à l'accueil</Link>
    </div>
  );
}
