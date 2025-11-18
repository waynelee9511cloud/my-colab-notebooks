# CLI 命令列參考手冊

## Clinical Document Automation - 命令列介面

---

## 📖 基本語法

```bash
python automation_workflow.py [OPTIONS]
```

---

## 🎯 快速參考

### 最常用的命令

```bash
# 1. 最簡單的使用（生成所有文件）
python automation_workflow.py --protocol protocol.pdf

# 2. 只生成 CRF 和 DVP
python automation_workflow.py --protocol protocol.pdf --generate crf dvp

# 3. 批次處理
python automation_workflow.py --batch p1.pdf p2.pdf p3.pdf

# 4. 顯示詳細日誌
python automation_workflow.py --protocol protocol.pdf --verbose

# 5. 查看幫助
python automation_workflow.py --help
```

---

## 📋 完整參數列表

### 必填參數（二選一）

#### `--protocol <PATH>`
指定單個 Protocol PDF 檔案路徑

**範例**:
```bash
python automation_workflow.py --protocol my_protocol.pdf
python automation_workflow.py --protocol /full/path/to/protocol.pdf
python automation_workflow.py --protocol "../protocols/study_001.pdf"
```

**注意**:
- 路徑可以是相對路徑或絕對路徑
- 檔案必須存在且為有效的 PDF
- 路徑中有空格時需要使用引號

#### `--batch <PATH1> <PATH2> ...`
批次處理多個 Protocol PDF 檔案

**範例**:
```bash
python automation_workflow.py --batch protocol1.pdf protocol2.pdf
python automation_workflow.py --batch protocols/*.pdf
python automation_workflow.py --batch \
  studies/study1/protocol.pdf \
  studies/study2/protocol.pdf \
  studies/study3/protocol.pdf
```

**注意**:
- 可以指定任意數量的檔案
- 支援通配符（如 `*.pdf`）
- 每個 Protocol 會有獨立的輸出目錄

---

### 選填參數

#### `--api-key <KEY>`
指定 Gemini API 金鑰

**範例**:
```bash
python automation_workflow.py --protocol protocol.pdf --api-key "AIzaSy..."
```

**預設值**: 從環境變數 `GEMINI_API_KEY` 讀取

**注意**:
- 建議使用環境變數而非命令列參數（更安全）
- API Key 通常以 `AIzaSy` 開頭
- 使用引號包含整個 Key

**推薦做法**:
```bash
# 設置環境變數
export GEMINI_API_KEY="your-api-key"

# 然後執行，無需 --api-key 參數
python automation_workflow.py --protocol protocol.pdf
```

#### `--output-dir <PATH>`
指定輸出目錄

**範例**:
```bash
python automation_workflow.py --protocol protocol.pdf --output-dir ./output
python automation_workflow.py --protocol protocol.pdf --output-dir "/data/results"
python automation_workflow.py --protocol protocol.pdf --output-dir "../results/study_001"
```

**預設值**: 自動生成（格式: `output_{protocol_name}_{timestamp}`）

**範例預設目錄**: `output_PROTO-001_20251118_120000`

**注意**:
- 如果目錄不存在會自動創建
- 相對路徑從當前工作目錄計算
- 批次處理時，這是基礎目錄，每個 Protocol 會創建子目錄

#### `--generate <TYPE1> <TYPE2> ...`
指定要生成的文件類型

**可用類型**:
- `crf` - Case Report Form
- `dvp` - Data Validation Plan
- `user_guide` - EDC/ePRO User Guide
- `dmp` - Data Management Plan（尚未實現）
- `all` - 所有文件（預設）

**範例**:
```bash
# 只生成 CRF
python automation_workflow.py --protocol protocol.pdf --generate crf

# 生成 CRF 和 DVP
python automation_workflow.py --protocol protocol.pdf --generate crf dvp

# 生成所有文件（明確指定）
python automation_workflow.py --protocol protocol.pdf --generate all

# 生成 User Guide 和 DVP
python automation_workflow.py --protocol protocol.pdf --generate user_guide dvp
```

**預設值**: `all`（生成所有文件）

#### `--verbose` 或 `-v`
顯示詳細的執行日誌

**範例**:
```bash
python automation_workflow.py --protocol protocol.pdf --verbose
python automation_workflow.py --protocol protocol.pdf -v
```

**預設值**: `False`（只顯示關鍵訊息）

**效果**:
- 顯示 DEBUG 級別的日誌
- 顯示詳細的 API 調用資訊
- 顯示每個步驟的詳細進度
- 有助於除錯和監控

**日誌級別對比**:
```
正常模式:   INFO, WARNING, ERROR
Verbose模式: DEBUG, INFO, WARNING, ERROR
```

#### `--no-backup`
禁用備份功能

**範例**:
```bash
python automation_workflow.py --protocol protocol.pdf --no-backup
```

**預設值**: 啟用備份

**效果**:
- 失敗時不會保存已生成的檔案到備份目錄
- 可以節省磁碟空間
- 不建議在生產環境使用

#### `--version`
顯示版本資訊

**範例**:
```bash
python automation_workflow.py --version
```

**輸出範例**:
```
Clinical Document Automation v1.0
```

#### `--help` 或 `-h`
顯示幫助資訊

**範例**:
```bash
python automation_workflow.py --help
python automation_workflow.py -h
```

**輸出**: 顯示所有可用參數和使用範例

---

## 💡 使用範例

### 範例 1: 基本使用

```bash
# 使用環境變數中的 API Key，生成所有文件
export GEMINI_API_KEY="your-api-key"
python automation_workflow.py --protocol my_protocol.pdf
```

**輸出目錄**: `output_my_protocol_20251118_120000/`

### 範例 2: 自訂輸出目錄

```bash
# 將輸出保存到指定目錄
python automation_workflow.py \
  --protocol my_protocol.pdf \
  --output-dir ./study_001_documents
```

**輸出目錄**: `./study_001_documents/`

### 範例 3: 選擇性生成

```bash
# 只生成 CRF 和 DVP，不生成 User Guide
python automation_workflow.py \
  --protocol my_protocol.pdf \
  --generate crf dvp
```

### 範例 4: 批次處理

```bash
# 批次處理 3 個 Protocol
python automation_workflow.py \
  --batch \
    protocols/study_001.pdf \
    protocols/study_002.pdf \
    protocols/study_003.pdf \
  --output-dir ./batch_results
```

**輸出結構**:
```
batch_results/
├── study_001_20251118_120000/
│   ├── CRF_...docx
│   ├── DVP_...docx
│   └── ...
├── study_002_20251118_120015/
│   └── ...
└── study_003_20251118_120030/
    └── ...
```

### 範例 5: 詳細日誌模式

```bash
# 顯示詳細日誌，用於除錯
python automation_workflow.py \
  --protocol my_protocol.pdf \
  --verbose
```

### 範例 6: 完整參數範例

```bash
# 使用所有主要參數
python automation_workflow.py \
  --protocol /data/protocols/PROTO-2025-001.pdf \
  --api-key "AIzaSy..." \
  --output-dir /data/output/PROTO-2025-001 \
  --generate crf dvp user_guide \
  --verbose
```

### 範例 7: 使用通配符批次處理

```bash
# 處理目錄中所有 PDF
python automation_workflow.py \
  --batch protocols/*.pdf \
  --output-dir ./all_protocols_output
```

---

## 🔄 退出碼

程式執行完成後會返回退出碼：

| 退出碼 | 意義 | 說明 |
|--------|------|------|
| `0` | 成功 | 所有任務成功完成 |
| `1` | 失敗 | 有任務執行失敗 |
| `130` | 中斷 | 使用者中斷執行（Ctrl+C） |

**使用範例**:
```bash
python automation_workflow.py --protocol protocol.pdf

# 檢查退出碼
if [ $? -eq 0 ]; then
    echo "成功！"
else
    echo "失敗！"
fi
```

---

## 🌍 環境變數

### `GEMINI_API_KEY`

Gemini API 金鑰

**設置方法**:

```bash
# Linux/Mac (bash/zsh)
export GEMINI_API_KEY="your-api-key"

# Linux/Mac (永久設置，添加到 ~/.bashrc 或 ~/.zshrc)
echo 'export GEMINI_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc

# Windows (CMD)
set GEMINI_API_KEY=your-api-key

# Windows (永久設置)
setx GEMINI_API_KEY "your-api-key"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"

# Windows (永久設置，PowerShell)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-api-key', 'User')
```

**驗證設置**:
```bash
# Linux/Mac
echo $GEMINI_API_KEY

# Windows (CMD)
echo %GEMINI_API_KEY%

# Windows (PowerShell)
echo $env:GEMINI_API_KEY
```

---

## 🔍 錯誤處理

### 常見錯誤訊息

#### 錯誤: 找不到 Protocol PDF

```
錯誤: FileNotFoundError: Protocol PDF 不存在: protocol.pdf
```

**解決方法**:
```bash
# 檢查檔案是否存在
ls -la protocol.pdf

# 使用絕對路徑
python automation_workflow.py --protocol /absolute/path/to/protocol.pdf
```

#### 錯誤: API Key 未設置

```
錯誤: 必須提供 API Key（使用 --api-key 或設置環境變數 GEMINI_API_KEY）
```

**解決方法**:
```bash
# 方法 1: 設置環境變數
export GEMINI_API_KEY="your-key"

# 方法 2: 使用命令列參數
python automation_workflow.py --protocol protocol.pdf --api-key "your-key"
```

#### 錯誤: 必須指定參數

```
錯誤: 必須指定 --protocol 或 --batch 參數
```

**解決方法**:
```bash
# 提供 Protocol 檔案
python automation_workflow.py --protocol protocol.pdf

# 或使用批次模式
python automation_workflow.py --batch protocol1.pdf protocol2.pdf
```

#### 錯誤: 參數衝突

```
錯誤: --protocol 和 --batch 不能同時使用
```

**解決方法**:
```bash
# 只使用其中一個
python automation_workflow.py --protocol protocol.pdf

# 或
python automation_workflow.py --batch protocol1.pdf protocol2.pdf
```

---

## 📊 輸出說明

執行成功後，會在輸出目錄看到以下結構：

```
output_PROTOCOL-001_20251118_120000/
├── protocol_info.json              # Protocol 解析結果（JSON）
├── CRF_PROTOCOL-001.docx           # Case Report Form 文件
├── DVP_PROTOCOL-001.docx           # Data Validation Plan 文件
├── UserGuide_PROTOCOL-001.docx     # EDC/ePRO User Guide 文件
├── UserGuide_Screenshots.txt       # 截圖需求清單
├── automation.log                   # 詳細執行日誌
├── automation_report.json          # 結構化執行報告
├── automation_report.txt           # 人類可讀執行報告
└── _backup/                         # 備份目錄（如果啟用且有失敗）
```

---

## 🚀 Shell 腳本整合

### 批次腳本範例（Bash）

```bash
#!/bin/bash
# batch_process.sh - 批次處理多個 Protocol

export GEMINI_API_KEY="your-api-key"

PROTOCOLS=(
  "protocols/study_001.pdf"
  "protocols/study_002.pdf"
  "protocols/study_003.pdf"
)

for protocol in "${PROTOCOLS[@]}"; do
  echo "處理: $protocol"
  python automation_workflow.py \
    --protocol "$protocol" \
    --output-dir "./output/$(basename $protocol .pdf)" \
    --generate crf dvp \
    --verbose

  if [ $? -eq 0 ]; then
    echo "✓ 成功: $protocol"
  else
    echo "✗ 失敗: $protocol"
  fi
done
```

### Windows 批次腳本範例（batch.bat）

```batch
@echo off
REM batch_process.bat - Windows 批次處理

set GEMINI_API_KEY=your-api-key

python automation_workflow.py --protocol protocols\study_001.pdf
if %ERRORLEVEL% EQU 0 (
    echo 成功: study_001.pdf
) else (
    echo 失敗: study_001.pdf
)

python automation_workflow.py --protocol protocols\study_002.pdf
if %ERRORLEVEL% EQU 0 (
    echo 成功: study_002.pdf
) else (
    echo 失敗: study_002.pdf
)
```

### PowerShell 腳本範例

```powershell
# batch_process.ps1 - PowerShell 批次處理

$env:GEMINI_API_KEY = "your-api-key"

$protocols = @(
    "protocols\study_001.pdf",
    "protocols\study_002.pdf",
    "protocols\study_003.pdf"
)

foreach ($protocol in $protocols) {
    Write-Host "處理: $protocol"

    python automation_workflow.py `
        --protocol $protocol `
        --generate crf dvp `
        --verbose

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 成功: $protocol" -ForegroundColor Green
    } else {
        Write-Host "✗ 失敗: $protocol" -ForegroundColor Red
    }
}
```

---

## 💻 與其他工具整合

### Make

```makefile
# Makefile

.PHONY: all clean test

PROTOCOL ?= protocol.pdf
OUTPUT_DIR ?= output

all:
	python automation_workflow.py \
		--protocol $(PROTOCOL) \
		--output-dir $(OUTPUT_DIR)

crf:
	python automation_workflow.py \
		--protocol $(PROTOCOL) \
		--generate crf \
		--output-dir $(OUTPUT_DIR)

batch:
	python automation_workflow.py \
		--batch protocols/*.pdf \
		--output-dir batch_output

clean:
	rm -rf output_*/ batch_output/

test:
	python test_installation.py
```

使用:
```bash
make                              # 處理 protocol.pdf
make PROTOCOL=my_protocol.pdf     # 處理指定 Protocol
make crf PROTOCOL=protocol.pdf    # 只生成 CRF
make batch                        # 批次處理
make clean                        # 清理輸出
make test                         # 測試安裝
```

---

## 📚 更多資源

- [完整文檔](AUTOMATION_WORKFLOW_README.md)
- [快速開始](QUICKSTART_AUTOMATION.md)
- [工作流程總結](WORKFLOW_SUMMARY.md)
- [Python API 文檔](automation_workflow.py)
- [使用範例](examples/automation_example.py)

---

**版本**: 1.0
**更新日期**: 2025-11-18
