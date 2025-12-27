// villes.test.js
import {
  getVilles,
  createVille,
  updateVille,
  deleteVilleById,
  reorderVilles,
  flushAndInsertTemplate,
} from '../Admin/services/villeService';


global.localStorage = (() => {
  let store = {};

  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    removeItem: (key) => { delete store[key]; },
    clear: () => { store = {}; },
  };
})();

global.fetch = jest.fn();


beforeEach(async () => {
  localStorage.clear();

  localStorage.setItem('access_token',"FAKE_JWT_TOKEN");
  console.log(localStorage.getItem("access_token"))
  fetch.mockClear();
});



describe('API villes', () => {
  test('getVilles should fetch villes', async () => {
    const mockData = [{ id: 1, name: 'Paris' }];
    fetch.mockResolvedValueOnce({
      json: jest.fn().mockResolvedValueOnce(mockData),
    });

    const result = await getVilles();

    expect(fetch).toHaveBeenCalledWith('/api/villes');
    expect(result).toEqual(mockData);
  });

  test('createVille should POST a ville', async () => {
    const newVille = { name: 'Lyon' };
    fetch.mockResolvedValueOnce({});

    await createVille(newVille);

    expect(fetch).toHaveBeenCalledWith('/api/villes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': "FAKE_JWT_TOKEN" },
      body: JSON.stringify(newVille),
    });
  });

  test('updateVille should PUT a ville', async () => {
    const updatedVille = { name: 'Marseille' };
    fetch.mockResolvedValueOnce({});

    await updateVille(1, updatedVille);

    expect(fetch).toHaveBeenCalledWith('/api/villes/1', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Authorization': "FAKE_JWT_TOKEN"  },
      body: JSON.stringify(updatedVille),
    });
  });

  test('deleteVilleById should DELETE a ville', async () => {
    fetch.mockResolvedValueOnce({});

    await deleteVilleById(1);

    expect(fetch).toHaveBeenCalledWith('/api/villes/1', { method: 'DELETE' });
  });

  test('reorderVilles should PUT the payload', async () => {
    const payload = [{ id: 1, order: 2 }];
    fetch.mockResolvedValueOnce({});

    await reorderVilles(payload);

    expect(fetch).toHaveBeenCalledWith('/api/villes/reorder', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Authorization': "FAKE_JWT_TOKEN" },
      body: JSON.stringify(payload),
    });
  });

  test('flushAndInsertTemplate should POST to flushDB and insertDATA', async () => {
    fetch.mockResolvedValue({});

    await flushAndInsertTemplate();

    expect(fetch).toHaveBeenNthCalledWith(1, '/api/flushDB', { method: 'POST', headers: { 'Authorization': "FAKE_JWT_TOKEN"} });
    expect(fetch).toHaveBeenNthCalledWith(2, '/api/insertDATA', { method: 'POST', headers: {'Authorization': "FAKE_JWT_TOKEN"} });
  });
});
