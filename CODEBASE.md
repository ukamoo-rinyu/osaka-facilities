# 大阪市施設検索システム — コードベースマップ

## ファイル構成

| ファイル | サイズ | 役割 |
|---|---|---|
| `index.html` | ~244行 | HTMLのみ（構造・マークアップ） |
| `style.css` | ~171行 | 全スタイル定義 |
| `app.js` | ~1617行 | 全ロジック（関数・イベント） |
| `facilities.json` | 540KB | 施設データ（1,606件）→ fetch で読込 |
| `miryochi.json` | 140KB | 未利用地データ → fetch で読込 |

## app.js — 関数マップ

### データ・初期化
| 行 | 関数 / 変数 | 概要 |
|---|---|---|
| 1 | `MIRYOCHI` | 未利用地データ配列（fetch後に設定） |
| 3 | `FACILITIES` | 施設データ配列（fetch後に設定） |
| 5〜11 | `UC`, `UB` | 用途別カラー定義 |
| 15 | `normalizeUseDetail()` | 用途詳細の表記ゆれ正規化 |
| 37 | `addrCount` | 同一住所インデックス |
| 43 | `state` | フィルター・表示状態 |
| 1602 | `loadAndInit()` | fetch→FACILITIES/MIRYOCHI設定→init呼び出し |

### 施設フィルター・表示
| 行 | 関数 | 概要 |
|---|---|---|
| ~444 | `init()` | 起動時初期化（ドロップダウン構築・URL読込・描画） |
| ~473 | `resetF()` | フィルターリセット |
| ~485 | `setSort()` | ソート変更 |
| ~505 | `setView()` | グリッド/リスト/地図 切替 |
| ~1049 | `getFiltered()` | 現在のフィルター条件で施設配列を返す |
| ~1076 | `render()` | カード/リスト/地図を再描画 |
| ~1095 | `renderCard()` | 施設カード1枚のHTML生成 |

### 地図
| 行 | 関数 | 概要 |
|---|---|---|
| ~520 | `initMap()` | Leafletマップ初期化 |
| ~548 | `toggleLabels()` | ラベル表示ON/OFF |
| ~565 | `enableCircle()` | 範囲円モード開始 |
| ~609 | `drawCircle()` | 範囲円・中心マーカー描画 |
| ~686 | `renderMap()` | マーカー・グループアイコン描画 |

### ドロップダウン（カスタム）
| 行 | 関数群 | 概要 |
|---|---|---|
| ~870 | `buildUsItems`, `toggleUsMenu`, `usSelectAll/None` | 用途区分 |
| ~914 | `buildBsItems`, `toggleBsMenu`, `bsSelectAll/None` | 所管局 |
| ~951 | `buildWsItems`, `toggleWsMenu`, `wsSelectAll/None` | 行政区 |
| ~986 | `buildUdsItems`, `toggleUdsMenu`, `udsSelectAll/None` | 用途詳細 |

### 詳細パネル・AI検索
| 行 | 関数 | 概要 |
|---|---|---|
| ~1196 | `selF()` | 施設選択（地図ハイライト） |
| ~1207 | `openP()` | 詳細パネル開く |
| ~1307 | `closeP()` | 詳細パネル閉じる |
| ~1313 | `runAI()` | 周辺情報AI検索 |

### 未利用地タブ
| 行 | 関数 | 概要 |
|---|---|---|
| ~1353 | `computeMiryochiWards()` | 未利用地の区リスト生成 |
| ~1384 | `switchTab()` | 施設/未利用地タブ切替 |
| ~1498 | `getMiryochiFiltered()` | 未利用地フィルター |
| ~1519 | `renderMiryochiCards()` | 未利用地カード描画 |

### URL共有・統計・リスト管理
| 行 | 関数 | 概要 |
|---|---|---|
| ~1655 | `copyShareUrl()`, `loadStateFromUrl()` | URLコピー・URL読込 |
| ~1753 | `renderDash()`, `toggleDash()` | 統計ダッシュボード |
| ~1862 | `loadLists()`, `createList()`, `addToList()` | 施設リスト管理 |

## index.html — 主要DOM要素

| ID/クラス | 役割 |
|---|---|
| `#dashPanel` | 統計ダッシュボード（右スライドイン） |
| `.filter-bar` | 施設フィルターバー（検索・区・用途など） |
| `#miryochiBar` | 未利用地フィルターバー |
| `.sbar` | ソート・操作バー |
| `#cg` | 施設カードグリッド |
| `#mapWrap` / `#mapView` | 地図コンテナ |
| `#dp` | 詳細パネル（右サイド） |
| `#updatePopup` | 更新情報ポップアップ |
| `#listPanel` | 施設リストパネル |

## style.css — 主要クラス

| クラス | 対象 |
|---|---|
| `.filter-bar`, `.fg`, `.fl` | フィルターバー |
| `.card`, `.ch`, `.cn`, `.ct`, `.ca` | 施設カード |
| `.dp`, `.dph`, `.dpb`, `.dpg` | 詳細パネル |
| `.dash-*` | 統計ダッシュボード |
| `.tab-btn` | タブバー |
| `.mcard`, `.mcard-*` | 未利用地カード |
| `.ais`, `.air` | AI検索ボックス |
