import { useState, useEffect } from 'react';
import { getVersions, createVersion, compareDiff } from '../api/versions';
import { updatePrompt } from '../api/prompts';
import { getTags, attachTagToPrompt, removeTagFromPrompt } from '../api/tags';
import DiffViewer from './DiffViewer';

export default function PromptDetail({ promptId, onBack }) {
  const [prompt, setPrompt] = useState(null);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // New version form
  const [newContent, setNewContent] = useState('');
  const [creating, setCreating] = useState(false);

  // Title editing
  const [editingTitle, setEditingTitle] = useState(false);
  const [editTitle, setEditTitle] = useState('');

  // Version comparison selection
  const [compareA, setCompareA] = useState(null);
  const [compareB, setCompareB] = useState(null);

  // Diff result
  const [diffResult, setDiffResult] = useState(null);
  const [diffLoading, setDiffLoading] = useState(false);
  const [diffError, setDiffError] = useState(null);

  // Tagging
  const [allTags, setAllTags] = useState([]);
  const [newTagName, setNewTagName] = useState('');
  const [tagError, setTagError] = useState(null);

  useEffect(() => {
    fetchData();
    fetchAllTags();
  }, [promptId]);

  const fetchAllTags = async () => {
    try {
      const tags = await getTags();
      setAllTags(tags);
    } catch (err) {
      console.error("Etiketler alınamadı:", err);
    }
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch prompt detail
      const promptRes = await fetch(`http://127.0.0.1:8000/prompts/${promptId}`);
      if (!promptRes.ok) throw new Error('Prompt bulunamadı');
      const promptData = await promptRes.json();
      setPrompt(promptData);

      // Fetch versions
      const versionData = await getVersions(promptId);
      setVersions(versionData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddVersion = async (e) => {
    e.preventDefault();
    if (newContent.trim().length === 0) {
      alert("Versiyon içeriği boş olamaz!");
      return;
    }
    try {
      setCreating(true);
      await createVersion(promptId, newContent);
      setNewContent('');
      await fetchData();
    } catch (err) {
      alert("Versiyon ekleme hatası: " + err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleTitleEdit = async (e) => {
    e.preventDefault();
    if (editTitle.trim().length === 0) {
      alert("Başlık boş olamaz!");
      return;
    }
    try {
      await updatePrompt(promptId, editTitle);
      setEditingTitle(false);
      await fetchData();
    } catch (err) {
      alert("Güncelleme hatası: " + err.message);
    }
  };

  const handleCompareToggle = (versionNo) => {
    if (compareA === versionNo) {
      setCompareA(null);
    } else if (compareB === versionNo) {
      setCompareB(null);
    } else if (compareA === null) {
      setCompareA(versionNo);
    } else if (compareB === null) {
      setCompareB(versionNo);
    } else {
      // Both slots full — replace the older selection (A)
      setCompareA(compareB);
      setCompareB(versionNo);
    }
  };

  const isSelected = (versionNo) => compareA === versionNo || compareB === versionNo;
  const canCompare = compareA !== null && compareB !== null;

  const handleCompare = async () => {
    const vA = Math.min(compareA, compareB);
    const vB = Math.max(compareA, compareB);
    try {
      setDiffLoading(true);
      setDiffError(null);
      const result = await compareDiff(promptId, vA, vB);
      setDiffResult(result);
    } catch (err) {
      setDiffError(err.message);
      setDiffResult(null);
    } finally {
      setDiffLoading(false);
    }
  };

  const handleRemoveTag = async (tagId) => {
    try {
      await removeTagFromPrompt(promptId, tagId);
      setPrompt(prev => ({ ...prev, tags: prev.tags.filter(t => t.id !== tagId) }));
    } catch (err) {
      alert("Etiket silinemedi: " + err.message);
    }
  };

  const handleAddTag = async (e) => {
    e.preventDefault();
    setTagError(null);
    if (!newTagName.trim()) return;
    
    try {
      const addedTag = await attachTagToPrompt(promptId, newTagName);
      // Avoid duplicate rendering if already attached
      if (!prompt.tags.find(t => t.id === addedTag.id)) {
        setPrompt(prev => ({ ...prev, tags: [...prev.tags, addedTag] }));
      }
      setNewTagName('');
      fetchAllTags(); // refresh tag list for datalist
    } catch (err) {
      setTagError(err.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-gray-500">Yükleniyor...</div>;
  if (error) return (
    <div className="max-w-4xl mx-auto p-4">
      <button onClick={onBack} className="text-blue-500 hover:text-blue-700 mb-4 inline-block">&larr; Geri</button>
      <div className="text-red-500">Hata: {error}</div>
    </div>
  );

  const latestVersion = versions.length > 0 ? versions[versions.length - 1] : null;

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Back button */}
      <button onClick={onBack} className="text-blue-500 hover:text-blue-700 mb-4 inline-flex items-center gap-1 text-sm font-medium">
        &larr; Prompt Listesi
      </button>

      <datalist id="tags-list">
        {allTags.map(tag => <option key={tag.id} value={tag.name} />)}
      </datalist>

      {/* Prompt Header */}
      <div className="bg-white p-5 rounded-lg shadow mb-6">
        {editingTitle ? (
          <form onSubmit={handleTitleEdit} className="flex gap-2 items-center">
            <input
              type="text"
              className="flex-1 border border-gray-300 rounded px-3 py-2 text-xl font-bold focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              autoFocus
            />
            <button type="submit" className="text-green-600 hover:text-green-800 font-medium text-sm">Kaydet</button>
            <button type="button" onClick={() => setEditingTitle(false)} className="text-gray-500 hover:text-gray-700 font-medium text-sm">İptal</button>
          </form>
        ) : (
          <div>
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-bold text-gray-800">{prompt.title}</h1>
              <button
                onClick={() => { setEditingTitle(true); setEditTitle(prompt.title); }}
                className="text-blue-500 hover:text-blue-700 text-sm font-medium"
              >
                Düzenle
              </button>
            </div>
            
            {/* Tags Section */}
            <div className="mt-3 flex items-center flex-wrap gap-2">
              {prompt.tags && prompt.tags.map(tag => (
                <span key={tag.id} className="inline-flex items-center gap-1 bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded-full uppercase tracking-wide font-semibold">
                  {tag.name}
                  <button 
                    onClick={() => handleRemoveTag(tag.id)} 
                    className="hover:text-purple-900 focus:outline-none"
                    title="Etiketi Kaldır"
                  >
                    &times;
                  </button>
                </span>
              ))}
              
              <form onSubmit={handleAddTag} className="flex items-center ml-1">
                <input
                  type="text"
                  list="tags-list"
                  value={newTagName}
                  onChange={(e) => setNewTagName(e.target.value)}
                  placeholder="Etiket ekle..."
                  className="border border-gray-300 rounded-l px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500 w-28"
                />
                <button 
                  type="submit" 
                  className="bg-gray-100 hover:bg-gray-200 border border-l-0 border-gray-300 rounded-r px-2 py-1 text-xs font-medium text-gray-600"
                >
                  +
                </button>
              </form>
              {tagError && <span className="text-red-500 text-xs ml-2">{tagError}</span>}
            </div>
          </div>
        )}
        <div className="text-xs text-gray-400 mt-2">
          Oluşturuldu: {new Date(prompt.created_at).toLocaleString('tr-TR')}
          {prompt.updated_at !== prompt.created_at &&
            ` · Güncellendi: ${new Date(prompt.updated_at).toLocaleString('tr-TR')}`}
          <span className="ml-2 bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{versions.length} versiyon</span>
        </div>
      </div>

      {/* Latest Content */}
      {latestVersion && (
        <div className="bg-white p-5 rounded-lg shadow mb-6">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Güncel İçerik <span className="text-gray-400 font-normal">(v{latestVersion.version_no})</span>
          </h2>
          <pre className="whitespace-pre-wrap text-gray-700 bg-gray-50 p-3 rounded border border-gray-200 text-sm leading-relaxed">
            {latestVersion.content}
          </pre>
        </div>
      )}

      {/* New Version Form */}
      <div className="bg-white p-5 rounded-lg shadow mb-6">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Yeni Versiyon Ekle</h2>
        <form onSubmit={handleAddVersion} className="space-y-3">
          <textarea
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px] text-sm"
            placeholder="Yeni versiyon içeriği..."
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            disabled={creating}
          />
          <button
            type="submit"
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-green-300 text-sm font-medium"
            disabled={creating}
          >
            {creating ? 'Ekleniyor...' : 'Versiyon Ekle'}
          </button>
        </form>
      </div>

      {/* Version History */}
      <div className="bg-white rounded-lg shadow overflow-hidden mb-6">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Versiyon Geçmişi</h2>
          {canCompare && (
            <button
              onClick={handleCompare}
              className="bg-indigo-500 text-white px-3 py-1.5 rounded hover:bg-indigo-600 text-sm font-medium transition-colors"
            >
              Karşılaştır (v{Math.min(compareA, compareB)} ↔ v{Math.max(compareA, compareB)})
            </button>
          )}
          {!canCompare && (compareA !== null || compareB !== null) && (
            <span className="text-xs text-gray-400">Karşılaştırma için 1 versiyon daha seçin</span>
          )}
        </div>

        {versions.length === 0 ? (
          <div className="p-4 text-gray-500 text-center">Henüz versiyon bulunmuyor.</div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {[...versions].reverse().map(v => (
              <li
                key={v.id}
                className={`p-4 hover:bg-gray-50 transition-colors cursor-pointer ${isSelected(v.version_no) ? 'bg-indigo-50 border-l-4 border-indigo-400' : ''}`}
                onClick={() => handleCompareToggle(v.version_no)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-bold ${isSelected(v.version_no) ? 'text-indigo-600' : 'text-gray-700'}`}>
                        v{v.version_no}
                      </span>
                      {v.version_no === latestVersion.version_no && (
                        <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-medium">güncel</span>
                      )}
                      {isSelected(v.version_no) && (
                        <span className="text-xs bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded font-medium">
                          {compareA === v.version_no ? 'A' : 'B'}
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {new Date(v.created_at).toLocaleString('tr-TR')}
                    </div>
                    <div className="text-sm text-gray-600 mt-2 line-clamp-2">
                      {v.content.length > 120 ? v.content.substring(0, 120) + '…' : v.content}
                    </div>
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    <input
                      type="checkbox"
                      checked={isSelected(v.version_no)}
                      onChange={() => handleCompareToggle(v.version_no)}
                      onClick={(e) => e.stopPropagation()}
                      className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Diff Result */}
      {diffLoading && (
        <div className="bg-white p-5 rounded-lg shadow mb-6 text-center text-gray-500">
          Karşılaştırma hesaplanıyor...
        </div>
      )}
      {diffError && (
        <div className="bg-white p-5 rounded-lg shadow mb-6">
          <div className="text-red-500">Karşılaştırma hatası: {diffError}</div>
        </div>
      )}
      {diffResult && !diffLoading && (
        <DiffViewer
          diff={diffResult.diff}
          versionA={diffResult.version_a}
          versionB={diffResult.version_b}
        />
      )}
    </div>
  );
}
