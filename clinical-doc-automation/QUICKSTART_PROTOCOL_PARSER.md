# Protocol Parser 快速入門指南

## 🚀 5 分鐘快速開始

### 步驟 1: 安裝依賴套件

```bash
pip install pdfplumber google-generativeai
```

### 步驟 2: 獲取免費 API 金鑰

1. 訪問 https://makersuite.google.com/app/apikey
2. 使用 Google 帳號登入
3. 點擊 "Create API Key"
4. 複製 API 金鑰

### 步驟 3: 設置 API 金鑰

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 步驟 4: 使用範例

**Python 腳本:**

```python
from modules.protocol_parser import ProtocolParser

# 初始化
parser = ProtocolParser()

# 解析 Protocol
protocol_info = parser.parse_protocol("your_protocol.pdf")

# 查看結果
print(protocol_info.study_title)
print(protocol_info.crf_domains)

# 保存 JSON
parser.save_to_json(protocol_info, "output.json")
```

**在 Colab 中使用:**

1. 打開 `examples/Protocol_Parser_Demo.ipynb`
2. 依序執行每個 cell
3. 上傳您的 Protocol PDF
4. 查看提取結果

## 📁 檔案位置

```
clinical-doc-automation/
├── modules/
│   ├── protocol_parser.py          # 主要模組
│   ├── test_protocol_parser.py     # 測試腳本
│   └── README_PROTOCOL_PARSER.md   # 完整文檔
├── examples/
│   ├── protocol_parser_example.py      # Python 範例
│   └── Protocol_Parser_Demo.ipynb      # Jupyter 範例
└── requirements.txt                    # 依賴清單
```

## ✨ 主要功能

| 功能 | 說明 |
|------|------|
| **自動提取基本資訊** | Study Title, Protocol Number, Sponsor, Phase |
| **試驗設計資訊** | Study Design, Target Population, Sample Size |
| **訪視時程** | 自動識別所有訪視時間點 |
| **終點指標** | Primary & Secondary Endpoints |
| **受試者標準** | Inclusion & Exclusion Criteria |
| **CRF 領域建議** | 自動推薦需要的 CRF 表單 |

## 💡 使用技巧

### 處理大型 PDF (>100 頁)
```python
# 只讀取前 50 頁
protocol_info = parser.parse_protocol("large.pdf", max_pages=50)
```

### 批次處理多個檔案
```python
import time
from pathlib import Path

pdf_files = Path("protocols/").glob("*.pdf")

for pdf in pdf_files:
    protocol_info = parser.parse_protocol(str(pdf))
    output = f"output/{pdf.stem}_info.json"
    parser.save_to_json(protocol_info, output)
    time.sleep(2)  # 避免 API 速率限制
```

### 自定義模型
```python
# 使用更強大的模型（可能有額度限制）
parser = ProtocolParser(
    api_key="YOUR_KEY",
    model_name="gemini-1.5-pro"
)
```

## 📊 輸出範例

```json
{
  "study_title": "A Phase 3 Study of Drug X in Diabetes",
  "protocol_number": "ABC-123-2024",
  "sponsor": "XYZ Pharma",
  "phase": "Phase III",
  "crf_domains": [
    "Demographics",
    "Vital Signs",
    "Adverse Events",
    "Laboratory",
    "ECG"
  ]
}
```

## ⚠️ 注意事項

- ✅ Gemini 1.5 Flash 完全免費
- ⚠️ API 有速率限制：每分鐘 15 次請求
- ⚠️ 建議 PDF 文字清晰可提取（非掃描版）
- ✅ 支持中英文 Protocol

## 🆘 常見問題

**Q: 為什麼提取結果不完整？**
A: 嘗試增加 `max_pages` 或檢查 PDF 是否包含所需資訊

**Q: 如何提高準確度？**
A: 使用 `gemini-1.5-pro` 模型或提供更清晰的 PDF

**Q: 可以處理掃描版 PDF 嗎？**
A: 需要先進行 OCR 處理，或使用支持 OCR 的工具

**Q: 支持哪些語言？**
A: 支持中文和英文，也支持其他主要語言

## 📚 延伸閱讀

- 完整文檔: `modules/README_PROTOCOL_PARSER.md`
- API 文檔: https://ai.google.dev/docs
- 範例代碼: `examples/protocol_parser_example.py`

## 🔧 故障排除

```bash
# 檢查安裝
python -c "import pdfplumber; import google.generativeai; print('✓ 依賴已安裝')"

# 測試語法
python -m py_compile modules/protocol_parser.py

# 執行測試（需要先安裝依賴）
cd modules && python test_protocol_parser.py
```

---

**需要協助？** 查看完整文檔或聯繫開發團隊

**最後更新**: 2025-11-18
