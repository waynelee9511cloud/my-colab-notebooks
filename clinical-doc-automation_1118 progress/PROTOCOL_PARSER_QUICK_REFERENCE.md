# Protocol Parser 快速參考卡

## 一行命令開始

```python
from modules.protocol_parser import ProtocolParser; parser = ProtocolParser(api_key="YOUR_KEY"); info = parser.parse_protocol("protocol.pdf"); parser.save_to_json(info, "output.json")
```

---

## 基本操作

### 初始化
```python
from modules.protocol_parser import ProtocolParser
parser = ProtocolParser(api_key="YOUR_GEMINI_API_KEY")
```

### 解析 PDF
```python
protocol_info = parser.parse_protocol("protocol.pdf")
```

### 訪問資料
```python
print(protocol_info.study_title)
print(protocol_info.protocol_number)
print(protocol_info.crf_domains)
```

### 保存結果
```python
parser.save_to_json(protocol_info, "output.json")
```

---

## 常用選項

### 只讀前 50 頁
```python
protocol_info = parser.parse_protocol("protocol.pdf", max_pages=50)
```

### 使用環境變數
```bash
export GEMINI_API_KEY="your-key"
```
```python
parser = ProtocolParser()  # 自動讀取環境變數
```

### 使用 Pro 模型
```python
parser = ProtocolParser(api_key="KEY", model_name="gemini-1.5-pro")
```

---

## 提取的資訊

```python
protocol_info.study_title           # 試驗標題
protocol_info.protocol_number       # Protocol 編號
protocol_info.sponsor               # 贊助商
protocol_info.phase                 # 試驗階段
protocol_info.study_design          # 試驗設計
protocol_info.target_population     # 目標族群
protocol_info.sample_size           # 樣本數
protocol_info.visit_schedule        # 訪視時程 (List)
protocol_info.primary_endpoints     # 主要終點 (List)
protocol_info.secondary_endpoints   # 次要終點 (List)
protocol_info.inclusion_criteria    # 納入標準 (List)
protocol_info.exclusion_criteria    # 排除標準 (List)
protocol_info.crf_domains           # CRF 領域 (List)
```

---

## 輸出格式

### JSON 字符串
```python
json_str = protocol_info.to_json()
```

### Python 字典
```python
data_dict = protocol_info.to_dict()
```

### 保存到檔案
```python
parser.save_to_json(protocol_info, "output.json")
```

---

## 批次處理

```python
from pathlib import Path
import time

for pdf in Path("protocols/").glob("*.pdf"):
    info = parser.parse_protocol(str(pdf))
    parser.save_to_json(info, f"output/{pdf.stem}.json")
    time.sleep(2)  # 避免 API 速率限制
```

---

## 錯誤處理

```python
try:
    protocol_info = parser.parse_protocol("protocol.pdf")
except FileNotFoundError:
    print("PDF 檔案不存在")
except ValueError:
    print("API 金鑰未設置")
except Exception as e:
    print(f"錯誤: {e}")
```

---

## 在 Colab 使用

```python
# 安裝
!pip install -q pdfplumber google-generativeai

# 上傳 PDF
from google.colab import files
uploaded = files.upload()

# 解析
from modules.protocol_parser import ProtocolParser
parser = ProtocolParser(api_key="YOUR_KEY")
info = parser.parse_protocol(list(uploaded.keys())[0])

# 顯示
print(info.to_json())

# 下載結果
parser.save_to_json(info, "output.json")
files.download("output.json")
```

---

## 檔案位置

| 檔案 | 路徑 |
|------|------|
| 主模組 | `modules/protocol_parser.py` |
| Python 範例 | `examples/protocol_parser_example.py` |
| Notebook 範例 | `examples/Protocol_Parser_Demo.ipynb` |
| 完整文檔 | `modules/README_PROTOCOL_PARSER.md` |
| 快速入門 | `QUICKSTART_PROTOCOL_PARSER.md` |
| 測試腳本 | `modules/test_protocol_parser.py` |

---

## API 資訊

- **獲取金鑰**: https://makersuite.google.com/app/apikey
- **免費額度**: 1,500 次/天
- **推薦模型**: `gemini-1.5-flash` (免費)
- **進階模型**: `gemini-1.5-pro`

---

## 常見 CRF 領域

- Demographics
- Vital Signs
- Adverse Events
- Concomitant Medications
- Laboratory
- ECG
- Physical Examination
- Medical History
- Efficacy Assessments
- Quality of Life
- Pharmacokinetics

---

## 疑難排解

| 問題 | 解決方案 |
|------|----------|
| 模組導入失敗 | `pip install pdfplumber google-generativeai` |
| API 未配置 | 設置 `GEMINI_API_KEY` 環境變數 |
| JSON 解析失敗 | 嘗試使用 `gemini-1.5-pro` 模型 |
| 提取不完整 | 增加 `max_pages` 或檢查 PDF 品質 |

---

## 快速測試

```bash
# 檢查安裝
python -c "import pdfplumber, google.generativeai; print('✓ OK')"

# 檢查語法
python -m py_compile modules/protocol_parser.py

# 執行測試
cd modules && python test_protocol_parser.py
```

---

**需要幫助?** 查看完整文檔: `modules/README_PROTOCOL_PARSER.md`
