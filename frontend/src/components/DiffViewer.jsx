/**
 * DiffViewer — Iki versiyon arasindaki farklari gorsel olarak gosteren bilesen.
 *
 * Props:
 *   diff       : Array<{type: "unchanged"|"added"|"removed", text: string}>
 *   versionA   : number (sol versiyon numarasi)
 *   versionB   : number (sag versiyon numarasi)
 */
export default function DiffViewer({ diff, versionA, versionB }) {
  // Ozet istatistikleri hesapla
  const added = diff.filter(l => l.type === 'added').length;
  const removed = diff.filter(l => l.type === 'removed').length;
  const hasChanges = added > 0 || removed > 0;

  // Satir numaralari: A (eski) ve B (yeni) icin ayri sayaclar
  let lineA = 0;
  let lineB = 0;
  const lines = diff.map((line, idx) => {
    let numA = '';
    let numB = '';
    if (line.type === 'unchanged') {
      lineA++;
      lineB++;
      numA = lineA;
      numB = lineB;
    } else if (line.type === 'removed') {
      lineA++;
      numA = lineA;
    } else if (line.type === 'added') {
      lineB++;
      numB = lineB;
    }
    return { ...line, idx, numA, numB };
  });

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden mb-6">
      {/* Baslik */}
      <div className="p-4 border-b border-gray-200 flex items-center justify-between flex-wrap gap-2">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">
          Karşılaştırma Sonucu — v{versionA} ↔ v{versionB}
        </h2>
        {hasChanges ? (
          <div className="flex items-center gap-3 text-xs">
            <span className="inline-flex items-center gap-1 text-green-700 bg-green-50 px-2 py-1 rounded font-medium">
              +{added} satır eklendi
            </span>
            <span className="inline-flex items-center gap-1 text-red-700 bg-red-50 px-2 py-1 rounded font-medium">
              −{removed} satır silindi
            </span>
          </div>
        ) : null}
      </div>

      {/* Icerik */}
      {!hasChanges ? (
        <div className="p-6 text-center text-gray-500">
          Bu iki versiyon arasında fark bulunamadı.
        </div>
      ) : (
        <div className="overflow-y-auto max-h-[500px] overflow-x-auto">
          <table className="w-full text-sm font-mono border-collapse">
            <tbody>
              {lines.map(line => (
                <tr
                  key={line.idx}
                  className={
                    line.type === 'added'
                      ? 'bg-green-50'
                      : line.type === 'removed'
                        ? 'bg-red-50'
                        : 'bg-white'
                  }
                >
                  {/* Satir numarasi — Eski (A) */}
                  <td className="px-2 py-0.5 text-right text-gray-400 select-none border-r border-gray-200 w-10 text-xs align-top whitespace-nowrap">
                    {line.numA}
                  </td>
                  {/* Satir numarasi — Yeni (B) */}
                  <td className="px-2 py-0.5 text-right text-gray-400 select-none border-r border-gray-200 w-10 text-xs align-top whitespace-nowrap">
                    {line.numB}
                  </td>
                  {/* +/- isareti */}
                  <td className={`px-2 py-0.5 select-none w-5 text-center font-bold align-top ${
                    line.type === 'added'
                      ? 'text-green-600'
                      : line.type === 'removed'
                        ? 'text-red-600'
                        : 'text-transparent'
                  }`}>
                    {line.type === 'added' ? '+' : line.type === 'removed' ? '−' : ' '}
                  </td>
                  {/* Metin */}
                  <td className={`px-3 py-0.5 whitespace-pre-wrap break-words align-top ${
                    line.type === 'added'
                      ? 'text-green-900'
                      : line.type === 'removed'
                        ? 'text-red-900'
                        : 'text-gray-800'
                  }`}>
                    {line.text || '\u00A0'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
