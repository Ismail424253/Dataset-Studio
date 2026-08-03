const API_BASE_URL = 'http://127.0.0.1:8000';

export async function getTags() {
  const response = await fetch(`${API_BASE_URL}/tags`);
  if (!response.ok) {
    throw new Error('Etiketler alınamadı');
  }
  return response.json();
}

export async function attachTagToPrompt(promptId, tagName) {
  const response = await fetch(`${API_BASE_URL}/prompts/${promptId}/tags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tag_name: tagName })
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Etiket eklenemedi');
  }
  return response.json();
}

export async function removeTagFromPrompt(promptId, tagId) {
  const response = await fetch(`${API_BASE_URL}/prompts/${promptId}/tags/${tagId}`, {
    method: 'DELETE'
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Etiket silinemedi');
  }
  return true;
}
