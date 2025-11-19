# 臨床試驗文件自動化系統 - 整合說明

## 📘 系統介紹

這是一個完整的臨床試驗文件自動化系統，整合了五個核心模組，提供從 Protocol 解析到文件生成的完整解決方案。

### 🎯 核心價值

- **自動化**: 從 Protocol PDF 到完整文件集，一鍵完成
- **智能化**: 使用 Google Gemini AI 進行智能解析
- **標準化**: 生成符合臨床試驗標準的專業文件
- **易用性**: 互動式介面，無需編程經驗

---

## 📦 檔案結構

```
clinical-doc-automation/
├── Clinical_Trial_Document_Automation_System.ipynb  # 主要 Notebook
├── NOTEBOOK_QUICK_START.md                          # 快速開始指南
├── README_INTEGRATED_SYSTEM.md                      # 本文件
├── modules/                                          # 核心模組
│   ├── protocol_parser.py                           # Protocol 解析器
│   ├── crf_generator.py                             # CRF 生成器
│   ├── dvp_generator.py                             # DVP 生成器
│   ├── user_guide_generator.py                      # User Guide 生成器
│   └── word_formatter.py                            # Word 格式化工具
├── examples/                                         # 使用範例
├── templates/                                        # 文件範本
└── output/                                          # 輸出資料夾
```

---

## 🚀 快速開始

### 方法 1: Google Colab（推薦）

1. **開啟 Colab**
   ```
   https://colab.research.google.com/
   ```

2. **上傳 Notebook**
   - File → Upload notebook
   - 選擇 `Clinical_Trial_Document_Automation_System.ipynb`

3. **上傳 modules 資料夾**
   - 在左側檔案面板
   - 上傳整個 `modules` 資料夾

4. **執行 Notebook**
   - Runtime → Run all
   - 或逐步執行各 Section

### 方法 2: 本地 Jupyter

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **啟動 Jupyter**
   ```bash
   cd clinical-doc-automation
   jupyter notebook Clinical_Trial_Document_Automation_System.ipynb
   ```

3. **執行 Notebook**
   - 逐步執行各 Section

---

## 📋 Notebook 結構

### Section 1: 系統安裝
- 安裝所有必要的 Python 套件
- 驗證套件安裝狀態

### Section 2: 環境設定
- 導入基礎模組
- 設置專案結構
- 導入自訂模組

### Section 3: 使用者介面設定
- **API Key 設定**: 輸入 Gemini API Key
- **檔案上傳**: Protocol PDF、Logo、Word 範本
- **參數設定**: 贊助商、階段、生成選項

### Section 4: Protocol 資訊提取
- 解析 Protocol PDF
- 提取關鍵資訊
- 保存為 JSON

### Section 5: CRF 生成
- 根據 Protocol 生成 CRF
- 建立表單和欄位
- 輸出 Word 文件

### Section 6: DVP 生成
- 生成驗證規則
- 建立 DVP 文件
- 匯出規則 JSON

### Section 7: User Guide 生成
- 生成 CRF 使用說明
- 建立填寫指南
- 輸出 Word 文件

### Section 8: 一鍵生成所有文件
- **自動化流程**: 執行所有步驟
- **進度顯示**: 即時顯示處理進度
- **錯誤處理**: 自動處理異常

### Section 9: 下載結果
- 個別下載檔案
- ZIP 壓縮下載
- 檔案清單查看

### Section 10: 範例和說明
- 完整使用流程
- 常見問題解答
- 進階功能說明

---

## 🎯 使用流程

### 最簡流程（5 分鐘）

```
1. 設定 API Key ────────────> Section 3
2. 上傳 Protocol PDF ──────> Section 3
3. 點擊「一鍵生成」 ───────> Section 8
4. 下載 ZIP 檔案 ─────────> Section 9
```

### 完整流程（10 分鐘）

```
1. 安裝套件 ───────────────> Section 1
2. 設定環境 ───────────────> Section 2
3. 配置參數 ───────────────> Section 3
4. 解析 Protocol ─────────> Section 4
   └─> 檢查提取結果
5. 生成 CRF ──────────────> Section 5
   └─> 可自訂欄位
6. 生成 DVP ──────────────> Section 6
   └─> 可添加自訂規則
7. 生成 User Guide ───────> Section 7
   └─> 可修改說明
8. 下載結果 ───────────────> Section 9
```

---

## 🔧 核心功能

### 1. Protocol Parser

**功能：**
- 從 PDF 提取試驗資訊
- 使用 AI 智能解析
- 輸出結構化 JSON

**提取內容：**
- 試驗標題、編號、贊助商
- 試驗設計、階段、樣本數
- 訪視時程
- 主要/次要終點
- 納入/排除標準
- CRF 領域

**使用範例：**
```python
parser = ProtocolParser(api_key="YOUR_KEY")
protocol_info = parser.parse_protocol("protocol.pdf")
```

### 2. CRF Generator

**功能：**
- 自動生成 CRF 表單
- 支援多種欄位類型
- 專業 Word 格式

**支援欄位：**
- 文字、數字、日期
- 下拉選單、核取方塊
- 時間、檔案上傳

**使用範例：**
```python
crf_gen = CRFGenerator(api_key="YOUR_KEY")
crf_gen.generate_crf(protocol_info)
```

### 3. DVP Generator

**功能：**
- 自動生成驗證規則
- 支援多種驗證類型
- 輸出詳細 DVP

**驗證類型：**
- 範圍檢查（Range Check）
- 一致性檢查（Consistency Check）
- 必填欄位檢查（Required Field）
- Protocol 偏差檢查（Protocol Deviation）
- 邏輯檢查（Logic Check）

**使用範例：**
```python
dvp_gen = DVPGenerator(protocol_info)
dvp_gen.add_crf_fields(fields)
dvp_gen.generate_all_rules()
dvp_gen.generate_dvp_document("dvp.docx")
```

### 4. User Guide Generator

**功能：**
- 自動生成填寫說明
- 包含欄位詳細說明
- 支援螢幕截圖

**內容結構：**
- 試驗概述
- 系統登入說明
- 表單填寫指南
- 常見問題
- 附錄

**使用範例：**
```python
guide_gen = UserGuideGenerator(
    protocol_number="ABC-001",
    protocol_title="Trial Title"
)
guide_gen.add_crf_form("Demographics", fields)
guide_gen.generate_document("guide.docx")
```

### 5. Word Formatter

**功能：**
- 統一文件格式
- 添加頁首頁尾
- 插入 Logo

**格式化選項：**
- 標題樣式
- 段落格式
- 表格樣式
- 頁碼、日期

**使用範例：**
```python
formatter = WordFormatter()
formatter.add_header("Protocol: ABC-001")
formatter.add_logo("logo.png")
formatter.format_document("input.docx", "output.docx")
```

---

## 📊 輸出文件

### 1. Protocol_Info.json
**內容：** Protocol 結構化資訊
**用途：** 資料交換、後續處理
**格式：** JSON

### 2. Protocol_CRF.docx
**內容：** 病例報告表
**用途：** 資料收集
**格式：** Word（可編輯）

### 3. Protocol_DVP.docx
**內容：** 資料驗證計畫
**用途：** 資料品質控制
**格式：** Word（可編輯）

### 4. Protocol_DVP_rules.json
**內容：** 驗證規則詳細定義
**用途：** 系統實施、程式開發
**格式：** JSON

### 5. Protocol_User_Guide.docx
**內容：** CRF 使用者手冊
**用途：** 訓練、參考
**格式：** Word（可編輯）

---

## ⚙️ 進階設定

### API 模型選擇

**gemini-1.5-flash（推薦）**
- 優點：速度快、免費額度高
- 適合：一般 Protocol、快速生成
- 配額：15 RPM, 1M TPM

**gemini-1.5-pro**
- 優點：更準確、更詳細
- 適合：複雜 Protocol、高品質要求
- 配額：2 RPM, 32K TPM

### 自訂參數

```python
# Protocol 解析參數
parser.parse_protocol(
    pdf_path="protocol.pdf",
    max_pages=50,  # 限制頁數（加快速度）
    extract_tables=True  # 提取表格
)

# DVP 生成參數
dvp_gen.generate_all_rules(
    include_range_check=True,
    include_consistency_check=True,
    include_protocol_deviation=True
)

# User Guide 生成參數
guide_gen.generate_document(
    output_path="guide.docx",
    logo_path="logo.png",
    include_screenshots=True
)
```

### 批次處理

```python
# 處理多個 Protocol
protocols = [
    {"pdf": "protocol1.pdf", "number": "ABC-001"},
    {"pdf": "protocol2.pdf", "number": "ABC-002"},
    {"pdf": "protocol3.pdf", "number": "ABC-003"}
]

for p in protocols:
    uploaded_files['protocol_pdf'] = p['pdf']
    generate_all_documents()
    # 重命名輸出檔案
    rename_outputs(p['number'])
```

---

## 💡 最佳實踐

### 1. Protocol 準備

✅ **推薦：**
- 完整的 Protocol PDF
- 文字可選取（非掃描版）
- 清晰的結構和章節
- 包含所有必要資訊

❌ **避免：**
- 掃描版 PDF
- 過大檔案（> 50MB）
- 損壞或加密的 PDF

### 2. 參數設定

✅ **推薦：**
- 正確填寫贊助商和階段
- 選擇合適的 AI 模型
- 只生成需要的文件

❌ **避免：**
- 留空必填欄位
- 使用錯誤的試驗資訊

### 3. 結果驗證

✅ **推薦：**
- 仔細檢查提取的 Protocol 資訊
- 驗證 CRF 欄位的完整性
- 檢查 DVP 規則的合理性
- 確認 User Guide 的正確性

❌ **避免：**
- 不檢查直接使用
- 忽略錯誤訊息

### 4. 文件編輯

✅ **推薦：**
- 將生成的文件作為初稿
- 根據實際需求調整
- 添加特定的專案資訊
- 經過專業人員審核

❌ **避免：**
- 完全依賴自動生成
- 不經審核直接使用

---

## 🐛 故障排除

### 問題 1: 模組導入失敗

**症狀：**
```
✗ Protocol Parser 導入失敗: No module named 'modules.protocol_parser'
```

**解決方法：**
1. 確認 `modules` 資料夾已上傳（Colab）
2. 檢查檔案路徑是否正確
3. 重新執行 Section 2

### 問題 2: API Key 錯誤

**症狀：**
```
✗ 解析失敗: Invalid API key
```

**解決方法：**
1. 確認 API Key 正確複製
2. 檢查 API Key 是否已啟用
3. 確認沒有多餘空格
4. 嘗試重新生成 API Key

### 問題 3: Protocol 解析超時

**症狀：**
```
✗ 解析失敗: Timeout error
```

**解決方法：**
1. 檢查網路連線
2. 限制 PDF 頁數（`max_pages=50`）
3. 嘗試使用更快的模型（flash）
4. 分段處理大型 Protocol

### 問題 4: 記憶體不足

**症狀：**
```
✗ 生成失敗: Out of memory
```

**解決方法：**
1. 重啟 Colab Runtime
2. 使用較小的 PDF
3. 分批生成文件
4. 清理不需要的變數

### 問題 5: 下載失敗

**症狀：**
檔案無法下載

**解決方法：**
1. 檢查瀏覽器彈出視窗設定
2. 使用 ZIP 下載（更穩定）
3. 從左側檔案面板手動下載
4. 確認檔案確實已生成

---

## 📈 效能優化

### 速度優化

1. **使用 Flash 模型**
   ```python
   model_dropdown.value = 'gemini-1.5-flash'
   ```

2. **限制 PDF 頁數**
   ```python
   parser.parse_protocol(pdf_path, max_pages=50)
   ```

3. **只生成需要的文件**
   ```python
   generate_crf.value = True
   generate_dvp.value = False  # 跳過
   generate_guide.value = False  # 跳過
   ```

### 品質優化

1. **使用 Pro 模型**
   ```python
   model_dropdown.value = 'gemini-1.5-pro'
   ```

2. **讀取完整 Protocol**
   ```python
   parser.parse_protocol(pdf_path, max_pages=None)
   ```

3. **手動檢查和調整**
   - 逐步執行各 Section
   - 檢查中間結果
   - 必要時手動調整

---

## 🔒 安全性

### 資料保護

- ✅ 本地處理（Session 內）
- ✅ API 傳輸加密
- ✅ 不儲存在第三方
- ✅ Session 結束自動清除

### 建議措施

1. **去識別化**
   - 使用去識別化的 Protocol
   - 不包含真實受試者資料

2. **API Key 管理**
   - 使用 Colab Secrets
   - 不要寫在程式碼中
   - 定期更換

3. **檔案管理**
   - 定期清理輸出資料夾
   - 下載後刪除 Colab 檔案
   - 不要分享含敏感資訊的檔案

---

## 📚 相關文件

### 快速開始
- `NOTEBOOK_QUICK_START.md` - 快速開始指南

### 模組文件
- `modules/README.md` - 模組總覽
- `modules/README_PROTOCOL_PARSER.md` - Protocol Parser 說明
- `modules/README_CRF_Generator.md` - CRF Generator 說明
- `modules/README_DVP.md` - DVP Generator 說明
- `modules/USER_GUIDE_GENERATOR_README.md` - User Guide Generator 說明

### 範例
- `examples/protocol_parser_example.py` - Protocol Parser 範例
- `examples/crf_generator_example.py` - CRF Generator 範例
- `examples/dvp_example.py` - DVP Generator 範例
- `examples/example_user_guide_generation.py` - User Guide Generator 範例

---

## 🎓 教學資源

### 視頻教學（建議製作）
1. 快速開始（5 分鐘）
2. 完整流程（15 分鐘）
3. 進階功能（20 分鐘）

### 實作練習
1. 使用範例 Protocol 生成文件
2. 自訂 DVP 驗證規則
3. 批次處理多個 Protocol

---

## 🔄 版本歷史

### v1.0.0 (2025-11-18)

**新功能：**
- ✅ 完整整合 5 個核心模組
- ✅ 一鍵生成功能
- ✅ 互動式使用者介面（ipywidgets）
- ✅ 檔案上傳功能
- ✅ 即時進度顯示
- ✅ ZIP 批次下載
- ✅ 詳細文件和範例

**核心模組版本：**
- Protocol Parser v1.0.0
- CRF Generator v1.0.0
- DVP Generator v1.0.0
- User Guide Generator v1.0.0
- Word Formatter v1.0.0

**技術規格：**
- Python 3.8+
- Google Colab 相容
- Jupyter Notebook 相容

---

## 📞 支援和聯絡

### 技術支援
- 查看文件和範例
- 參考常見問題
- 檢查故障排除指南

### 回饋和建議
- 回報 Bug
- 功能建議
- 使用經驗分享

---

## 📄 授權

本系統為內部使用工具，請遵守相關使用規範。

---

## 🎉 開始使用

準備好體驗自動化文件生成了嗎？

```bash
# 開啟 Notebook
jupyter notebook Clinical_Trial_Document_Automation_System.ipynb

# 或上傳到 Google Colab
# https://colab.research.google.com/
```

**祝您使用順利！**

---

*最後更新：2025-11-18*
*版本：1.0.0*
