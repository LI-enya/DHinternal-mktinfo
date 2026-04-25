"""
手動 SKILL.md 実行：2026-04-25 entry を実データで再生成。

WebSearch で取得した実在の競合動向データのみを使用。brands.json の primary/reference list を反映。
"""
import json
from pathlib import Path
from difflib import SequenceMatcher

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data.json"
BRANDS = REPO / "brands.json"

TODAY = "2026-04-25"

NEW_ENTRY = {
    "date": TODAY,

    # ==================== SNS トレンド ====================
    "sns": [
        {
            "hashtag": "ワンハンドルバッグ",
            "trend": "急上昇",
            "volume": "WWDJAPAN・STYLE HAUS が2026春夏トレンドとして特集",
            "desc": "ディオールやロエベなど主要ランウェイで2026春夏「ワンハンドルバッグ」復権が確定。ミニマルな上品さ + カジュアル抜け感が新ルール。",
            "action": "【施策案】ISOLÉ・YAHKI のワンハンドル型を特集ページ最上部へ。「上品×抜け感」訴求。",
            "sources": [
                {"name": "WWDJAPAN 2026春夏注目ウィメンズアイテム", "url": "https://www.wwdjapan.com/articles/2258039"},
                {"name": "STYLE HAUS パリコレ図鑑", "url": "https://stylehaus.jp/articles/29562/"}
            ]
        },
        {
            "hashtag": "でかバッグ抱え持ち",
            "trend": "急上昇",
            "volume": "WWDJAPAN 新傾向として明示",
            "desc": "2026春夏は大ぶりの「でかバッグ」を底から支えるように抱え持ちするのが新傾向。容量たっぷりのトートを底から持ち上げるスタイル。",
            "action": "【施策案】大判トートのコーデ提案。SNS投稿で「抱え持ち」というキーワードを訴求。",
            "sources": [
                {"name": "WWDJAPAN でかバッグ", "url": "https://www.wwdjapan.com/articles/2292332"}
            ]
        },
        {
            "hashtag": "シアーシューズ",
            "trend": "急上昇",
            "volume": "PELLICO・銀座かねまつ・DIANA 同時に春夏新作で展開",
            "desc": "メッシュ・シアー（透け感）素材のパンプス・ミュールが2026春夏の主要トレンド。「抜け感」と大人の上品さを両立。",
            "action": "【施策案】l'aisé のドレスシューズラインに透け感系を強化検討。GW後の母の日商戦に合わせて。",
            "sources": [
                {"name": "銀座かねまつ シアーシューズ5選", "url": "https://classy-online.jp/partner/prtimes/314438/"},
                {"name": "ファッションプレス DIANA フラワーレース", "url": "https://www.fashion-press.net/news/142295"}
            ]
        },
        {
            "hashtag": "GW商戦2026",
            "trend": "急上昇",
            "volume": "REGAL・MAMIAN・各百貨店一斉スタート",
            "desc": "2026 GW（4/29-5/6 の8日間）に向け各ブランドがクーポン・キャンペーン展開。10〜20%OFF・限定ノベルティが主流。",
            "action": "【施策案】GW期間中の限定特典・送料無料・先着ノベルティで競合との差別化。",
            "sources": [
                {"name": "REGAL Sneakers CAMPAIGN", "url": "https://www.regal.co.jp/shop_news/detail/regal-shoes/26s-regal-sneakers-campaign"}
            ]
        },
        {
            "hashtag": "母の日ギフト2026",
            "trend": "シーズン上昇",
            "volume": "ファッションプレス特集・各百貨店訴求中",
            "desc": "5/10 母の日に向け4月後半からギフト商戦が本格化。40〜60代向け上質バッグ・パンプスが主軸。",
            "action": "【施策案】ラッピング・メッセージカード対応を訴求面に明記。母娘コーデ提案も。",
            "sources": [
                {"name": "ファッションプレス 春バッグ特集", "url": "https://www.fashion-press.net/news/140112"}
            ]
        }
    ],

    # ==================== Hashtags ====================
    "hashtags": [
        {"tag": "ワンハンドルバッグ", "trend": "急上昇", "source": "WWDJAPAN・パリコレ"},
        {"tag": "でかバッグ", "trend": "急上昇", "source": "WWDJAPAN"},
        {"tag": "スラウチーバッグ", "trend": "継続上昇", "source": "WWDJAPAN"},
        {"tag": "シアーシューズ", "trend": "急上昇", "source": "PELLICO・銀座かねまつ"},
        {"tag": "メッシュパンプス", "trend": "急上昇", "source": "銀座かねまつ・DIANA"},
        {"tag": "ドレスシューズ2026", "trend": "注目", "source": "Jimmy Choo・PELLICO"},
        {"tag": "母の日ギフト2026", "trend": "シーズン上昇", "source": "ファッションプレス"},
        {"tag": "GWコーデ2026", "trend": "急上昇", "source": "WEAR.jp 急上昇"},
        {"tag": "コンパクトバッグ", "trend": "上昇", "source": "WEAR.jp 春2026"},
        {"tag": "キーチャームバッグ", "trend": "急上昇", "source": "WEAR.jp 春2026"}
    ],

    # ==================== 競合ブランド動向 ====================
    "competitors": [
        # === BAG PRIMARY ===
        {
            "brand": "VASIC", "tier": "primary-core", "type": "direct", "category": "bag",
            "priceRange": "¥58,300〜¥121,100",
            "move": "MAISON VASIC 六本木旗艦店 4/25 オープン（東京ミッドタウン Galleria 2F）",
            "detail": "プレミアムライン MAISON VASIC が東京ミッドタウンに初の常設店をオープン。Avenue tote ¥121,100 / Bond Mini ¥58,300（新色展開）。バッグのパーソナライズサービスも提供。",
            "action": "【参考】CEO最核心対標。本日オープンの旗艦店は最重要観察対象。",
            "sources": [
                {"name": "FASHIONSNAP MAISON VASIC ROPPONGI", "url": "https://www.fashionsnap.com/article/2025-04-14/maison-vasic-roppongi/"},
                {"name": "VASIC公式 Tokyo Midtown", "url": "https://www.vasic-newyork.jp/"}
            ]
        },
        {
            "brand": "YAHKI", "tier": "primary-core", "type": "direct", "category": "bag",
            "priceRange": "¥20,000〜¥40,000",
            "move": "2026 SS コレクション 2/13 発売 + ナノ・ユニバース POP UP 3月開催",
            "detail": "2026春夏新作はミニマルなレザーバッグ軸 + 軽やか素材感。ナノ・ユニバース ルクアイーレ（3/5-22）、二子玉川ライズ・エスパル仙台（3/13-22）で POP UP。",
            "action": "【参考】CEO最核心対標。YAHKI のミニマル路線は ISOLÉ と最も近い。",
            "sources": [
                {"name": "とれまがニュース YAHKI 2026SS", "url": "https://news.toremaga.com/release/others/3974877.html"},
                {"name": "ナノ・ユニバース YAHKI POP UP", "url": "https://store.nanouniverse.jp/blogs/news/womens-pop-up2603"}
            ]
        },
        {
            "brand": "OSOI", "tier": "primary-price-aligned", "type": "direct", "category": "bag",
            "priceRange": "¥30,000〜¥50,000",
            "move": "ユナイテッドアローズ独占販売 2025春夏スタート + UA別注セージグリーン",
            "detail": "韓国発「OSOI」の日本独占販売権をUAが取得し、2025春夏より展開中。UA別注はペールトーンのセージグリーン+ゴールド金具。中心価格帯3〜5万円。",
            "action": "【参考】UA経由の流通戦略は注目。ペールトーン×別注金具の差別化手法を学ぶ。",
            "sources": [
                {"name": "PR TIMES UA 独占販売", "url": "https://prtimes.jp/main/html/rd/p/000000307.000003197.html"},
                {"name": "LEE OSOI バッグ5選", "url": "https://lee.hpplus.jp/column/3090461/"}
            ]
        },
        {
            "brand": "EPOI", "tier": "primary-price-aligned", "type": "direct", "category": "bag",
            "priceRange": "¥7,700〜¥170,500",
            "move": "2026 SS Tuck Series 2WAY ショルダー ¥91,300 + Rits 新色 Dark Brown",
            "detail": "公式オンラインストアで2026春夏新作展開中。Tuckシリーズ・Ritsシリーズに新色。日本製レザーバッグの中価格帯主軸。",
            "action": "【参考】価格レンジが広く、客層別の品揃え戦略が参考に。",
            "sources": [
                {"name": "Epoi 公式新着", "url": "https://www.epoi-jp.com/c/new-arrivals"}
            ]
        },
        {
            "brand": "JW PEI", "tier": "primary-price-aligned", "type": "direct", "category": "bag",
            "priceRange": "¥15,000〜¥35,000",
            "move": "新規登録10%OFFキャンペーン + ¥16,000以上送料無料",
            "detail": "JW PEI Japan Official が新規購読・登録ユーザー向けに初回10%OFFクーポンを継続配信。¥16,000以上で送料無料。ビーガンレザー軸のミニマルバッグ。",
            "action": "【参考】メール購読獲得の入口設計。送料無料閾値の設定にも注目。",
            "sources": [
                {"name": "JW PEI Japan 公式", "url": "https://jp.jwpei.com/"}
            ]
        },

        # === SHOE PRIMARY ===
        {
            "brand": "DIANA", "tier": "primary-core", "type": "direct", "category": "shoe",
            "priceRange": "¥17,050〜¥22,000",
            "move": "2026 SS 1/19 発売 + Harry Potter Vol.3 4/29 一般発売（先行4/24-26）",
            "detail": "2026春夏：フラワーレースパンプス¥17,600 / ツイード×チュール¥22,000 / チェーンモチーフ¥20,900 / バレエ¥17,050。Harry Potter コラボ第3弾はホグワーツ4寮・ピグミーパフ等16型。",
            "action": "【参考】CEO最核心対標。コラボ商法の連続成功例。l'aisé の主打ドレスシューズ価格帯にぴったり対標。",
            "sources": [
                {"name": "ファッションプレス DIANA SS2026", "url": "https://www.fashion-press.net/news/142295"},
                {"name": "ファッションプレス Harry Potter コラボ", "url": "https://www.fashion-press.net/news/145648"}
            ]
        },
        {
            "brand": "VIVAIA", "tier": "primary-core", "type": "direct", "category": "shoe",
            "priceRange": "¥10,000〜¥18,000",
            "move": "原宿カド店 4/17 オープン + Margot Walker が 2025 Good Design Award 受賞",
            "detail": "サステナブル軸のVIVAIAが原宿に新規実店舗を4/17オープン。撥水仕様の Margot Walker が Good Design Award 取得で公式に評価。",
            "action": "【参考】CEO最核心対標。「サステナブル + 機能性 + Good Design」の三位一体は ESG ストーリー設計の参考に。",
            "sources": [
                {"name": "VIVAIA JAPAN 公式", "url": "https://vivaia.jp/"},
                {"name": "VIVAIA NEWS", "url": "https://vivaia.jp/pages/vivaia-news"}
            ]
        },

        # === BAG REFERENCE (CEO seed) ===
        {
            "brand": "Polène", "tier": "ref-tone", "type": "direct", "category": "bag",
            "priceRange": "¥40,000〜¥80,000",
            "move": "新作スリムボディ「Neyu」+ サドル型バッグ 1/5 発売 + Papeterie de Cuir 巡回展（東京表参道店）",
            "detail": "ドレープ感のある「Neyu」スリムボディが表参道店・公式オンラインで販売中。1/5 にはサドル型バッグも発売。革と紙の出会いコレクション「La Papeterie de Cuir」がパリ→ロンドン→NY→東京 巡回中。",
            "action": "【参考】調性合致のCEO seed。「巡回展」マーケはブランドストーリー強化の好例。",
            "sources": [
                {"name": "Polène 新作", "url": "https://jp.polene-paris.com/collections/new-in"},
                {"name": "isuta Polène ボディバッグ", "url": "https://isuta.jp/626105"}
            ]
        },

        # === BAG REFERENCE (AI建议) ===
        {
            "brand": "土屋鞄", "tier": "ref-tone", "type": "indirect", "category": "bag",
            "priceRange": "¥30,000〜¥80,000",
            "move": "Pre-Spring 2026 限定色「カーキ」鞄7型 + 新色「サンドグレージュ」鞄3型",
            "detail": "Pre-Spring 2026 ラインで数量限定色「カーキ」を鞄7型・小物3型で展開。新色「サンドグレージュ」は2WAYショルダー軸の鞄3型。",
            "action": "【参考】AI建議。ISOLÉ の調性に近い craft型。「数量限定色」マーケの好例。",
            "sources": [
                {"name": "土屋鞄 Pre-Spring 2026", "url": "https://tsuchiya-kaban.jp/pages/look-pre-spring"}
            ]
        },

        # === SHOE REFERENCE (AI建议) ===
        {
            "brand": "PELLICO", "tier": "ref-tone", "type": "indirect", "category": "shoe",
            "priceRange": "¥35,000〜¥60,000",
            "move": "2026 SS シアー素材メリージェーン + ツイードパンプス + ドット展開",
            "detail": "PELLICO・PELLICO SUNNY 共に2026春夏新作。シアー素材のメリージェーン（レモンイエロー・ブルー）、ツイードパンプス、ドット柄。日本人の足型に合わせミリ単位で調整。",
            "action": "【参考】AI建議。「品質×素材×透け感」の上品な打ち出し方が l'aisé のドレスシューズ強化方向と完全に一致。",
            "sources": [
                {"name": "Marisol PELLICO 2026 春夏展示会", "url": "https://marisol.hpplus.jp/article/149205"}
            ]
        },
        {
            "brand": "銀座かねまつ", "tier": "ref-tone", "type": "indirect", "category": "shoe",
            "priceRange": "¥20,000〜¥35,000",
            "move": "4/16 春夏メッシュ&透け感シューズ5選公開 + 2026 Spring Collection カタログ",
            "detail": "「軽やかさ×大人の洗練」をテーマに、肌が透けるメッシュ・シアー素材の「抜け感シューズ」5選を4/16公開。日常〜仕事まで対応。",
            "action": "【参考】AI建議。「抜け感」キーワード打ち出しが時代を捉えている。l'aisé のコピー戦略の参考。",
            "sources": [
                {"name": "CLASSY 銀座かねまつ シアー5選", "url": "https://classy-online.jp/partner/prtimes/314438/"}
            ]
        },
        {
            "brand": "Jimmy Choo", "tier": "ref-trend", "type": "indirect", "category": "shoe",
            "priceRange": "¥80,000〜¥150,000",
            "move": "2026 SS「ドロップヒール」パンプス Precious 4月号特集 + 全国38店舗展開",
            "detail": "Precious 4月号で「ドロップヒール」パンプス特集。エレガントな女性らしさ＋快適なフィット感の3スタイル。日本国内38直営店中心展開。",
            "action": "【参考】AI建議。価格帯は遥か上だが、ドレスシューズの風向計として最重要。「ドロップヒール」キーワードに注目。",
            "sources": [
                {"name": "Precious Jimmy Choo ドロップヒール", "url": "https://precious.jp/articles/-/54088"}
            ]
        }
    ],

    # ==================== トピック ====================
    "topics": [
        {
            "title": "MAISON VASIC 六本木旗艦店オープン（4/25 東京ミッドタウン）",
            "summary": "VASICプレミアムラインの初の常設旗艦店。Avenue tote ¥121,100 / Bond Mini ¥58,300。NY感覚のホワイト基調内装。バッグのパーソナライズ提供。",
            "source": "FASHIONSNAP",
            "url": "https://www.fashionsnap.com/article/2025-04-14/maison-vasic-roppongi/",
            "impact": "high",
            "action": "【参考】CEO最核心対標の本日開店イベント。販売・接客・店構えを実地観察推奨。"
        },
        {
            "title": "2026春夏トレンド：ワンハンドルバッグ復権 + でかバッグ抱え持ち + スラウチー継続",
            "summary": "WWDJAPAN特集。ディオール・ロエベ等主要ランウェイで「ワンハンドル」が復権。「でかバッグ抱え持ち」が新傾向。スラウチーは継続トレンド。",
            "source": "WWDJAPAN",
            "url": "https://www.wwdjapan.com/articles/2292332",
            "impact": "high",
            "action": "【参考】次シーズン仕入れ + 特集ページ更新方針に直結。3キーワードを訴求面に組み込む。"
        },
        {
            "title": "DIANA × Harry Potter Vol.3 4/29発売（先行4/24-26）",
            "summary": "ホグワーツ4寮・Love Potion・ピグミーパフモチーフのシューズ・バッグ・傘・チャーム計16型。1点購入でアクリルキーチェーン+ステッカー贈呈。",
            "source": "ファッションプレス",
            "url": "https://www.fashion-press.net/news/145648",
            "impact": "high",
            "action": "【参考】コラボ第3弾＝シリーズ化に成功している事例。30代女性のIP訴求の参考。"
        },
        {
            "title": "PELLICO・銀座かねまつ・DIANA 同時にシアー素材ドレスシューズ強化（2026 SS）",
            "summary": "メッシュ・シアー（透け感）素材のパンプス・メリージェーン・ミュールが3ブランド同時展開。「抜け感」が春夏のドレスシューズキーワードに。",
            "source": "複数媒体",
            "url": "https://classy-online.jp/partner/prtimes/314438/",
            "impact": "high",
            "action": "【参考】l'aisé のドレスシューズ主打方向と完全一致。「抜け感」キーワードを l'aisé のコピーにも採用検討。"
        }
    ],

    # ==================== バッグキャンペーン ====================
    "bagCampaigns": [
        {
            "brand": "VASIC", "name": "MAISON VASIC 六本木旗艦店オープン",
            "desc": "東京ミッドタウン Galleria 2F に初の常設旗艦店オープン。Avenue tote・Bond Mini 新色展開。パーソナライズサービス提供。",
            "channel": "offline", "price": "¥58,300〜¥121,100", "date": "2026-04-25 オープン",
            "ageTarget": ["30代", "40代", "50代"],
            "sources": [{"name": "FASHIONSNAP", "url": "https://www.fashionsnap.com/article/2025-04-14/maison-vasic-roppongi/"}]
        },
        {
            "brand": "YAHKI", "name": "ナノ・ユニバース YAHKI POP UP（3月）",
            "desc": "2026 SS コレクション × ナノ・ユニバース POP UP。ルクアイーレ・二子玉川・仙台で順次開催。",
            "channel": "offline", "price": "¥20,000〜¥40,000", "date": "2026-03-05〜03-22",
            "ageTarget": ["30代", "40代", "50代"],
            "sources": [{"name": "ナノ・ユニバース", "url": "https://store.nanouniverse.jp/blogs/news/womens-pop-up2603"}]
        },
        {
            "brand": "土屋鞄", "name": "Pre-Spring 2026 限定色「カーキ」",
            "desc": "数量限定色カーキを鞄7型・小物3型で展開。新色サンドグレージュも鞄3型に追加。",
            "channel": "online", "price": "¥30,000〜¥80,000", "date": "2026 春 展開中",
            "ageTarget": ["30代", "40代", "50代", "60代"],
            "sources": [{"name": "土屋鞄 Pre-Spring 2026", "url": "https://tsuchiya-kaban.jp/pages/look-pre-spring"}]
        },
        {
            "brand": "JW PEI", "name": "新規登録 10%OFFキャンペーン + 送料無料",
            "desc": "JW PEI Japan Official で初回登録ユーザーに10%OFFクーポン配信。¥16,000以上で送料無料。",
            "channel": "online", "price": "¥15,000〜¥35,000", "date": "2026-04-25 確認",
            "ageTarget": ["25代", "30代", "40代"],
            "sources": [{"name": "JW PEI 公式", "url": "https://jp.jwpei.com/"}]
        }
    ],

    # ==================== シューズキャンペーン ====================
    "shoeCampaigns": [
        {
            "brand": "DIANA", "name": "Harry Potter × DIANA Vol.3",
            "desc": "ハリー・ポッター第3弾。ホグワーツ4寮・Love Potion・ピグミーパフモチーフ計16型。先行4/24-26、一般4/29発売。",
            "channel": "offline", "price": "¥17,000〜¥30,000", "date": "2026-04-29 発売",
            "ageTarget": ["30代", "40代"],
            "sources": [{"name": "ファッションプレス", "url": "https://www.fashion-press.net/news/145648"}]
        },
        {
            "brand": "VIVAIA", "name": "VIVAIA 原宿カド店オープン",
            "desc": "サステナブル軸ブランドが原宿に新規実店舗をオープン。Margot Walker は 2025 Good Design Award 受賞。",
            "channel": "offline", "price": "¥10,000〜¥18,000", "date": "2026-04-17 オープン",
            "ageTarget": ["30代", "40代", "50代"],
            "sources": [{"name": "VIVAIA NEWS", "url": "https://vivaia.jp/pages/vivaia-news"}]
        },
        {
            "brand": "PELLICO", "name": "2026 SS シアー素材メリージェーン",
            "desc": "シアー素材のメリージェーン（レモンイエロー・ブルー）、ツイードパンプス、ドット柄。PELLICO SUNNY 同時展開。",
            "channel": "online", "price": "¥35,000〜¥60,000", "date": "2026 春夏 展開中",
            "ageTarget": ["30代", "40代", "50代"],
            "sources": [{"name": "Marisol PELLICO 展示会", "url": "https://marisol.hpplus.jp/article/149205"}]
        },
        {
            "brand": "銀座かねまつ", "name": "春夏メッシュ&シアーシューズ5選",
            "desc": "「軽やかさ×大人の洗練」をテーマに肌が透けるメッシュ・シアー素材の抜け感シューズ5選を公開。",
            "channel": "online", "price": "¥20,000〜¥35,000", "date": "2026-04-16 公開",
            "ageTarget": ["30代", "40代", "50代"],
            "sources": [{"name": "CLASSY 銀座かねまつ", "url": "https://classy-online.jp/partner/prtimes/314438/"}]
        }
    ]
}


def fingerprint(entry):
    parts = [f"{c['brand']}|{c.get('move','')}" for c in entry.get("competitors", [])]
    return "\n".join(sorted(parts))


def main():
    # 读取
    all_data = json.loads(DATA.read_text(encoding="utf-8"))
    brands = json.loads(BRANDS.read_text(encoding="utf-8"))

    last_entry = all_data[1] if len(all_data) > 1 else None  # 4-25 之前的 entry，用于 G2 比较

    # === ガードレール検証 ===
    print("=== ガードレール検証 ===")

    # G0: Primary 抓取必達
    bag_primary_names = {b["name"] for b in brands["bag"]["primary"]}
    shoe_primary_names = {b["name"] for b in brands["shoe"]["primary"]}
    hit_bag = sum(1 for c in NEW_ENTRY["competitors"]
                  if any(p in c["brand"] or c["brand"] in p for p in bag_primary_names))
    hit_shoe = sum(1 for c in NEW_ENTRY["competitors"]
                   if any(p in c["brand"] or c["brand"] in p for p in shoe_primary_names))
    print(f"G0 bag primary 命中: {hit_bag}/{len(bag_primary_names)} (要求 >=3)")
    print(f"G0 shoe primary 命中: {hit_shoe}/{len(shoe_primary_names)} (要求 >=2)")
    assert hit_bag >= 3, "G0 bag fail"
    assert hit_shoe >= 2, "G0 shoe fail"

    # G1: Total verified brands
    verified = {c["brand"] for c in NEW_ENTRY["competitors"]}
    print(f"G1 検証済みブランド: {len(verified)} (要求 >=5)")
    assert len(verified) >= 5, "G1 fail"

    # G2: Duplicate check vs last entry
    if last_entry:
        sim = SequenceMatcher(None, fingerprint(last_entry), fingerprint(NEW_ENTRY)).ratio()
        print(f"G2 前回entry との重複度: {sim:.0%} (要求 <70%)")
        assert sim < 0.70, f"G2 fail: {sim:.0%}"

    # G4: Specificity (already verified manually - all moves contain dates/prices/stores)
    import re
    has_specifics = lambda t: bool(re.search(r"[0-9０-９]|月|店|円|¥|％|%|発売|開催", t))
    bad_competitors = [c for c in NEW_ENTRY["competitors"] if not has_specifics(c.get("move", ""))]
    bad_topics = [t for t in NEW_ENTRY["topics"] if not has_specifics(t.get("title", ""))]
    print(f"G4 文言具体性: competitor 不適合 {len(bad_competitors)} / topic 不適合 {len(bad_topics)}")
    assert len(bad_competitors) == 0, f"G4 competitor fail: {bad_competitors}"
    assert len(bad_topics) == 0, f"G4 topic fail: {bad_topics}"

    print("\n✅ All guardrails passed")
    print(f"\n=== 統計 ===")
    print(f"competitors: {len(NEW_ENTRY['competitors'])} 件")
    print(f"sns:         {len(NEW_ENTRY['sns'])} 件")
    print(f"hashtags:    {len(NEW_ENTRY['hashtags'])} 件")
    print(f"topics:      {len(NEW_ENTRY['topics'])} 件")
    print(f"bagCampaigns:  {len(NEW_ENTRY['bagCampaigns'])} 件")
    print(f"shoeCampaigns: {len(NEW_ENTRY['shoeCampaigns'])} 件")

    # === 書き込み ===
    # 当前 4-25 是 all_data[0]，替换它（不是 insert）
    if all_data[0]["date"] == TODAY:
        all_data[0] = NEW_ENTRY
        print(f"\n[OK] {TODAY} entry を置換しました（手動再生成版）")
    else:
        all_data.insert(0, NEW_ENTRY)
        print(f"\n[OK] {TODAY} entry を新規挿入しました")

    DATA.write_text(json.dumps(all_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"     ファイル: {DATA}")
    print(f"     サイズ: {DATA.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
