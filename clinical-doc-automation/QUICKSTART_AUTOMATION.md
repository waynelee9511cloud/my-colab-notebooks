# 快速開始指南

## 臨床試驗文件自動化工作流程 - 5 分鐘上手

---

## 🎯 3 步驟快速開始

### 步驟 1: 準備 API Key

```bash
# 訪問 Google AI Studio 獲取免費 API Key
# https://makersuite.google.com/app/apikey

# 設置環境變數（推薦）
export GEMINI_API_KEY="your-api-key-here"
```

### 步驟 2: 準備 Protocol PDF

確保您有一個 Protocol PDF 檔案，例如 `my_protocol.pdf`

### 步驟 3: 執行自動化

```bash
# 進入專案目錄
cd clinical-doc-automation

# 執行自動化（生成所有文件）
python automation_workflow.py --protocol my_protocol.pdf
```

✅ 完成！所有文件已自動生成在輸出目錄中。

---

## 📋 生成的文件

執行完成後，您會在輸出目錄中看到：

```
output_my_protocol_20251118_120000/
├── CRF_PROTO-001.docx           ✓ Case Report Form
├── DVP_PROTO-001.docx           ✓ Data Validation Plan
├── UserGuide_PROTO-001.docx     ✓ EDC/ePRO User Guide
├── protocol_info.json           ✓ Protocol 資訊（JSON）
├── automation_report.txt        ✓ 執行報告
└── automation.log               ✓ 詳細日誌
```

---

## 🎨 常用命令

### 1. 生成所有文件（預設）

```bash
python automation_workflow.py --protocol protocol.pdf
```

### 2. 只生成 CRF 和 DVP

```bash
python automation_workflow.py \
  --protocol protocol.pdf \
  --generate crf dvp
```

### 3. 自訂輸出目錄

```bash
python automation_workflow.py \
  --protocol protocol.pdf \
  --output-dir ./my_output
```

### 4. 顯示詳細日誌

```bash
python automation_workflow.py \
  --protocol protocol.pdf \
  --verbose
```

### 5. 批次處理多個 Protocol

```bash
python automation_workflow.py \
  --batch protocol1.pdf protocol2.pdf protocol3.pdf
```

---

## 🐍 Python 程式使用

### 基本使用

```python
from automation_workflow import ClinicalDocAutomation

# 創建自動化實例
automation = ClinicalDocAutomation(
    protocol_pdf="my_protocol.pdf",
    api_key="your-api-key",  # 或從環境變數讀取
    verbose=True
)

# 執行所有任務
report = automation.run_all()

# 查看結果
print(f"完成: {report.completed_tasks}/{report.total_tasks}")
for file in report.generated_files:
    print(f"✓ {file}")
```

### 選擇性生成

```python
# 只生成 CRF 和 User Guide
report = automation.run_all(
    generate_types=['crf', 'user_guide']
)
```

---

## 📊 查看執行報告

### 查看文字報告

```bash
cat output_*/automation_report.txt
```

### 查看 JSON 報告

```bash
cat output_*/automation_report.json | python -m json.tool
```

### 查看日誌

```bash
# 查看完整日誌
cat output_*/automation.log

# 只查看錯誤
grep ERROR output_*/automation.log

# 只查看警告
grep WARNING output_*/automation.log
```

---

## 🔧 常見設定

### 使用環境變數（推薦）

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key"

# Windows (CMD)
set GEMINI_API_KEY=your-api-key

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"

# 然後直接執行，無需指定 --api-key
python automation_workflow.py --protocol protocol.pdf
```

### 創建設定檔

建立 `.env` 檔案：

```bash
# .env
GEMINI_API_KEY=your-api-key-here
```

然後在 Python 中：

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

---

## ⚠️ 常見問題快速解決

### 問題 1: 找不到 Protocol PDF

```
錯誤: FileNotFoundError: Protocol PDF 不存在
解決: 使用絕對路徑或確認檔案存在
```

```bash
# 使用絕對路徑
python automation_workflow.py --protocol /full/path/to/protocol.pdf

# 或先確認檔案存在
ls -la protocol.pdf
```

### 問題 2: 沒有設定 API Key

```
錯誤: 必須提供 API Key
解決: 設定環境變數或使用 --api-key 參數
```

```bash
# 方法 1: 環境變數
export GEMINI_API_KEY="your-key"

# 方法 2: 命令列參數
python automation_workflow.py --protocol protocol.pdf --api-key "your-key"
```

### 問題 3: 缺少依賴套件

```
錯誤: ModuleNotFoundError: No module named 'xxx'
解決: 安裝所需套件
```

```bash
pip install -r requirements.txt
```

---

## 📚 進階使用

更多進階功能和詳細說明，請參考：

- 📖 [完整文檔](AUTOMATION_WORKFLOW_README.md)
- 💡 [使用範例](examples/automation_example.py)
- 🔍 [API 文檔](automation_workflow.py) - 查看程式碼中的 docstrings

---

## 🎯 使用技巧

### 技巧 1: 先測試小規模

```bash
# 只生成一個文件來測試
python automation_workflow.py \
  --protocol protocol.pdf \
  --generate crf
```

### 技巧 2: 使用 verbose 模式除錯

```bash
# 顯示詳細執行過程
python automation_workflow.py \
  --protocol protocol.pdf \
  --verbose
```

### 技巧 3: 保留輸出歷史

```bash
# 使用有意義的輸出目錄名稱
python automation_workflow.py \
  --protocol protocol.pdf \
  --output-dir ./output_v1.0

python automation_workflow.py \
  --protocol protocol_updated.pdf \
  --output-dir ./output_v1.1
```

### 技巧 4: 批次處理使用通配符

```bash
# 處理資料夾中所有 Protocol
python automation_workflow.py \
  --batch protocols/*.pdf
```

---

## 📈 效能優化

### 1. Protocol 太大時

如果 Protocol 超過 100 頁，可以限制解析頁數：

修改 `automation_workflow.py` 中的 `parse_protocol` 方法：

```python
self.protocol_info = parser.parse_protocol(
    str(self.protocol_pdf),
    max_pages=50  # 只解析前 50 頁
)
```

### 2. 批次處理時

批次處理時建議：
- 分批執行（每次 5-10 個）
- 注意 API 配額限制
- 在非尖峰時段執行

---

## ✅ 檢查清單

開始之前，確認：

- [ ] Python 3.8+ 已安裝
- [ ] 依賴套件已安裝 (`pip install -r requirements.txt`)
- [ ] Gemini API Key 已獲取並設置
- [ ] Protocol PDF 檔案已準備
- [ ] 有足夠的磁碟空間（至少 500MB）
- [ ] 網路連接正常

執行後，確認：

- [ ] 輸出目錄已創建
- [ ] 所有文件已生成
- [ ] 執行報告顯示成功
- [ ] 沒有錯誤訊息

---

## 🚀 現在就開始！

```bash
# 最簡單的命令
export GEMINI_API_KEY="your-key"
python automation_workflow.py --protocol your_protocol.pdf
```

**就是這麼簡單！** 🎉

---

需要更多幫助？

- 📖 查看 [完整文檔](AUTOMATION_WORKFLOW_README.md)
- 💻 查看 [範例程式](examples/automation_example.py)
- 📝 查看 [日誌檔案](output_*/automation.log)
