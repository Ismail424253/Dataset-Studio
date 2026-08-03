import { useState } from 'react'
import PromptList from './components/PromptList'
import PromptDetail from './components/PromptDetail'

function App() {
  const [selectedPromptId, setSelectedPromptId] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 py-8 font-sans">
      {selectedPromptId === null ? (
        <PromptList onOpenPrompt={(id) => setSelectedPromptId(id)} />
      ) : (
        <PromptDetail
          promptId={selectedPromptId}
          onBack={() => setSelectedPromptId(null)}
        />
      )}
    </div>
  )
}

export default App
