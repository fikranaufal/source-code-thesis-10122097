"""
Internationalization (i18n) Module for Streamlit Dashboard.
Supports Indonesian (ID) and Japanese (JA) for bilingual presentation.
"""

import streamlit as st

TRANSLATIONS = {
    "id": {
        # App Meta & General
        "app_title": "Sistem Pendukung Keputusan Peramalan Penjualan Ritel",
        "app_subtitle": "Evaluasi & Simulasi Bisnis Model Global LSTM (3 Juta Data Transaksi)",
        "language_select": "Pilih Bahasa / 言語選択",
        "author_tag": "Tugas Akhir Teknik Informatika / Data Science",
        "nav_home": "🏠 Ringkasan Eksekutif",
        "nav_story": "📊 Cerita Kaizen (Evolusi Model)",
        "nav_roi": "💰 Dampak Bisnis & Simulasi Biaya",
        "nav_matrix": "🧭 Matriks Pola Permintaan",
        "nav_forecast": "🔮 Peramalan What-If & Stok Ulang",
        
        # Executive Summary (Home)
        "exec_header": "Ringkasan Eksekutif & Arsitektur Solusi",
        "exec_sub": "Dari kegagalan LSTM individual pada seminar proposal hingga dominasi Model Global LSTM pada 1.782 kombinasi toko-produk.",
        "kpi_data_points": "Total Data Dilatih",
        "kpi_data_desc": "Transaksi historis 54 toko & 33 kategori",
        "kpi_combos": "Kombinasi Toko-Kategori",
        "kpi_combos_desc": "Deret waktu cross-sectional dipelajari serempak",
        "kpi_accuracy_boost": "Rata-rata Peningkatan RMSLE",
        "kpi_accuracy_desc": "Dibandingkan Baseline Seasonal Naive",
        "kpi_waste_reduction": "Estimasi Reduksi Kerugian Stok",
        "kpi_waste_desc": "Pengurangan biaya overstock & stockout",
        
        "core_pillars_title": "3 Pilar Utama Keunggulan Penelitian",
        "pillar1_title": "1. Paradigma Model Global",
        "pillar1_desc": "Mengatasi keterbatasan data (*data sparsity*) pada model per-produk dengan melatih satu arsitektur LSTM mendalam pada seluruh 3 juta data lintas 54 toko secara simultan.",
        "pillar2_title": "2. Integrasi Fitur Eksogen Multivariat",
        "pillar2_desc": "Memanfaatkan sinyal makroekonomi (harga minyak Ekuador), promosi, hari gajian dua mingguan (*quincena*), dan dampak gempa bumi Manabi 2016.",
        "pillar3_title": "3. Diferensiasi Pola Permintaan",
        "pillar3_desc": "Mengklasifikasikan 1.782 deret waktu ke dalam 4 kuadran Syntetos-Boylan (Smooth, Intermittent, Lumpy, Erratic) untuk optimasi model yang presisi.",
        
        "interview_guide_title": "Panduan Alur Presentasi 3 Menit (Untuk Penguji & Interviewer)",
        "step1_title": "Langkah 1: Tunjukkan Latar Belakang & Masalah",
        "step1_desc": "Buka modul 'Cerita Kaizen' untuk menjelaskan mengapa model time-series deep learning individual rentan gagal pada data ritel bervolume pendek.",
        "step2_title": "Langkah 2: Tunjukkan Bukti Keunggulan Global LSTM",
        "step2_desc": "Tunjukkan grafik perbandingan di mana Global LSTM mampu menangkap tren gajian, promosi, dan musiman mingguan tanpa lag.",
        "step3_title": "Langkah 3: Buktikan Dampak Finansial (ROI)",
        "step3_desc": "Gunakan modul 'Dampak Bisnis' untuk mengubah metrik RMSLE menjadi penghematan biaya riil dan pengurangan limbah makanan segar (Muda Elimination).",

        # Modul 1: The Kaizen Story
        "story_title": "Cerita Kaizen: Evolusi Model Peramalan",
        "story_sub": "Menerapkan Siklus PDCA (Plan-Do-Check-Act) dari Kegagalan Sempro menuju Keberhasilan TA-2",
        "stage_comparison_title": "Komparasi Kinerja Antar Tahap Eksperimen",
        "store_select": "Pilih Toko Target:",
        "family_select": "Pilih Kategori Produk:",
        "select_target_combo": "Pilih Kombinasi Target Eksperimen:",
        "legend_actual": "Data Aktual (Ground Truth)",
        "legend_naive": "Seasonal Naive (Baseline TA-1)",
        "legend_individual_lstm": "Individual LSTM (Model Lama Sempro)",
        "legend_global_simple": "Global Simple LSTM (TA-2)",
        "legend_global_complex": "Global Complex Multivariate LSTM (TA-2)",
        "kaizen_insight_title": "💡 Mengapa Global LSTM Berhasil?",
        "kaizen_insight_body": "Model individual mengalami overfitting karena hanya melihat data dari satu toko (~1.600 baris). Global Model LSTM melatih 'shared representation' dari 3 juta baris transaksi, memungkinkan model memahami pola musiman makro, elastisitas promosi, dan fluktuasi hari gajian dengan jauh lebih stabil.",
        "table_summary_header": "Tabel Komparasi RMSLE (8 Kombinasi Target Kunci)",

        # Modul 2: Business Impact & ROI
        "roi_title": "Dampak Finansial & Simulator Eliminasi Pemborosan (Muda)",
        "roi_sub": "Mengubah Metrik Teknis (RMSLE) Menjadi Estimasi Nilai Bisnis Nyata",
        "sim_params": "Parameter Biaya & Risiko Inventaris",
        "holding_cost_label": "Biaya Penyimpanan per Unit/Hari ($):",
        "stockout_cost_label": "Biaya Penalti Kehabisan Stok per Unit ($):",
        "spoilage_rate_label": "Faktor Risiko Basi / Spoilage (%):",
        "annual_volume_label": "Estimasi Volume Tahunan (Unit):",
        "financial_summary_title": "Estimasi Efisiensi Finansial Tahunan",
        "cost_naive": "Total Biaya Kerugian (Seasonal Naive)",
        "cost_global_lstm": "Total Biaya Kerugian (Global LSTM)",
        "cost_savings": "Estimasi Penghematan Finansial",
        "waste_reduction_kpi": "Pengurangan Limbah Barang Basi",
        "stockout_reduction_kpi": "Pengurangan Risiko Stok Kosong",
        "cost_breakdown_chart": "Komparasi Komposisi Biaya Operasional Stok",
        "roi_explanation_title": "Penerapan Prinsip Lean & Just-In-Time (JIT)",
        "roi_explanation_body": "Dalam manajemen ritel modern, kelebihan stok (overstock) memicu pemborosan modal dan kerusakan barang segar (terutama Daging & Ikan), sedangkan kekurangan stok (understock) menghilangkan pendapatan dan menurunkan kepuasan pelanggan. Presisi Global LSTM menjaga level persediaan tepat pada batas optimal.",

        # Modul 3: Demand Pattern Matrix
        "matrix_title": "Matriks Pola Permintaan (Syntetos-Boylan Framework)",
        "matrix_sub": "Karakterisasi 1.782 Kombinasi Toko-Produk Berdasarkan ADI dan CV²",
        "matrix_desc": "Klasifikasi permintaan membantu manajemen rantai pasok menentukan strategi peramalan yang paling efektif untuk setiap tipe produk.",
        "filter_category": "Filter Kategori Pola:",
        "all_categories": "Semua Kategori (1.782 Kombinasi)",
        "quadrant_smooth": "Smooth (Permintaan Stabil)",
        "quadrant_intermittent": "Intermittent (Permintaan Sporadis)",
        "quadrant_erratic": "Erratic (Volume Sangat Fluktuatif)",
        "quadrant_lumpy": "Lumpy (Sporadis & Fluktuatif)",
        "quadrant_no_sales": "No Sales (Tidak Ada Penjualan)",
        "matrix_scatter_title": "Distribusi 1.782 Kombinasi pada Kuadran ADI vs CV²",
        "category_performance_title": "Performa Rata-Rata RMSLE Model Global per Kategori",

        # Modul 4: What-If & Reorder Advisor
        "forecast_title": "Simulator Skenario What-If & Rekomendasi Stok Ulang",
        "forecast_sub": "Perencanaan Pengadaan Barang Berbasis Sinyal Eksogen & Ketidakpastian Permintaan",
        "scenario_controls": "Tuas Pengaturan Skenario",
        "promo_slider": "Intensitas Promosi (Jumlah Produk Diskon):",
        "payday_toggle": "Simulasikan Periode Gajian (Quincena 15 & Akhir Bulan)",
        "oil_shock_slider": "Fluktuasi Harga Minyak Dunia (%):",
        "lead_time_label": "Lead Time Pengiriman Supplier (Hari):",
        "service_level_label": "Target Service Level (% Kepuasan Pelanggan):",
        "forecast_chart_title": "Proyeksi Permintaan 30 Hari & Batas Stok Pengaman",
        "reorder_kpi_title": "Rekomendasi Parameter Pengadaan (Reorder Parameters)",
        "safety_stock_kpi": "Stok Pengaman (Safety Stock)",
        "rop_kpi": "Titik Pemesanan Ulang (Reorder Point)",
        "avg_daily_demand": "Rata-Rata Permintaan Harian",
        "peak_demand": "Puncak Permintaan Diproyeksikan",
    },
    "ja": {
        # App Meta & General
        "app_title": "小売需要予測・意思決定支援システム (DSS)",
        "app_subtitle": "300万件の取引データに基づくグローバルLSTMモデルの評価とビジネスシミュレーション",
        "language_select": "言語選択 / Language",
        "author_tag": "卒業研究（情報工学 / データサイエンス）",
        "nav_home": "🏠 エグゼクティブサマリー",
        "nav_story": "📊 改善ストーリー（モデルの進化）",
        "nav_roi": "💰 ビジネスインパクト＆コスト削減シミュレーション",
        "nav_matrix": "🧭 需要パターン分類マトリクス",
        "nav_forecast": "🔮 What-If 予測＆発注点シミュレーター",
        
        # Executive Summary (Home)
        "exec_header": "エグゼクティブサマリー＆ソリューション概要",
        "exec_sub": "個別LSTMモデルの課題克服から、1,782系列を統合学習したグローバルLSTMモデルの確立まで",
        "kpi_data_points": "学習データ総数",
        "kpi_data_desc": "54店舗・33商品カテゴリの時系列データ",
        "kpi_combos": "店舗×カテゴリ系列数",
        "kpi_combos_desc": "クロスセクショナルな同時統合学習",
        "kpi_accuracy_boost": "平均RMSLE改善率",
        "kpi_accuracy_desc": "Seasonal Naive ベースライン比較",
        "kpi_waste_reduction": "在庫ロス削減見込み",
        "kpi_waste_desc": "過剰在庫および欠品損失の極小化",
        
        "core_pillars_title": "本研究における3つの核心的価値",
        "pillar1_title": "1. グローバルモデルパラダイム",
        "pillar1_desc": "個別モデルでのデータスパースティ（標本不足）を解消し、54店舗・300万件の大規模データを統合学習することで、深層学習本来の表現力を発揮。",
        "pillar2_title": "2. 多変量・外生変数の統合",
        "pillar2_desc": "マクロ経済指標（原油価格）、販促プロモーション、半月ごとの給与支給日（Quincena）、2016年エクアドル地震などの外部ショックを特徴量として統合。",
        "pillar3_title": "3. 需要パターン別最適化",
        "pillar3_desc": "Syntetos-Boylanフレームワークを用い、1,782系列を4象限（Smooth, Intermittent, Lumpy, Erratic）に分類し、特性に応じた最適なモデルを選択。",
        
        "interview_guide_title": "3分間プレゼンテーションガイド（面接・口頭試問用）",
        "step1_title": "ステップ 1: 背景と課題提起（反省・現状把握）",
        "step1_desc": "「改善ストーリー」画面を開き、個別時系列での過学習やデータ不足という初期の課題を説明します。",
        "step2_title": "ステップ 2: グローバルLSTMによるブレークスルー",
        "step2_desc": "給与日やプロモーションのスパイクを遅延なく正確に捉えるモデル予測グラフを提示します。",
        "step3_title": "ステップ 3: ビジネス価値と無駄の排除（見える化）",
        "step3_desc": "「ビジネスインパクト」画面で、RMSLEの改善が金銭的コスト削減や食品廃棄ロス削減に直結することを証明します。",

        # Modul 1: The Kaizen Story
        "story_title": "改善ストーリー：需要予測モデルの進化過程",
        "story_sub": "PDCAサイクルに基づく仮説検証：初期プロポーザルから本研究完了までの軌跡",
        "stage_comparison_title": "各実験ステージにおける予測精度の比較",
        "store_select": "対象店舗を選択:",
        "family_select": "商品カテゴリを選択:",
        "select_target_combo": "検証ターゲット系列を選択:",
        "legend_actual": "実績値 (Ground Truth)",
        "legend_naive": "Seasonal Naive (初期ベースライン)",
        "legend_individual_lstm": "個別LSTM (初期プロポーザルモデル)",
        "legend_global_simple": "グローバル Simple LSTM (TA-2)",
        "legend_global_complex": "グローバル Complex 多変量 LSTM (TA-2)",
        "kaizen_insight_title": "💡 グローバルLSTMが成功した理由（要因分析）",
        "kaizen_insight_body": "個別モデルは単一店舗の限られたデータ（約1,600行）しか参照できず過学習に陥っていました。一方、グローバルモデルは全300万行の取引から共有表現を学習し、曜日周期・給与日サイクル・プロモーション効果を極めて安定して捉えることが可能になりました。",
        "table_summary_header": "主要8ターゲット系列のRMSLE比較表",

        # Modul 2: Business Impact & ROI
        "roi_title": "財務インパクト＆「無駄（Muda）」削減シミュレーター",
        "roi_sub": "技術指標（RMSLE）を経営判断に資する金銭的価値へ変換",
        "sim_params": "在庫コストおよびリスク設定パラメータ",
        "holding_cost_label": "在庫維持費用 / 個・日 ($):",
        "stockout_cost_label": "欠品機会損失ペナルティ / 個 ($):",
        "spoilage_rate_label": "生鮮食品廃棄リスク率 (%):",
        "annual_volume_label": "年間販売見込み数量 (個):",
        "financial_summary_title": "年間在庫関連コスト削減推計",
        "cost_naive": "従来モデル（Naive）における総損失コスト",
        "cost_global_lstm": "グローバルLSTMにおける総損失コスト",
        "cost_savings": "年間コスト削減見込み額",
        "waste_reduction_kpi": "食品廃棄ロス削減率",
        "stockout_reduction_kpi": "欠品リスク削減率",
        "cost_breakdown_chart": "在庫運用コスト構成の比較内訳",
        "roi_explanation_title": "リーン生産方式・ジャストインタイム（JIT）の適用",
        "roi_explanation_body": "小売業において、過剰在庫はキャッシュフローの悪化と生鮮品（肉・魚・卵等）の廃棄ロスを引き起こし、欠品は売上機会の喪失と顧客満足度低下を招きます。高精度なグローバルLSTMにより、在庫を常に適正水準に維持できます。",

        # Modul 3: Demand Pattern Matrix
        "matrix_title": "需要パターン分類マトリクス (Syntetos-Boylan)",
        "matrix_sub": "ADI（需要発生間隔）とCV²（需要変動係数）による1,782系列の俯瞰",
        "matrix_desc": "需要特性に応じた分類により、サプライチェーンにおける最適な予測・在庫補充戦略を策定します。",
        "filter_category": "需要パターンの絞り込み:",
        "all_categories": "全カテゴリ（1,782系列）",
        "quadrant_smooth": "Smooth（安定型需要）",
        "quadrant_intermittent": "Intermittent（間欠型需要）",
        "quadrant_erratic": "Erratic（不規則・変動型需要）",
        "quadrant_lumpy": "Lumpy（塊状・不規則間欠型）",
        "quadrant_no_sales": "No Sales（販売実績なし）",
        "matrix_scatter_title": "1,782系列のADI vs CV² 4象限分布",
        "category_performance_title": "需要パターン別 グローバルモデル平均RMSLE比較",

        # Modul 4: What-If & Reorder Advisor
        "forecast_title": "What-If シナリオ予測＆適正発注点アドバイザー",
        "forecast_sub": "外生変数シミュレーションと需要の不確実性を考慮した現場発注支援",
        "scenario_controls": "シミュレーション制御レバー",
        "promo_slider": "プロモーション強度（対象商品数）:",
        "payday_toggle": "給与支給日（15日・月末 Quincena）効果を適用",
        "oil_shock_slider": "原油価格変動率 (%):",
        "lead_time_label": "サプライヤー調達リードタイム (日):",
        "service_level_label": "目標サービス率 (顧客充足率 %):",
        "forecast_chart_title": "今後30日間の需要予測推移と安全在庫バンド",
        "reorder_kpi_title": "推奨在庫発注パラメータ",
        "safety_stock_kpi": "推奨安全在庫数 (Safety Stock)",
        "rop_kpi": "発注点 (Reorder Point - ROP)",
        "avg_daily_demand": "1日あたり平均需要",
        "peak_demand": "最大予測ピーク需要",
    }
}

def get_current_lang() -> str:
    """Get the currently selected language from session state."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "id"
    return st.session_state["lang"]

def set_lang(lang_code: str):
    """Set the active language in session state."""
    st.session_state["lang"] = lang_code

def t(key: str) -> str:
    """Translate a key into the active language."""
    lang = get_current_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS["id"]).get(key, key)

def render_language_selector():
    """Render language switcher in Streamlit sidebar."""
    current_lang = get_current_lang()
    options = ["🇮🇩 Bahasa Indonesia", "🇯🇵 日本語 (Japanese)"]
    current_index = 0 if current_lang == "id" else 1
    
    selected = st.sidebar.selectbox(
        t("language_select"),
        options=options,
        index=current_index,
        key="lang_selector_widget"
    )
    new_lang = "id" if "Bahasa Indonesia" in selected else "ja"
    if new_lang != current_lang:
        set_lang(new_lang)
        st.rerun()
