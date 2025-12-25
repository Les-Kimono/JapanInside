import "./infoPanel.css"

const SpecialitesModal = ({ show, onClose, specialites }) => {
  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3>Spécialités Japonaises</h3>
          <span className="close-btn" onClick={onClose}>×</span>
        </div>
        <ul className="specialites-list">
          {specialites.map((meal) => (
            <li key={meal.idMeal}>
              <img src={meal.strMealThumb} alt={meal.strMeal} className="meal-thumb" /> {meal.strMeal}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SpecialitesModal;
