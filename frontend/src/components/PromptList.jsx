import { useState, useEffect } from 'react';
import { getPrompts, createPrompt, updatePrompt, deletePrompt } from '../api/prompts';

export default function PromptList({ onOpenPrompt }) {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [creating, setCreating] = useState(false);
  
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');

  useEffect(() => {
    fetchPrompts();
  }, []);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getPrompts();
      setPrompts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (newTitle.trim().length === 0) {
      alert("Prompt başlığı boş olamaz!");
      return;
    }
    if (newTitle.length > 255) {
      alert("Prompt başlığı çok uzun!");
      return;
    }
    if (newContent.trim().length === 0) {
      alert("Prompt içeriği boş olamaz!");
      return;
    }
    
    try {
      setCreating(true);
      await createPrompt(newTitle, newContent);
      setNewTitle('');
      setNewContent('');
      await fetchPrompts();
    } catch (err) {
      alert("Oluşturma hatası: " + err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleEdit = (prompt) => {
    setEditingId(prompt.id);
    setEditTitle(prompt.title);
  };

  const handleUpdate = async (e, id) => {
    e.preventDefault();
    if (editTitle.trim().length === 0) {
      alert("Prompt başlığı boş olamaz!");
      return;
    }
    if (editTitle.length > 255) {
      alert("Prompt başlığı çok uzun!");
      return;
    }

    try {
      await updatePrompt(id, editTitle);
      setEditingId(null);
      await fetchPrompts();
    } catch (err) {
      alert("Güncelleme hatası: " + err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu prompt'u silmek istediğinize emin misiniz?")) return;
    try {
      await deletePrompt(id);
      await fetchPrompts();
    } catch (err) {
      alert("Silme hatası: " + err.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-gray-500">Yükleniyor...</div>;
  if (error) return <div className="text-center py-12 text-red-500">Hata: {error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Prompt Yönetimi</h1>
      
      {/* Create Form */}
      <div className="bg-white p-4 rounded-lg shadow mb-8">
        <h2 className="text-lg font-semibold mb-3">Yeni Prompt Oluştur</h2>
        <form onSubmit={handleCreate} className="space-y-3">
          <input
            type="text"
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Prompt başlığı..."
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            disabled={creating}
          />
          <textarea
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[80px]"
            placeholder="Prompt içeriği (ilk versiyon)..."
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            disabled={creating}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
            disabled={creating}
          >
            {creating ? 'Oluşturuluyor...' : 'Ekle'}
          </button>
        </form>
      </div>

      {/* Prompt List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {prompts.length === 0 ? (
          <div className="p-4 text-gray-500 text-center">Henüz prompt bulunmuyor.</div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {prompts.map(prompt => (
              <li key={prompt.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                {editingId === prompt.id ? (
                  <form onSubmit={(e) => handleUpdate(e, prompt.id)} className="flex-1 flex gap-2 items-center">
                    <input
                      type="text"
                      className="flex-1 border border-gray-300 rounded px-2 py-1"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      autoFocus
                    />
                    <button type="submit" className="text-green-600 hover:text-green-800 font-medium text-sm">
                      Kaydet
                    </button>
                    <button 
                      type="button" 
                      onClick={() => setEditingId(null)}
                      className="text-gray-500 hover:text-gray-700 font-medium text-sm"
                    >
                      İptal
                    </button>
                  </form>
                ) : (
                  <>
                    <div className="flex-1 cursor-pointer" onClick={() => onOpenPrompt(prompt.id)}>
                      <div className="text-gray-800 font-medium hover:text-blue-600 transition-colors">
                        {prompt.title}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        Oluşturuldu: {new Date(prompt.created_at).toLocaleString('tr-TR')} 
                        {prompt.updated_at !== prompt.created_at && 
                          ` (Güncellendi: ${new Date(prompt.updated_at).toLocaleString('tr-TR')})`}
                        {prompt.version_count != null && (
                          <span className="ml-2 bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">
                            {prompt.version_count} versiyon
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-3 ml-4">
                      <button 
                        onClick={() => onOpenPrompt(prompt.id)}
                        className="text-indigo-500 hover:text-indigo-700 text-sm font-medium"
                      >
                        Aç
                      </button>
                      <button 
                        onClick={() => handleEdit(prompt)}
                        className="text-blue-500 hover:text-blue-700 text-sm font-medium"
                      >
                        Düzenle
                      </button>
                      <button 
                        onClick={() => handleDelete(prompt.id)}
                        className="text-red-500 hover:text-red-700 text-sm font-medium"
                      >
                        Sil
                      </button>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
