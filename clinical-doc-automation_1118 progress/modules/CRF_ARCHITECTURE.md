# CRF Generator - 架構設計文檔

## 系統架構概述

```
┌─────────────────────────────────────────────────────────────────┐
│                      CRF Generator System                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │   Protocol Info  │         │  Custom Domains  │            │
│  │   (Input Data)   │────────▶│   (Optional)     │            │
│  └──────────────────┘         └──────────────────┘            │
│           │                             │                      │
│           └─────────────┬───────────────┘                      │
│                         ▼                                      │
│              ┌─────────────────────┐                          │
│              │   CRFGenerator      │                          │
│              │   (Main Engine)     │                          │
│              └─────────────────────┘                          │
│                         │                                      │
│          ┌──────────────┼──────────────┐                      │
│          ▼              ▼              ▼                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │ Standard   │  │  Custom    │  │  Document  │             │
│  │  Domains   │  │  Domains   │  │  Builder   │             │
│  │  (Built-in)│  │ (User-def) │  │ (python-   │             │
│  │            │  │            │  │  docx)     │             │
│  └────────────┘  └────────────┘  └────────────┘             │
│          │              │              │                      │
│          └──────────────┼──────────────┘                      │
│                         ▼                                      │
│              ┌─────────────────────┐                          │
│              │  CRF Document       │                          │
│              │  (.docx)            │                          │
│              └─────────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心組件

### 1. CRFGenerator（主引擎）

**職責**:
- 管理CRF生成流程
- 整合標準和自定義domains
- 協調文檔建構

**主要方法**:
```python
- __init__(protocol_info)         # 初始化
- generate_crf(domains, output)   # 生成CRF
- add_custom_domain(domain)       # 添加自定義domain
- get_available_domains()         # 獲取可用domains
- export_domain_template()        # 導出模板
```

### 2. CRFDomain（Domain定義）

**職責**:
- 封裝domain結構
- 驗證欄位定義
- 提供domain元數據

**屬性**:
```python
- name: str                       # Domain名稱
- description: str                # Domain描述
- fields: List[Dict]              # 欄位定義列表
```

**方法**:
```python
- validate() -> bool              # 驗證結構
```

### 3. Standard Domains（標準Domains庫）

內建7個標準臨床試驗domains:

```
Demographics ──────────────► 人口統計學資訊
Medical History ───────────► 病史記錄
Vital Signs ───────────────► 生命徵象測量
Laboratory Tests ──────────► 實驗室檢查
Adverse Events ────────────► 不良事件報告
Concomitant Medications ───► 併用藥物記錄
Study Drug Administration ─► 試驗藥物給藥
```

## 資料流程

```
Step 1: 輸入
┌────────────────────────────────────────┐
│ Protocol Information                   │
│ ─────────────────────────────────────  │
│ • Study Title                          │
│ • Protocol Number                      │
│ • Sponsor                              │
│ • Version                              │
│ • Custom Domains (optional)            │
└────────────────────────────────────────┘
              ▼
Step 2: 初始化
┌────────────────────────────────────────┐
│ CRFGenerator Initialization            │
│ ─────────────────────────────────────  │
│ • Load standard domains                │
│ • Load custom domains                  │
│ • Initialize document builder          │
└────────────────────────────────────────┘
              ▼
Step 3: 選擇Domains
┌────────────────────────────────────────┐
│ Domain Selection                       │
│ ─────────────────────────────────────  │
│ • User specifies domains               │
│ • Or use all standard domains          │
│ • Validate domain availability         │
└────────────────────────────────────────┘
              ▼
Step 4: 建構文檔
┌────────────────────────────────────────┐
│ Document Construction                  │
│ ─────────────────────────────────────  │
│ 1. Add header (title, protocol info)  │
│ 2. For each domain:                    │
│    • Add domain heading                │
│    • Create field table                │
│    • Add coding instructions           │
│    • Add page break                    │
└────────────────────────────────────────┘
              ▼
Step 5: 輸出
┌────────────────────────────────────────┐
│ .docx File Output                      │
│ ─────────────────────────────────────  │
│ • Professional formatting              │
│ • Tables with borders                  │
│ • Colored headers                      │
│ • Complete coding instructions         │
└────────────────────────────────────────┘
```

## Domain結構

### Domain定義架構

```python
{
    'name': 'Domain Name',
    'description': 'Domain description',
    'fields': [
        {
            'name': 'field_identifier',      # 欄位ID
            'label': 'Display Label',        # 顯示標籤
            'type': 'field_type',            # 欄位類型
            'required': True/False,          # 是否必填
            'unit': 'measurement_unit',      # 單位（可選）
            'options': [...],                # 選項（dropdown/checkbox）
            'coding_instruction': '...'      # 編碼說明
        },
        ...
    ]
}
```

### 支援的欄位類型

```
┌──────────┬──────────────────────────────────────┐
│ Type     │ Description                          │
├──────────┼──────────────────────────────────────┤
│ text     │ 自由文字輸入                          │
│ numeric  │ 數值輸入（可含單位）                  │
│ date     │ 日期輸入                              │
│ checkbox │ 核取方塊（需options）                 │
│ dropdown │ 下拉選單（需options）                 │
└──────────┴──────────────────────────────────────┘
```

## 文檔格式結構

### 生成的CRF文檔結構

```
┌─────────────────────────────────────────┐
│  Case Report Form (CRF)                 │  ← 文檔標題
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Protocol Information Table        │ │  ← 試驗資訊表
│  │ • Study Title                     │ │
│  │ • Protocol Number                 │ │
│  │ • Sponsor                         │ │
│  │ • CRF Version                     │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ══════════════════════════════════════ │
│  Demographics                           │  ← Domain 1
│  ──────────────────────────────────────│
│  Subject demographic information        │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │ Field Name │Type│Reqd│Value/Response││  ← 欄位表格
│  ├────────────┼────┼────┼──────────────┤│
│  │Subject ID  │Text│Yes │              ││
│  │Age         │Num │Yes │              ││
│  │...         │... │... │              ││
│  └─────────────────────────────────────┘│
│                                         │
│  Coding Instructions:                   │  ← 編碼說明
│  • Subject ID: Unique identifier...    │
│  • Age: Age at informed consent...     │
│                                         │
│  ═══════════════ PAGE BREAK ═══════════ │
│                                         │
│  Vital Signs                            │  ← Domain 2
│  ...                                    │
│                                         │
│  [Additional domains...]                │
│                                         │
└─────────────────────────────────────────┘
```

## 樣式設計

### 表格樣式

```
Header Row:
├─ Background: Blue (#4472C4)
├─ Text: White, Bold
├─ Alignment: Center
└─ Border: All sides, 4pt

Data Rows:
├─ Background: White
├─ Text: Black
├─ Border: All sides, 4pt
└─ Cell padding: Standard

Label Cells (Protocol Info):
├─ Background: Light Gray (#D3D3D3)
├─ Text: Black, Bold
└─ Alignment: Left
```

### 標題樣式

```
Document Title (Level 0):
├─ Font: Calibri, 24pt
├─ Bold: Yes
└─ Alignment: Center

Domain Heading (Level 1):
├─ Font: Calibri, 18pt
├─ Bold: Yes
├─ Color: Dark Blue (#003366)
└─ Alignment: Left

Coding Instructions (Level 2):
├─ Font: Calibri, 14pt
├─ Bold: Yes
├─ Color: Gray (#666666)
└─ Alignment: Left
```

## 擴展性設計

### 添加新的標準Domain

```python
# 在 CRFGenerator.STANDARD_DOMAINS 中添加
'new_domain_key': {
    'name': 'New Domain Name',
    'description': 'Domain description',
    'fields': [
        # 欄位定義...
    ]
}
```

### 自定義欄位類型

```python
# 未來可擴展支援的欄位類型:
- 'multi_select'    # 多選核取方塊
- 'time'            # 時間輸入
- 'datetime'        # 日期時間
- 'file_upload'     # 文件上傳
- 'signature'       # 電子簽名
- 'calculated'      # 計算欄位
```

### 輸出格式擴展

```python
# 未來支援的輸出格式:
- PDF               # PDF文檔
- HTML              # 網頁格式（eCRF）
- ODM               # CDISC ODM XML
- Excel             # Excel工作簿
- JSON              # 結構化數據
```

## 整合能力

### 與其他模組整合

```
Protocol Parser ──────► CRF Generator
    │                        │
    │                        ▼
    └──► Extract Info ──► Auto-generate CRF
         • Title
         • Endpoints
         • Visit Schedule
         • Assessments
```

### EDC系統整合（未來）

```
CRF Generator ──────► ODM Export ──────► EDC Import
                          │
                          ├─► Medidata Rave
                          ├─► Oracle InForm
                          ├─► OpenClinica
                          └─► REDCap
```

## 性能考量

### 處理時間（估計）

```
┌────────────────────────────┬──────────────┐
│ Operation                  │ Time         │
├────────────────────────────┼──────────────┤
│ Initialize Generator       │ < 0.1s       │
│ Add Custom Domain          │ < 0.01s      │
│ Generate CRF (3 domains)   │ < 1s         │
│ Generate CRF (7 domains)   │ < 2s         │
│ Export Domain Template     │ < 0.5s       │
└────────────────────────────┴──────────────┘
```

### 文件大小（估計）

```
┌────────────────────────────┬──────────────┐
│ Content                    │ Size         │
├────────────────────────────┼──────────────┤
│ Empty Document             │ ~15 KB       │
│ + 1 Domain (5 fields)      │ ~20 KB       │
│ + Full CRF (7 domains)     │ ~40 KB       │
│ + Complex CRF (15 domains) │ ~70 KB       │
└────────────────────────────┴──────────────┘
```

## 安全性考量

### 資料驗證

```python
1. Domain Validation
   ├─ Required fields check
   ├─ Field type validation
   └─ Options list validation

2. Input Sanitization
   ├─ Protocol info validation
   ├─ Path traversal prevention
   └─ File extension validation

3. Output Security
   ├─ Safe file naming
   ├─ Directory creation checks
   └─ Permission validation
```

### 最佳實踐

```
✓ Always validate domains before use
✓ Use absolute paths for output
✓ Check write permissions
✓ Sanitize user input
✓ Handle exceptions gracefully
✓ Log generation activities
```

## 錯誤處理

### 錯誤層級

```
Level 1: Validation Errors
├─ Invalid domain structure
├─ Missing required fields
└─ Invalid field types

Level 2: Runtime Errors
├─ File I/O errors
├─ Permission denied
└─ Disk space issues

Level 3: Logic Errors
├─ Domain not found
├─ Duplicate domains
└─ Invalid configuration
```

### 錯誤恢復策略

```python
try:
    generator.generate_crf(...)
except ValidationError:
    # Fix domain definition
    # Retry generation
except IOError:
    # Check permissions
    # Try alternative path
except Exception as e:
    # Log error
    # Notify user
    # Graceful degradation
```

## 測試策略

### 測試覆蓋

```
Unit Tests:
├─ CRFGenerator initialization ✓
├─ Domain validation ✓
├─ Custom domain addition ✓
├─ Field type handling ✓
└─ Document generation ✓

Integration Tests:
├─ Multi-domain CRF ✓
├─ Template export ✓
├─ Protocol info integration ✓
└─ File I/O operations ✓

End-to-End Tests:
├─ Complete CRF workflow ✓
├─ Custom domain workflow ✓
└─ Template export workflow ✓
```

## 版本演進

### v1.0 (Current)
- ✓ 7個標準domains
- ✓ 自定義domain支援
- ✓ Word文檔輸出
- ✓ Coding instructions
- ✓ 模板導出

### v1.1 (Planned)
- □ eCRF HTML輸出
- □ 多語言支援
- □ PDF輸出
- □ 改進的樣式

### v2.0 (Future)
- □ CDISC ODM支援
- □ EDC整合
- □ Edit checks生成
- □ 資料驗證規則

## 貢獻指南

### 添加新功能

1. **添加新的標準Domain**:
   - 在`STANDARD_DOMAINS`中定義
   - 遵循現有結構
   - 添加完整的coding instructions
   - 更新文檔

2. **添加新的欄位類型**:
   - 在`_add_domain_section`中處理渲染
   - 更新驗證邏輯
   - 添加範例
   - 更新文檔

3. **改進文檔格式**:
   - 修改`_add_header`或`_add_domain_section`
   - 保持一致性
   - 測試各種scenarios
   - 更新樣式指南

## 總結

CRF Generator是一個強大、靈活、易於擴展的臨床試驗文檔自動化工具。其模組化設計允許輕鬆添加新功能和整合其他系統，為臨床研究文檔管理提供了完整的解決方案。
