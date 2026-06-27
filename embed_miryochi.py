import csv, json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

rows = []
with open('ichiranhyou_geocoded.csv', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        rows.append({
            'name': r['財産名称'].strip(),
            'bureau': r['土地所管局'].strip(),
            'area': r['面積（㎡）'].strip(),
            'status': r['現状'].strip(),
            'policy': r['活用方針'].strip(),
            'criteria': r['分類基準'].strip(),
            'rental': r['貸付等の活用状況'].strip(),
            'link': r['マップナビおおさかへのリンク'].strip(),
            'lat': float(r['緯度']) if r['緯度'] else None,
            'lng': float(r['経度']) if r['経度'] else None,
        })

js_data = 'const MIRYOCHI = ' + json.dumps(rows, ensure_ascii=False) + ';'

# index.html を読み込む
with open('index.html', encoding='utf-8') as f:
    html = f.read()

# <script> タグの直後にデータを挿入（最初の <script> タグを探す）
html = re.sub(
    r'(<script>)',
    r'\1\n' + js_data + '\n',
    html,
    count=1
)

# markerLayer の初期化の近くに miryochiLayer を追加
html = html.replace(
    'markerLayer = L.layerGroup().addTo(leafletMap);',
    'markerLayer = L.layerGroup().addTo(leafletMap);\n      miryochiLayer = L.layerGroup(); miryochiVisible = false;'
)

# initMap 関数内で miryochiLayer を再アタッチ（既存の markerLayer 再構築処理の近く）
# miryochiLayer/miryochiVisible 変数宣言をグローバル変数エリアに追加
html = html.replace(
    'let markerLayer, leafletMap;',
    'let markerLayer, leafletMap;\nlet miryochiLayer, miryochiVisible = false;'
)

# circlePanel の直前にトグルボタンを追加
miryochi_btn = '''<button id="miryochiToggleBtn" onclick="toggleMiryochi()" style="position:absolute;top:10px;left:10px;z-index:1000;padding:6px 12px;background:var(--white);border:1px solid var(--line);border-radius:6px;font-size:12px;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.15)">未利用地 OFF</button>
    '''

html = html.replace(
    '<div id="circlePanel"',
    miryochi_btn + '<div id="circlePanel"'
)

# JS関数を </script> の直前に追加
miryochi_js = '''
function buildMiryochiPopup(m) {
  const rental = m.rental || '－';
  const linkBtn = m.link
    ? `<a href="${m.link}" target="_blank" rel="noopener" style="display:block;margin-top:8px;padding:5px 10px;background:#1a6fb5;color:#fff;text-align:center;border-radius:4px;text-decoration:none;font-size:12px">🗺 まっぷなびおおさかで見る</a>`
    : '';
  return `<div style="font-size:13px;line-height:1.6">
    <b style="font-size:14px">${m.name}</b><br>
    <table style="width:100%;border-collapse:collapse;margin-top:6px">
      <tr><td style="color:#888;white-space:nowrap;padding-right:8px">所管局</td><td>${m.bureau}</td></tr>
      <tr><td style="color:#888;white-space:nowrap;padding-right:8px">面積</td><td>${m.area} ㎡</td></tr>
      <tr><td style="color:#888;white-space:nowrap;padding-right:8px">現状</td><td>${m.status}</td></tr>
      <tr><td style="color:#888;white-space:nowrap;padding-right:8px">活用方針</td><td>${m.policy}（${m.criteria}）</td></tr>
      <tr><td style="color:#888;white-space:nowrap;padding-right:8px">貸付等</td><td>${rental}</td></tr>
    </table>
    ${linkBtn}
  </div>`;
}

function renderMiryochi() {
  miryochiLayer.clearLayers();
  MIRYOCHI.forEach(m => {
    if (!m.lat || !m.lng) return;
    const icon = L.divIcon({
      className: '',
      html: '<div style="width:10px;height:10px;background:#e67e22;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',
      iconSize: [10, 10],
      iconAnchor: [5, 5]
    });
    const marker = L.marker([m.lat, m.lng], { icon });
    marker.bindPopup(buildMiryochiPopup(m), { maxWidth: 320 });
    miryochiLayer.addLayer(marker);
  });
}

function toggleMiryochi() {
  miryochiVisible = !miryochiVisible;
  const btn = document.getElementById('miryochiToggleBtn');
  if (miryochiVisible) {
    if (!leafletMap) { miryochiVisible = false; return; }
    renderMiryochi();
    miryochiLayer.addTo(leafletMap);
    btn.textContent = '未利用地 ON';
    btn.style.background = '#e67e22';
    btn.style.color = '#fff';
    btn.style.borderColor = '#e67e22';
  } else {
    miryochiLayer.remove();
    btn.textContent = '未利用地 OFF';
    btn.style.background = '';
    btn.style.color = '';
    btn.style.borderColor = '';
  }
}
'''

# </script> の最後の出現の直前に挿入
last_script_end = html.rfind('</script>')
html = html[:last_script_end] + miryochi_js + '\n' + html[last_script_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html を更新しました")
print(f"未利用地データ: {len(rows)}件埋め込み")
