# Protocol PDF 解析器模組

## 概述

智能 Protocol PDF 解析器是一個用於從臨床試驗 Protocol 文件中自動提取關鍵資訊的 Python 模組。它結合了 PDF 文本提取技術和 Google Gemini AI 的自然語言處理能力，能夠智能識別和提取 Protocol 中的各種結構化資訊。

## 功能特點

### 核心功能
- ✅ **PDF 文本提取**: 使用 pdfplumber 高效提取 PDF 文本內容
- ✅ **AI 智能解析**: 整合 Google Gemini API 進行智能資訊提取
- ✅ **結構化輸出**: 提供標準化的 JSON 格式輸出
- ✅ **完整錯誤處理**: 包含完善的異常處理和日誌記錄
- ✅ **免費 API**: 支持使用免費的 Gemini 1.5 Flash 模型

### 提取的資訊

模組可以提取以下 Protocol 關鍵資訊：

1. **基本資訊**
   - Study Title (試驗標題)
   - Protocol Number (試驗編號)
   - Sponsor (贊助商)
   - Phase (試驗階段)

2. **試驗設計**
   - Study Design (試驗設計類型)
   - Target Population (目標族群)
   - Sample Size (樣本數)

3. **時程與評估**
   - Visit Schedule (訪視時程)
   - Primary Endpoints (主要終點指標)
   - Secondary Endpoints (次要終點指標)

4. **受試者標準**
   - Inclusion Criteria (納入標準)
   - Exclusion Criteria (排除標準)

5. **CRF 需求**
   - CRF Domains (所需的 CRF 表單領域)

## 安裝

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install pdfplumber google-generativeai python-dotenv
```

### 2. 獲取 Google Gemini API 金鑰

1. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用 Google 帳號登入
3. 點擊 "Create API Key" 創建新的 API 金鑰
4. 複製 API 金鑰

**注意**: Gemini 1.5 Flash 模型是完全免費的，適合大多數使用場景。

### 3. 設置 API 金鑰

**方式 1: 環境變數（推薦）**

```bash
export GEMINI_API_KEY="your-api-key-here"
```

或在 Python 中：

```python
import os
os.environ["GEMINI_API_KEY"] = "your-api-key-here"
```

**方式 2: 直接傳入**

```python
parser = ProtocolParser(api_key="your-api-key-here")
```

## 使用方法

### 基本使用

```python
from modules.protocol_parser import ProtocolParser

# 初始化解析器
parser = ProtocolParser(api_key="YOUR_API_KEY")

# 解析 Protocol PDF
protocol_info = parser.parse_protocol("path/to/protocol.pdf")

# 訪問提取的資訊
print(protocol_info.study_title)
print(protocol_info.protocol_number)
print(protocol_info.phase)

# 保存為 JSON
parser.save_to_json(protocol_info, "output/protocol_info.json")
```

### 進階使用

```python
# 只讀取前 30 頁（加快處理速度）
protocol_info = parser.parse_protocol("protocol.pdf", max_pages=30)

# 使用不同的模型
parser = ProtocolParser(
    api_key="YOUR_API_KEY",
    model_name="gemini-1.5-pro"  # 更強大但可能有額度限制
)

# 獲取 JSON 字符串
json_str = protocol_info.to_json()

# 轉換為字典
data_dict = protocol_info.to_dict()

# 訪問列表資訊
for visit in protocol_info.visit_schedule:
    print(f"訪視: {visit}")

for endpoint in protocol_info.primary_endpoints:
    print(f"主要終點: {endpoint}")

for criterion in protocol_info.inclusion_criteria:
    print(f"納入標準: {criterion}")
```

### 完整範例

```python
import os
from pathlib import Path
from modules.protocol_parser import ProtocolParser

def main():
    # 設置 API 金鑰
    os.environ["GEMINI_API_KEY"] = "your-api-key-here"

    # 初始化解析器
    parser = ProtocolParser()

    # 設置路徑
    pdf_path = "protocols/study_protocol.pdf"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    try:
        # 解析 Protocol
        print(f"正在解析: {pdf_path}")
        protocol_info = parser.parse_protocol(pdf_path)

        # 顯示基本資訊
        print(f"\n試驗標題: {protocol_info.study_title}")
        print(f"Protocol 編號: {protocol_info.protocol_number}")
        print(f"試驗階段: {protocol_info.phase}")

        # 顯示 CRF 領域
        print(f"\n所需 CRF 領域:")
        for domain in protocol_info.crf_domains or []:
            print(f"  - {domain}")

        # 保存結果
        output_file = output_dir / f"{protocol_info.protocol_number}_info.json"
        parser.save_to_json(protocol_info, str(output_file))
        print(f"\n✓ 結果已保存至: {output_file}")

    except Exception as e:
        print(f"✗ 錯誤: {e}")

if __name__ == "__main__":
    main()
```

## 輸出格式

解析器輸出的 JSON 格式範例：

```json
{
  "study_title": "A Phase 3, Randomized, Double-Blind Study...",
  "protocol_number": "ABC-123-2024",
  "sponsor": "XYZ Pharmaceutical Company",
  "phase": "Phase III",
  "study_design": "Randomized, Double-Blind, Placebo-Controlled",
  "target_population": "Adults with Type 2 Diabetes",
  "sample_size": "500 subjects",
  "visit_schedule": [
    "Screening",
    "Baseline (Day 1)",
    "Week 4",
    "Week 8",
    "Week 12",
    "Week 24 (End of Treatment)"
  ],
  "primary_endpoints": [
    "Change from baseline in HbA1c at Week 24"
  ],
  "secondary_endpoints": [
    "Change from baseline in fasting plasma glucose",
    "Proportion of subjects achieving HbA1c <7%"
  ],
  "inclusion_criteria": [
    "Age ≥18 years",
    "Diagnosis of Type 2 Diabetes Mellitus",
    "HbA1c between 7.0% and 10.5%",
    "BMI ≤45 kg/m²"
  ],
  "exclusion_criteria": [
    "Type 1 Diabetes or secondary diabetes",
    "Severe renal impairment (eGFR <30 mL/min/1.73m²)",
    "History of diabetic ketoacidosis"
  ],
  "crf_domains": [
    "Demographics",
    "Vital Signs",
    "Adverse Events",
    "Concomitant Medications",
    "Laboratory",
    "ECG",
    "Physical Examination",
    "Efficacy Assessments",
    "Quality of Life"
  ]
}
```

## 常見 CRF 領域

解析器可識別的常見 CRF 領域包括：

- **Demographics** (人口學資料)
- **Vital Signs** (生命徵象)
- **Adverse Events** (不良事件)
- **Concomitant Medications** (併用藥物)
- **Laboratory** (實驗室檢查)
- **ECG** (心電圖)
- **Physical Examination** (身體檢查)
- **Medical History** (病史)
- **Efficacy Assessments** (療效評估)
- **Quality of Life** (生活品質)
- **Pharmacokinetics** (藥物動力學)
- **Inclusion/Exclusion Criteria** (納入/排除標準確認)
- **Informed Consent** (知情同意)
- **Prior/Concomitant Therapy** (先前/併用治療)

## 性能優化建議

### 1. 處理大型 PDF
```python
# 對於超過 100 頁的 Protocol，建議只讀取關鍵頁面
protocol_info = parser.parse_protocol("large_protocol.pdf", max_pages=50)
```

### 2. 批次處理
```python
import time

protocols = ["protocol1.pdf", "protocol2.pdf", "protocol3.pdf"]

for pdf in protocols:
    protocol_info = parser.parse_protocol(pdf)
    parser.save_to_json(protocol_info, f"output/{pdf.stem}_info.json")
    time.sleep(2)  # 避免 API 速率限制
```

### 3. 錯誤處理
```python
try:
    protocol_info = parser.parse_protocol("protocol.pdf")
except FileNotFoundError:
    print("PDF 檔案不存在")
except ValueError:
    print("API 金鑰未設置")
except Exception as e:
    print(f"處理錯誤: {e}")
    # 記錄錯誤日誌或發送通知
```

## 故障排除

### 問題 1: 找不到 PDF 檔案
```
FileNotFoundError: PDF檔案不存在
```

**解決方案**: 確認 PDF 檔案路徑正確，使用絕對路徑或確保相對路徑正確。

### 問題 2: API 金鑰錯誤
```
ValueError: Gemini API未正確配置
```

**解決方案**:
1. 檢查 API 金鑰是否正確設置
2. 確認環境變數 `GEMINI_API_KEY` 已設置
3. 嘗試直接傳入 API 金鑰到 ProtocolParser 初始化

### 問題 3: JSON 解析失敗
```
JSONDecodeError: JSON解析失敗
```

**解決方案**:
1. 檢查日誌中的原始回應
2. 可能是 PDF 文本品質問題，嘗試使用更清晰的 PDF
3. 嘗試使用更強大的模型（gemini-1.5-pro）

### 問題 4: 提取資訊不完整

**解決方案**:
1. 增加 `max_pages` 參數，讀取更多頁面
2. 檢查 Protocol PDF 是否包含所需資訊
3. 查看 `raw_data` 欄位了解 AI 的原始回應

## API 使用限制

### Gemini 1.5 Flash (免費)
- ✅ 完全免費
- ✅ 每分鐘 15 次請求
- ✅ 每天 1,500 次請求
- ✅ 適合大多數使用場景

### Gemini 1.5 Pro
- ⚠️ 可能有額度限制
- ✅ 更強大的理解能力
- ✅ 更準確的提取結果

## 最佳實踐

1. **使用環境變數**: 將 API 金鑰存儲在環境變數中，不要硬編碼
2. **日誌記錄**: 保留處理日誌以便追蹤和調試
3. **結果驗證**: 提取後檢查資料完整性和準確性
4. **版本控制**: 保存提取結果的版本，便於追蹤變更
5. **批次處理**: 處理多個檔案時添加適當的延遲避免速率限制

## 擴展開發

### 添加自定義欄位

編輯 `ProtocolInfo` 類別：

```python
@dataclass
class ProtocolInfo:
    # ... 現有欄位 ...
    custom_field: Optional[str] = None
```

修改提示詞模板以提取新欄位：

```python
def _create_extraction_prompt(self, text: str) -> str:
    # 在提示詞中添加新欄位的提取指示
    # ...
```

### 整合其他 LLM

```python
class CustomProtocolParser(ProtocolParser):
    def extract_info_with_custom_llm(self, text: str) -> Dict[str, Any]:
        # 實現自定義 LLM 整合
        pass
```

## 授權

本模組為臨床數據自動化專案的一部分，供內部使用。

## 聯絡方式

如有問題或建議，請聯繫開發團隊。

---

**最後更新**: 2025-11-18
**版本**: 1.0.0
