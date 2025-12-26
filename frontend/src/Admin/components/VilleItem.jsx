import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faTrash, faEye, faEdit, faChevronUp, faChevronDown
} from "@fortawesome/free-solid-svg-icons";

export default function VilleItem({ ville, index, onMove, onView, onEdit, onDelete }) {
  return (
    <div className="ville-item">
      <div style={{flex: 1, display: "flex", alignItems: "center", gap: "15px"}}>
      <div className="ville-controls">
        <button onClick={() => onMove(index, -1)}><FontAwesomeIcon icon={faChevronUp} /></button>
        <button onClick={() => onMove(index, 1)}><FontAwesomeIcon icon={faChevronDown} /></button>
      </div>
      <div className="ville-name">{ville.nom}</div>
      </div>
      <div className="ville-actions">
        <button onClick={() => onView(ville)}><FontAwesomeIcon icon={faEye} /></button>
        <button onClick={() => onEdit(ville)}><FontAwesomeIcon icon={faEdit} /></button>
        <button onClick={() => onDelete(ville.id)}><FontAwesomeIcon icon={faTrash} /></button>
      </div>
    </div>
  );
}
