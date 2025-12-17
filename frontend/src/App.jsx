const API_URL = "http://localhost:8000";

function App() {
    return (
        <iframe
            src={`${API_URL}/api/carte`}
            title="Carte du Japon"
            style={{ width:"100vw", height:"100vh", border:"none" }}
        />
    );
}

export default App;