import csv, json, time, urllib.request, urllib.parse, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

rows = []
with open('ichiranhyou.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        ku = row['所在（区）'].strip()
        cho = row['町丁目'].strip()
        ban = row['街区番号'].strip()
        row['住居表示'] = f"大阪府大阪市{ku}{cho}{ban}"
        rows.append(row)

print(f"読み込み: {len(rows)}件")

def geocode(addr):
    url = 'https://msearch.gsi.go.jp/address-search/AddressSearch?q=' + urllib.parse.quote(addr)
    try:
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read())
        if data:
            lng, lat = data[0]['geometry']['coordinates']
            return lat, lng
    except Exception as e:
        print(f"  エラー: {addr} → {e}")
    return None, None

for i, row in enumerate(rows):
    addr = row['住居表示']
    lat, lng = geocode(addr)
    # 失敗時は街区番号を除いて再試行
    if lat is None:
        short = f"大阪府大阪市{row['所在（区）'].strip()}{row['町丁目'].strip()}"
        lat, lng = geocode(short)
        if lat is not None:
            row['緯度'] = lat
            row['経度'] = lng
            row['ジオコード精度'] = '町丁目'
        else:
            row['緯度'] = ''
            row['経度'] = ''
            row['ジオコード精度'] = '失敗'
    else:
        row['緯度'] = lat
        row['経度'] = lng
        row['ジオコード精度'] = '街区番号'
    time.sleep(0.2)
    if (i + 1) % 50 == 0:
        ok = sum(1 for r in rows[:i+1] if r.get('緯度') != '')
        print(f"{i+1}/{len(rows)} 完了（成功:{ok}）")

ok = sum(1 for r in rows if r.get('緯度') != '')
print(f"\n完了: 成功={ok}, 失敗={len(rows)-ok}")

out_fields = list(fieldnames) + ['住居表示', '緯度', '経度', 'ジオコード精度']
with open('ichiranhyou_geocoded.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    writer.writerows(rows)

print("ichiranhyou_geocoded.csv を保存しました")
