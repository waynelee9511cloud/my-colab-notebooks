# 臨床試驗文件自動化系統 - 系統架構

## 🏗️ 系統架構圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                   臨床試驗文件自動化系統                                │
│              Clinical Trial Document Automation System              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         輸入層 (Input Layer)                         │
├─────────────────────────────────────────────────────────────────────┤
│  📄 Protocol PDF    🖼️ Logo 圖片    📋 Word 範本    🔑 API Key      │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      互動介面層 (UI Layer)                            │
├─────────────────────────────────────────────────────────────────────┤
│  • ipywidgets 互動式介面                                              │
│  • 檔案上傳控制                                                       │
│  • 參數設定面板                                                       │
│  • 進度顯示                                                          │
│  • 下載控制                                                          │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      處理層 (Processing Layer)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐      ┌──────────────────┐                    │
│  │ Protocol Parser  │ ───> │  Protocol Info   │                    │
│  │  試驗書解析器     │      │   結構化資料      │                    │
│  └──────────────────┘      └──────────────────┘                    │
│           ↓                                                          │
│  ┌─────────────────────────────────────────────────────┐           │
│  │              核心生成模組 (Core Generators)           │           │
│  ├─────────────────────────────────────────────────────┤           │
│  │                                                       │           │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │           │
│  │  │CRF Generator│  │DVP Generator│  │User Guide   │ │           │
│  │  │CRF 生成器   │  │DVP 生成器   │  │Generator    │ │           │
│  │  └─────────────┘  └─────────────┘  │使用手冊生成器│ │           │
│  │                                     └─────────────┘ │           │
│  └─────────────────────────────────────────────────────┘           │
│           ↓                                                          │
│  ┌──────────────────┐                                               │
│  │ Word Formatter   │                                               │
│  │  文件格式化工具   │                                               │
│  └──────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      輸出層 (Output Layer)                           │
├─────────────────────────────────────────────────────────────────────┤
│  📄 Protocol_Info.json                                               │
│  📝 Protocol_CRF.docx                                                │
│  📊 Protocol_DVP.docx                                                │
│  📋 Protocol_DVP_rules.json                                          │
│  📖 Protocol_User_Guide.docx                                         │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     下載層 (Download Layer)                          │
├─────────────────────────────────────────────────────────────────────┤
│  💾 個別檔案下載    📦 ZIP 壓縮下載                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 資料流程圖

```
Protocol PDF
     │
     ↓
┌────────────────────┐
│ PDF Text Extract   │ ← pdfplumber
└────────────────────┘
     │
     ↓
┌────────────────────┐
│  Gemini AI Parse   │ ← Google Gemini API
└────────────────────┘
     │
     ↓
┌────────────────────┐
│  Protocol Info     │ (JSON)
│  - Study Title     │
│  - Protocol Number │
│  - Sponsor         │
│  - Phase           │
│  - Visit Schedule  │
│  - Endpoints       │
│  - Criteria        │
│  - CRF Domains     │
└────────────────────┘
     │
     ├──────────────────────┬──────────────────────┐
     ↓                      ↓                      ↓
┌──────────┐         ┌──────────┐         ┌──────────┐
│   CRF    │         │   DVP    │         │  Guide   │
│Generator │         │Generator │         │Generator │
└──────────┘         └──────────┘         └──────────┘
     │                      │                      │
     ↓                      ↓                      ↓
┌──────────┐         ┌──────────┐         ┌──────────┐
│CRF Fields│         │Validation│         │Form      │
│& Forms   │         │Rules     │         │Instructions│
└──────────┘         └──────────┘         └──────────┘
     │                      │                      │
     └──────────────────────┴──────────────────────┘
                           ↓
                  ┌──────────────┐
                  │Word Formatter│
                  └──────────────┘
                           ↓
                  ┌──────────────┐
                  │ Word Docs    │
                  └──────────────┘
```

---

## 📦 模組依賴關係

```
Clinical_Trial_Document_Automation_System.ipynb
│
├── modules/
│   │
│   ├── protocol_parser.py
│   │   ├── pdfplumber (PDF 讀取)
│   │   ├── google.generativeai (AI 解析)
│   │   └── json (資料儲存)
│   │
│   ├── crf_generator.py
│   │   ├── google.generativeai (AI 生成)
│   │   ├── python-docx (Word 文件)
│   │   └── protocol_parser (Protocol 資訊)
│   │
│   ├── dvp_generator.py
│   │   ├── python-docx (Word 文件)
│   │   ├── dataclasses (資料結構)
│   │   └── enum (列舉類型)
│   │
│   ├── user_guide_generator.py
│   │   ├── python-docx (Word 文件)
│   │   └── PIL (圖片處理)
│   │
│   └── word_formatter.py
│       ├── python-docx (Word 文件)
│       ├── PIL (圖片處理)
│       └── lxml (XML 處理)
│
└── requirements.txt
```

---

## 🎯 核心技術棧

### 前端（使用者介面）
- **ipywidgets**: 互動式控制元件
- **IPython.display**: 輸出顯示
- **HTML/CSS**: 介面美化

### 後端（資料處理）
- **Google Gemini API**: AI 解析和生成
- **pdfplumber**: PDF 文字提取
- **python-docx**: Word 文件操作
- **PIL (Pillow)**: 圖片處理
- **pandas**: 資料處理

### 輔助工具
- **json**: 資料交換
- **pathlib**: 檔案路徑處理
- **datetime**: 時間戳記
- **zipfile**: 檔案壓縮

---

## 🔧 核心模組詳解

### 1. Protocol Parser（試驗書解析器）

**輸入：**
- Protocol PDF 檔案
- API Key
- 模型名稱（flash/pro）
- 最大頁數（可選）

**處理：**
1. 使用 pdfplumber 提取 PDF 文字
2. 將文字分段處理
3. 使用 Gemini AI 智能解析
4. 提取結構化資訊

**輸出：**
- ProtocolInfo 物件（包含所有關鍵資訊）
- JSON 格式檔案

**關鍵類別：**
```python
class ProtocolInfo:
    study_title: str
    protocol_number: str
    sponsor: str
    phase: str
    study_design: str
    target_population: str
    sample_size: str
    visit_schedule: List[str]
    primary_endpoints: List[str]
    secondary_endpoints: List[str]
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    crf_domains: List[str]
```

---

### 2. CRF Generator（CRF 生成器）

**輸入：**
- Protocol Info
- API Key
- 自訂欄位（可選）

**處理：**
1. 分析 Protocol 資訊
2. 使用 AI 生成 CRF 結構
3. 建立表單和欄位
4. 格式化 Word 文件

**輸出：**
- CRF Word 文件（.docx）

**支援欄位類型：**
- text（文字）
- numeric（數字）
- date（日期）
- time（時間）
- dropdown（下拉選單）
- checkbox（核取方塊）
- radio（單選按鈕）

---

### 3. DVP Generator（DVP 生成器）

**輸入：**
- Protocol Info
- CRF Fields 列表

**處理：**
1. 分析欄位特性
2. 自動生成驗證規則
3. 分類規則類型
4. 建立 DVP 文件

**輸出：**
- DVP Word 文件（.docx）
- 驗證規則 JSON（.json）

**驗證規則類型：**
```python
class ValidationType(Enum):
    RANGE_CHECK = "Range Check"
    REQUIRED_FIELD = "Required Field"
    CONSISTENCY_CHECK = "Consistency Check"
    PROTOCOL_DEVIATION = "Protocol Deviation"
    LOGIC_CHECK = "Logic Check"

class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    CRITICAL = "Critical"
```

---

### 4. User Guide Generator（使用手冊生成器）

**輸入：**
- Protocol 基本資訊
- CRF 表單定義
- Logo 圖片（可選）

**處理：**
1. 建立文件結構
2. 生成試驗概述
3. 為每個表單建立說明
4. 添加螢幕截圖佔位符
5. 格式化文件

**輸出：**
- User Guide Word 文件（.docx）

**文件結構：**
1. 封面
2. 目錄
3. 試驗概述
4. 系統存取說明
5. CRF 填寫指南（按表單）
6. 常見問題
7. 附錄

---

### 5. Word Formatter（文件格式化工具）

**輸入：**
- Word 文件
- Logo 圖片（可選）
- 格式化參數

**處理：**
1. 設定文件樣式
2. 添加頁首頁尾
3. 插入 Logo
4. 格式化表格
5. 調整段落

**輸出：**
- 格式化的 Word 文件

**格式化功能：**
- 標題樣式（Heading 1-4）
- 段落格式（對齊、間距）
- 表格樣式（邊框、底色）
- 頁首頁尾（頁碼、日期）
- Logo 插入

---

## 💾 資料模型

### Protocol Info 資料結構

```json
{
  "study_title": "試驗標題",
  "protocol_number": "Protocol 編號",
  "sponsor": "贊助商",
  "phase": "試驗階段",
  "study_design": "試驗設計",
  "target_population": "目標族群",
  "sample_size": "樣本數",
  "visit_schedule": [
    "篩選訪視",
    "基線訪視",
    "第4週訪視",
    "..."
  ],
  "primary_endpoints": [
    "主要終點1",
    "主要終點2"
  ],
  "secondary_endpoints": [
    "次要終點1",
    "次要終點2"
  ],
  "inclusion_criteria": [
    "納入標準1",
    "納入標準2"
  ],
  "exclusion_criteria": [
    "排除標準1",
    "排除標準2"
  ],
  "crf_domains": [
    "人口統計學",
    "生命徵象",
    "實驗室檢查",
    "..."
  ]
}
```

### CRF Field 資料結構

```python
@dataclass
class CRFField:
    field_name: str          # 欄位名稱
    field_label: str         # 欄位標籤
    form_name: str           # 表單名稱
    data_type: str           # 資料類型
    required: bool = False   # 是否必填
    min_value: float = None  # 最小值
    max_value: float = None  # 最大值
    units: str = None        # 單位
    valid_values: List[str] = None  # 有效值
```

### Validation Rule 資料結構

```python
@dataclass
class ValidationRule:
    rule_id: str                    # 規則ID
    description: str                # 規則描述
    validation_type: ValidationType # 驗證類型
    severity: Severity              # 嚴重程度
    query_text: str                 # 查詢文字
    form_name: str = None           # 表單名稱
    field_name: str = None          # 欄位名稱
    condition: str = None           # 觸發條件
```

---

## 🔐 安全性架構

### 資料流安全

```
使用者 → Colab/Jupyter → Python 程式 → Gemini API
                                              ↓
                                          (加密傳輸)
                                              ↓
                                        Google 伺服器
                                              ↓
                                          處理並返回
                                              ↓
                                       結果儲存於 Session
```

### 安全措施

1. **API Key 保護**
   - 使用環境變數
   - 不寫入程式碼
   - Colab Secrets 加密

2. **資料隔離**
   - Session 內處理
   - 不儲存在雲端
   - Session 結束自動清除

3. **傳輸加密**
   - HTTPS 通訊
   - API 加密傳輸

---

## 📊 效能指標

### 處理能力

| 項目 | 指標 | 說明 |
|------|------|------|
| PDF 大小 | < 50MB | 建議上限 |
| PDF 頁數 | < 200 頁 | 建議上限 |
| CRF 表單數 | < 50 個 | 建議上限 |
| CRF 欄位數 | < 500 個 | 建議上限 |
| 驗證規則數 | < 1000 個 | 建議上限 |

### 處理時間

| 步驟 | Flash 模型 | Pro 模型 |
|------|-----------|---------|
| Protocol 解析 | 30-60秒 | 60-120秒 |
| CRF 生成 | 1-2分鐘 | 2-3分鐘 |
| DVP 生成 | 1-2分鐘 | 1-2分鐘 |
| User Guide 生成 | 1-2分鐘 | 1-2分鐘 |
| **總計** | **3-5分鐘** | **5-8分鐘** |

### 資源使用

| 資源 | 使用量 | 說明 |
|------|--------|------|
| 記憶體 | ~500MB | Runtime 記憶體 |
| 儲存空間 | ~50MB | 含輸出檔案 |
| API 呼叫 | 5-10次 | 完整流程 |
| 網路流量 | ~10MB | 上傳+下載 |

---

## 🔄 版本控制

### 系統版本

- **主版本**: 1.0.0
- **發布日期**: 2025-11-18

### 模組版本

| 模組 | 版本 | 狀態 |
|------|------|------|
| Protocol Parser | 1.0.0 | 穩定 |
| CRF Generator | 1.0.0 | 穩定 |
| DVP Generator | 1.0.0 | 穩定 |
| User Guide Generator | 1.0.0 | 穩定 |
| Word Formatter | 1.0.0 | 穩定 |

### 相容性

- Python: 3.8+
- Google Colab: ✅
- Jupyter Notebook: ✅
- JupyterLab: ✅

---

## 🚀 未來規劃

### 短期（1-3個月）

- [ ] 添加更多 Protocol 範例
- [ ] 優化 AI 提示詞
- [ ] 提升解析準確度
- [ ] 添加錯誤恢復機制

### 中期（3-6個月）

- [ ] 支援更多文件格式（Excel、CSV）
- [ ] 批次處理功能
- [ ] 自訂範本系統
- [ ] 多語言支援

### 長期（6-12個月）

- [ ] Web 介面版本
- [ ] 協作功能
- [ ] 版本控制
- [ ] 雲端儲存整合

---

*最後更新：2025-11-18*
*系統版本：1.0.0*
