const API_BASE_URL = 'http://127.0.0.1:8000';

export async function getPrompts() {
  const response = await fetch(`${API_BASE_URL}/prompts`);
  if (!response.ok) {
    throw new Error('Prompts fetch failed');
  }
  return response.json();
}

export async function createPrompt(title, content) {
  const response = await fetch(`${API_BASE_URL}/prompts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, content })
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to create prompt');
  }
  return response.json();
}

export async function updatePrompt(id, title) {
  const response = await fetch(`${API_BASE_URL}/prompts/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title })
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to update prompt');
  }
  return response.json();
}

export async function deletePrompt(id) {
  const response = await fetch(`${API_BASE_URL}/prompts/${id}`, {
    method: 'DELETE'
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to delete prompt');
  }
  // DELETE /prompts/{id} returns 204 No Content
  return true;
}
