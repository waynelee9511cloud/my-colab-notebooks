# 臨床試驗文件自動化工作流程

## Clinical Document Automation Workflow

> 從 Protocol PDF 一鍵生成所有臨床試驗文件的端到端自動化解決方案

---

## 📋 目錄

- [功能特色](#功能特色)
- [快速開始](#快速開始)
- [安裝](#安裝)
- [使用方法](#使用方法)
  - [命令列使用](#命令列使用)
  - [Python API 使用](#python-api-使用)
  - [批次處理](#批次處理)
- [生成的文件](#生成的文件)
- [配置選項](#配置選項)
- [錯誤處理](#錯誤處理)
- [執行報告](#執行報告)
- [進階功能](#進階功能)
- [常見問題](#常見問題)
- [範例](#範例)

---

## 🚀 功能特色

### 核心功能

✅ **Protocol PDF 自動解析**
- 使用 Google Gemini AI 智能提取 Protocol 關鍵資訊
- 支援多種 Protocol 格式和結構
- 自動識別試驗階段、目標族群、訪視時程等

✅ **CRF (Case Report Form) 自動生成**
- 基於 Protocol 資訊自動生成 CRF 文件
- 支援標準 CDISC 領域
- 自訂欄位和驗證規則
- 完整的編碼指引 (Coding Instructions)

✅ **DVP (Data Validation Plan) 自動生成**
- 自動生成數據驗證規則
- 支援多種驗證類型：範圍檢查、必填欄位、邏輯檢查等
- 智能生成 Query 文本
- 按嚴重程度分類（Critical/Major/Minor）

✅ **User Guide 自動生成**
- 完整的 EDC/ePRO 系統使用指南
- 包含登入、導航、數據輸入等完整流程
- 自動生成截圖需求清單
- 包含 Query 管理和報告生成說明

✅ **進度追蹤與日誌**
- 即時進度顯示
- 詳細的日誌記錄
- 任務狀態追蹤
- 執行時間分析

✅ **錯誤處理與回滾**
- 完善的異常處理機制
- 自動備份功能
- 詳細的錯誤報告
- 任務失敗不影響其他任務

✅ **批次處理支援**
- 一次處理多個 Protocol
- 並行處理（可選）
- 批次處理摘要報告

---

## ⚡ 快速開始

### 最簡單的使用方式

```bash
# 1. 設置環境變數（推薦）
export GEMINI_API_KEY="your-api-key-here"

# 2. 執行自動化
python automation_workflow.py --protocol your_protocol.pdf

# 完成！所有文件已自動生成
```

### 或者使用 API Key 參數

```bash
python automation_workflow.py \
  --protocol your_protocol.pdf \
  --api-key "your-api-key-here" \
  --output-dir ./output
```

---

## 📦 安裝

### 系統需求

- Python 3.8 或更高版本
- 足夠的磁碟空間（建議至少 500MB）
- 網路連接（用於 Gemini API）

### 安裝依賴

```bash
# 進入專案目錄
cd clinical-doc-automation

# 安裝所需套件
pip install -r requirements.txt
```

### 獲取 Gemini API Key

1. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入您的 Google 帳號
3. 點擊 "Create API Key"
4. 複製生成的 API Key
5. 設置環境變數（推薦）或在命令中使用

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows (CMD)
set GEMINI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

---

## 💻 使用方法

### 命令列使用

#### 1. 生成所有文件（預設）

```bash
python automation_workflow.py --protocol protocol.pdf
```

#### 2. 只生成特定文件

```bash
# 只生成 CRF 和 DVP
python automation_workflow.py \
  --protocol protocol.pdf \
  --generate crf dvp

# 只生成 User Guide
python automation_workflow.py \
  --protocol protocol.pdf \
  --generate user_guide
```

#### 3. 自訂輸出目錄

```bash
python automation_workflow.py \
  --protocol protocol.pdf \
  --output-dir ./my_output_folder
```

#### 4. 顯示詳細日誌

```bash
python automation_workflow.py \
  --protocol protocol.pdf \
  --verbose
```

#### 5. 批次處理多個 Protocol

```bash
python automation_workflow.py \
  --batch protocol1.pdf protocol2.pdf protocol3.pdf \
  --api-key "your-api-key"
```

### Python API 使用

#### 基本使用

```python
from automation_workflow import ClinicalDocAutomation

# 創建自動化實例
automation = ClinicalDocAutomation(
    protocol_pdf="path/to/protocol.pdf",
    api_key="your-gemini-api-key",
    output_dir="./output",
    verbose=True
)

# 執行所有任務
report = automation.run_all()

# 查看結果
print(f"完成: {report.completed_tasks}/{report.total_tasks}")
print(f"生成檔案: {len(report.generated_files)}")
```

#### 選擇性生成

```python
# 只生成 CRF 和 DVP
report = automation.run_all(generate_types=['crf', 'dvp'])
```

#### 單獨執行各個步驟

```python
# 1. 解析 Protocol
success = automation.parse_protocol()

# 2. 生成 CRF
if success:
    automation.generate_crf()

# 3. 生成 DVP
if success:
    automation.generate_dvp()

# 4. 生成 User Guide
if success:
    automation.generate_user_guide()

# 5. 生成報告
automation.generate_final_report()
```

### 批次處理

```python
from automation_workflow import BatchProcessor

# 創建批次處理器
processor = BatchProcessor(
    api_key="your-api-key",
    output_base_dir="batch_output",
    verbose=True
)

# 處理多個 Protocol
protocols = [
    "protocol1.pdf",
    "protocol2.pdf",
    "protocol3.pdf"
]

results = processor.process_protocols(
    protocol_pdfs=protocols,
    generate_types=['crf', 'dvp', 'user_guide']
)

# 查看結果
for protocol_path, report in results:
    print(f"{protocol_path}: {report.completed_tasks} 完成")
```

---

## 📄 生成的文件

執行完成後，會在輸出目錄中生成以下文件：

```
output_PROTOCOL-001_20251118_120000/
├── protocol_info.json              # Protocol 解析結果（JSON 格式）
├── CRF_PROTOCOL-001.docx           # Case Report Form 文件
├── DVP_PROTOCOL-001.docx           # Data Validation Plan 文件
├── UserGuide_PROTOCOL-001.docx    # EDC/ePRO User Guide 文件
├── UserGuide_Screenshots.txt      # 截圖需求清單
├── automation.log                  # 詳細執行日誌
├── automation_report.json         # 執行報告（JSON 格式）
├── automation_report.txt          # 執行報告（文字格式）
└── _backup/                        # 備份目錄（如果啟用）
    └── ...
```

### 文件說明

| 文件名 | 說明 | 格式 |
|--------|------|------|
| `protocol_info.json` | Protocol 解析結果，包含所有提取的關鍵資訊 | JSON |
| `CRF_*.docx` | Case Report Form，包含所有 CRF 領域和欄位定義 | Word |
| `DVP_*.docx` | Data Validation Plan，包含所有驗證規則 | Word |
| `UserGuide_*.docx` | EDC/ePRO 系統使用指南 | Word |
| `UserGuide_Screenshots.txt` | 截圖需求清單，列出所有需要的截圖 | Text |
| `automation.log` | 詳細的執行日誌，用於除錯 | Text |
| `automation_report.json` | 結構化的執行報告 | JSON |
| `automation_report.txt` | 人類可讀的執行報告 | Text |

---

## ⚙️ 配置選項

### 命令列參數

| 參數 | 說明 | 預設值 | 範例 |
|------|------|--------|------|
| `--protocol` | Protocol PDF 檔案路徑 | 必填 | `--protocol protocol.pdf` |
| `--batch` | 批次處理：多個 Protocol | - | `--batch p1.pdf p2.pdf` |
| `--api-key` | Gemini API 金鑰 | 環境變數 | `--api-key "key123"` |
| `--output-dir` | 輸出目錄 | 自動生成 | `--output-dir ./output` |
| `--generate` | 要生成的文件類型 | `all` | `--generate crf dvp` |
| `--verbose` / `-v` | 顯示詳細日誌 | `False` | `--verbose` |
| `--no-backup` | 不備份檔案 | `False` | `--no-backup` |
| `--version` | 顯示版本資訊 | - | `--version` |

### Python API 參數

```python
ClinicalDocAutomation(
    protocol_pdf: str,        # Protocol PDF 檔案路徑（必填）
    api_key: str,             # Gemini API 金鑰（必填）
    output_dir: Optional[str] = None,  # 輸出目錄
    verbose: bool = False,    # 顯示詳細日誌
    backup: bool = True       # 啟用備份功能
)
```

### 文件生成選項

可用的 `generate_types` 值：

- `'crf'` - 生成 CRF (Case Report Form)
- `'dvp'` - 生成 DVP (Data Validation Plan)
- `'user_guide'` - 生成 User Guide
- `'dmp'` - 生成 DMP (Data Management Plan) - 尚未實現
- `'all'` - 生成所有文件（預設）

---

## 🔧 錯誤處理

### 常見錯誤和解決方法

#### 1. Protocol PDF 找不到

```
錯誤: FileNotFoundError: Protocol PDF 不存在
解決: 確認檔案路徑正確，使用絕對路徑或相對路徑
```

#### 2. API Key 未設置

```
錯誤: ValueError: 必須提供 API Key
解決: 設置環境變數 GEMINI_API_KEY 或使用 --api-key 參數
```

#### 3. API 配額超限

```
錯誤: API quota exceeded
解決: 等待配額重置，或升級 API 計劃
```

#### 4. PDF 解析失敗

```
錯誤: PDF 解析失敗
解決: 確認 PDF 檔案完整且未損壞，檢查 PDF 是否有密碼保護
```

### 檢查日誌

詳細的錯誤資訊會記錄在 `automation.log` 檔案中：

```bash
# 查看日誌
cat output_*/automation.log

# 查看錯誤
grep ERROR output_*/automation.log
```

### 使用備份功能

```python
# 啟用備份（預設）
automation = ClinicalDocAutomation(
    protocol_pdf="protocol.pdf",
    api_key="key",
    backup=True  # 失敗時會保留已生成的檔案
)
```

---

## 📊 執行報告

### 報告結構

執行完成後會生成兩種格式的報告：

#### 1. JSON 報告 (`automation_report.json`)

```json
{
  "protocol_path": "/path/to/protocol.pdf",
  "output_directory": "/path/to/output",
  "start_time": "2025-11-18T12:00:00",
  "end_time": "2025-11-18T12:15:30",
  "total_tasks": 5,
  "completed_tasks": 4,
  "failed_tasks": 0,
  "skipped_tasks": 1,
  "tasks": [
    {
      "task_id": "parse_protocol",
      "task_type": "protocol_parsing",
      "status": "completed",
      "output_path": "/path/to/protocol_info.json",
      "start_time": "2025-11-18T12:00:00",
      "end_time": "2025-11-18T12:02:30"
    }
  ],
  "generated_files": [
    "/path/to/CRF_PROTO-001.docx",
    "/path/to/DVP_PROTO-001.docx"
  ],
  "errors": [],
  "protocol_info": {
    "study_title": "...",
    "protocol_number": "PROTO-001"
  }
}
```

#### 2. 文字報告 (`automation_report.txt`)

```
================================================================================
臨床試驗文件自動化生成報告
Clinical Document Automation Report
================================================================================

【基本資訊】
--------------------------------------------------------------------------------
Protocol PDF: /path/to/protocol.pdf
輸出目錄: /path/to/output
開始時間: 2025-11-18T12:00:00
結束時間: 2025-11-18T12:15:30
執行時長: 0:15:30

【Protocol 資訊】
--------------------------------------------------------------------------------
試驗標題: A Phase III Study of...
Protocol 編號: PROTO-2025-001
贊助商: Example Pharmaceuticals
試驗階段: Phase III

【執行統計】
--------------------------------------------------------------------------------
總任務數: 5
完成任務: 4
失敗任務: 0
跳過任務: 1
成功率: 80.0%

【任務詳情】
--------------------------------------------------------------------------------
1. ✓ PROTOCOL_PARSING - COMPLETED
   輸出檔案: /path/to/protocol_info.json
   開始時間: 2025-11-18T12:00:00
   結束時間: 2025-11-18T12:02:30

2. ✓ CRF - COMPLETED
   輸出檔案: /path/to/CRF_PROTO-001.docx
   ...
```

### 使用報告

```python
# 讀取 JSON 報告
import json

with open("output_*/automation_report.json") as f:
    report = json.load(f)

# 分析結果
print(f"成功率: {report['completed_tasks']/report['total_tasks']*100:.1f}%")

# 列出所有生成的檔案
for file_path in report['generated_files']:
    print(f"✓ {file_path}")

# 檢查錯誤
if report['errors']:
    print("發現錯誤:")
    for error in report['errors']:
        print(f"  - {error}")
```

---

## 🎯 進階功能

### 1. 自訂 CRF 領域

```python
from automation_workflow import ClinicalDocAutomation
from modules.crf_generator import CRFDomain

automation = ClinicalDocAutomation(
    protocol_pdf="protocol.pdf",
    api_key="key"
)

# 解析 Protocol
automation.parse_protocol()

# 添加自訂 CRF 領域（在生成 CRF 之前）
custom_domain = CRFDomain(
    name='Quality of Life',
    description='Patient QoL assessments',
    fields=[
        {
            'name': 'qol_score',
            'label': 'QoL Score',
            'type': 'numeric',
            'required': True,
            'coding_instruction': 'Score range 0-100'
        }
    ]
)

# 然後生成 CRF（會包含自訂領域）
automation.generate_crf()
```

### 2. 自訂驗證規則

```python
from modules.dvp_generator import Severity, ValidationType

automation.parse_protocol()

# 在生成 DVP 之前添加自訂規則
# （需要修改內部實現以支援此功能）
```

### 3. 並行處理（批次）

```python
from automation_workflow import BatchProcessor
from concurrent.futures import ThreadPoolExecutor

# 創建批次處理器
processor = BatchProcessor(
    api_key="key",
    output_base_dir="batch_output"
)

# 使用多線程並行處理（謹慎使用，注意 API 限制）
protocols = ["p1.pdf", "p2.pdf", "p3.pdf"]

with ThreadPoolExecutor(max_workers=2) as executor:
    # 實現並行處理邏輯
    pass
```

### 4. 整合到現有系統

```python
# 作為 API 服務
from fastapi import FastAPI, UploadFile
from automation_workflow import ClinicalDocAutomation

app = FastAPI()

@app.post("/generate")
async def generate_documents(file: UploadFile, api_key: str):
    # 保存上傳的 PDF
    pdf_path = f"temp/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # 執行自動化
    automation = ClinicalDocAutomation(
        protocol_pdf=pdf_path,
        api_key=api_key
    )
    report = automation.run_all()

    # 返回結果
    return {
        "status": "success",
        "completed_tasks": report.completed_tasks,
        "generated_files": report.generated_files
    }
```

---

## ❓ 常見問題

### Q1: 支援哪些語言的 Protocol？

A: 目前主要針對英文 Protocol 優化，但 Gemini API 支援多種語言。中文 Protocol 也可以處理，但可能需要調整提示詞。

### Q2: 處理一個 Protocol 需要多長時間？

A: 通常 5-15 分鐘，取決於：
- Protocol PDF 的大小和頁數
- 網路速度
- API 響應時間
- 生成的文件數量

### Q3: 是否需要網路連接？

A: 是的，需要網路連接來調用 Gemini API 進行 Protocol 解析。

### Q4: API 有使用限制嗎？

A: Gemini API 有免費配額限制。詳見 [Google AI Studio 定價](https://ai.google.dev/pricing)。

### Q5: 生成的文件可以編輯嗎？

A: 是的，所有生成的 Word 文件（.docx）都可以使用 Microsoft Word 或其他文書處理軟體編輯。

### Q6: 如何處理大型 Protocol（>100 頁）？

A: 可以在 `ProtocolParser` 中使用 `max_pages` 參數限制解析的頁數：

```python
automation.parse_protocol(max_pages=50)
```

### Q7: 支援 Protocol 更新嗎？

A: 可以重新執行自動化流程。建議使用不同的輸出目錄來保留版本歷史。

### Q8: 如何自訂文件樣式？

A: 可以修改各生成器模組中的樣式設定，或使用 Word 模板。

---

## 📚 範例

完整的使用範例請參考：

- `examples/automation_example.py` - 7 個詳細的使用範例
- `examples/crf_generator_example.py` - CRF 生成範例
- `examples/dvp_example.py` - DVP 生成範例
- `examples/example_user_guide_generation.py` - User Guide 生成範例

### 快速範例

```python
# 最簡單的使用方式
from automation_workflow import ClinicalDocAutomation

automation = ClinicalDocAutomation(
    protocol_pdf="my_protocol.pdf",
    api_key="your-api-key"
)

report = automation.run_all()

print(f"✓ 完成 {report.completed_tasks} 個任務")
print(f"✓ 生成 {len(report.generated_files)} 個檔案")
```

---

## 🤝 支援

如有問題或需要協助，請：

1. 查看日誌檔案 (`automation.log`)
2. 檢查執行報告 (`automation_report.txt`)
3. 參考範例程式碼
4. 查看常見問題

---

## 📝 版本資訊

**版本 1.0** (2025-11-18)

- ✅ Protocol PDF 自動解析
- ✅ CRF 自動生成
- ✅ DVP 自動生成
- ✅ User Guide 自動生成
- ✅ 批次處理支援
- ✅ CLI 介面
- ✅ 詳細報告生成
- ⏳ DMP 生成（計劃中）

---

## 📄 授權

Copyright © 2025 Clinical Documentation Automation Team

---

**Happy Automating! 🎉**
