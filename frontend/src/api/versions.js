const API_BASE_URL = 'http://127.0.0.1:8000';

export async function getVersions(promptId) {
  const response = await fetch(`${API_BASE_URL}/prompts/${promptId}/versions`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to fetch versions');
  }
  return response.json();
}

export async function getVersion(promptId, versionNo) {
  const response = await fetch(`${API_BASE_URL}/prompts/${promptId}/versions/${versionNo}`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to fetch version');
  }
  return response.json();
}

export async function createVersion(promptId, content) {
  const response = await fetch(`${API_BASE_URL}/prompts/${promptId}/versions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content })
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to create version');
  }
  return response.json();
}
