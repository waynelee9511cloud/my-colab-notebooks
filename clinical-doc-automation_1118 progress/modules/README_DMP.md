# Data Management Plan (DMP) Generator

## 概述

DMP Generator 是一個自動化的 Data Management Plan 生成器模組，專為臨床試驗設計。它能夠基於 Protocol 資訊自動生成完整、符合法規要求的 Data Management Plan 文檔。

## 主要功能

### ✅ 標準 DMP 章節（共 10 章）

1. **Introduction（簡介）** - DMP 目的、法規合規性聲明
2. **Study Overview（試驗概述）** - Protocol 基本資訊表格
3. **Data Management Responsibilities（資料管理職責）** - 各角色職責清單
4. **Data Flow（資料流程）** - 資料收集、傳輸、驗證流程圖
5. **CRF Design（CRF 設計）** - CRF 開發流程、領域列表、設計慣例
6. **Data Validation（資料驗證）** - 驗證策略、檢查規則、查詢管理
7. **Data Quality Control（資料品質控制）** - QC 策略、活動時程、品質指標
8. **Database Lock（資料庫鎖定）** - 鎖定標準、流程步驟、鎖定後變更程序
9. **Data Security（資料安全）** - 存取控制、稽核軌跡、GDPR 合規、備份與災難復原
10. **Archive（資料存檔）** - 存檔要求、保存期限、存檔格式

### ✅ 合規性要求

- **ICH GCP E6(R2)** - Good Clinical Practice 指南
- **FDA 21 CFR Part 11** - Electronic Records; Electronic Signatures
- **FDA 21 CFR Part 50** - Protection of Human Subjects
- **FDA 21 CFR Part 56** - Institutional Review Boards
- **GDPR** - General Data Protection Regulation（適用時）

### ✅ 進階功能

- 📊 **自動生成表格** - 角色職責表、資料流程表、CRF 領域表、驗證規則表、時程表
- 📈 **流程圖** - 資料流程圖以表格形式呈現，清晰易懂
- 🎨 **顏色編碼** - Critical/Major/Minor 嚴重性等級自動著色
- 📝 **自訂章節** - 支援添加研究特定的自訂章節
- 🔧 **Word Formatter 整合** - 與 WordFormatter 整合，確保格式一致性
- 💾 **資料匯出** - 可匯出為 Python 字典格式供其他程序使用

## 安裝

```bash
pip install python-docx
```

如需使用 WordFormatter 進行進階格式設定：
```bash
# WordFormatter 已包含在專案中，無需額外安裝
```

## 快速開始

### 最簡單的方式 - 使用預設值

```python
from modules.dmp_generator import create_dmp_with_defaults

# 僅需 6 個基本參數即可生成完整 DMP
create_dmp_with_defaults(
    protocol_number="PROTO-2025-001",
    protocol_title="我的臨床試驗",
    sponsor="製藥公司名稱",
    indication="適應症",
    phase="Phase III",
    output_path="output/DMP.docx"
)
```

### 基本使用

```python
from modules.dmp_generator import DMPGenerator, ProtocolInfo

# 1. 建立 Protocol 資訊
protocol_info = ProtocolInfo(
    protocol_number="PROTO-2025-001",
    protocol_title="A Phase III Study of Novel Drug",
    sponsor="Global Pharma Inc.",
    indication="Type 2 Diabetes",
    phase="Phase III",
    study_design="Randomized, Double-Blind",
    sample_size="300 subjects",
    study_duration="24 months"
)

# 2. 建立 DMP 生成器
generator = DMPGenerator(protocol_info)

# 3. 生成 DMP 文檔
generator.generate_dmp_document("output/DMP.docx")
```

### 進階使用 - 添加自訂內容

```python
from modules.dmp_generator import (
    DMPGenerator,
    ProtocolInfo,
    CRFDomain,
    Milestone,
    ValidationCheck,
    DataManagementRole,
    DMPSection
)

# 建立生成器
protocol_info = ProtocolInfo(
    protocol_number="PROTO-2025-001",
    protocol_title="Advanced Study Example",
    sponsor="Pharma Company",
    indication="Disease X",
    phase="Phase III"
)

generator = DMPGenerator(protocol_info)

# 設定 EDC 系統
generator.set_edc_system("Medidata Rave EDC v2023.1")

# 添加 CRF 領域
generator.add_crf_domain(CRFDomain(
    domain_name="Demographics",
    description="Subject demographic information",
    visit_schedule=["Screening"],
    is_critical=True,
    validation_rules=8
))

generator.add_crf_domain(CRFDomain(
    domain_name="Vital Signs",
    description="BP, HR, Temperature",
    visit_schedule=["Screening", "Week 4", "Week 8"],
    is_critical=False,
    validation_rules=12
))

# 添加專案里程碑
generator.add_milestone(Milestone(
    name="Database Lock",
    description="Lock clinical database for analysis",
    planned_date="31-Dec-2025",
    responsible="Data Management Lead"
))

# 添加自訂驗證規則
generator.add_validation_check(ValidationCheck(
    check_type="Study-Specific Range Check",
    description="Verify HbA1c between 7.0% and 10.0%",
    severity="Critical",
    implementation="Real-time"
))

# 添加自訂角色
generator.add_dm_role(DataManagementRole(
    role="Medical Coder",
    organization="Coding Services Inc.",
    responsibilities=[
        "Code adverse events using MedDRA",
        "Code medications using WHO Drug"
    ],
    contact_person="Jane Smith",
    contact_email="jane@coding.com"
))

# 添加自訂章節
generator.add_custom_section(DMPSection(
    section_number="11",
    title="Study-Specific Considerations",
    content="This study has unique requirements...",
    subsections=[
        {
            'title': 'CGM Data Management',
            'content': 'Continuous glucose monitoring data will be...'
        }
    ]
))

# 生成文檔
generator.generate_dmp_document("output/DMP_Advanced.docx")
```

## 資料類別說明

### ProtocolInfo
Protocol 基本資訊
```python
ProtocolInfo(
    protocol_number: str,        # Protocol 編號（必填）
    protocol_title: str,         # Protocol 標題（必填）
    sponsor: str,                # 贊助商（必填）
    indication: str,             # 適應症（必填）
    phase: str,                  # 試驗階段（必填）
    study_design: str = "",      # 試驗設計（選填）
    sample_size: str = "",       # 樣本數（選填）
    study_duration: str = "",    # 試驗期間（選填）
    version: str = "1.0",        # 版本（選填，預設 1.0）
    date: str = ""               # 日期（選填，預設今日）
)
```

### CRFDomain
CRF 領域/表單資訊
```python
CRFDomain(
    domain_name: str,            # 領域名稱（如 "Demographics"）
    description: str,            # 描述
    visit_schedule: List[str],   # 訪視時程（如 ["Screening", "Week 4"]）
    is_critical: bool = False,   # 是否為關鍵領域
    validation_rules: int = 0    # 驗證規則數量
)
```

### ValidationCheck
資料驗證檢查
```python
ValidationCheck(
    check_type: str,             # 檢查類型（如 "Range Check"）
    description: str,            # 描述
    severity: str,               # 嚴重性："Critical", "Major", "Minor"
    implementation: str          # 實施方式："Real-time", "Batch", "Manual"
)
```

### Milestone
專案里程碑
```python
Milestone(
    name: str,                   # 里程碑名稱
    description: str,            # 描述
    planned_date: str,           # 計劃日期（如 "31-Dec-2025"）
    responsible: str,            # 負責人
    status: str = "Planned"      # 狀態："Planned", "In Progress", "Completed"
)
```

### DataManagementRole
資料管理角色
```python
DataManagementRole(
    role: str,                   # 角色名稱
    organization: str,           # 組織
    responsibilities: List[str], # 職責清單
    contact_person: str = None,  # 聯絡人（選填）
    contact_email: str = None    # Email（選填）
)
```

### DMPSection
自訂 DMP 章節
```python
DMPSection(
    section_number: str,         # 章節編號（如 "11"）
    title: str,                  # 章節標題
    content: str,                # 章節內容
    subsections: List[Dict] = [] # 子章節清單（選填）
)
```

## 便利函數

### create_dmp()
```python
from modules.dmp_generator import create_dmp

create_dmp(
    protocol_info=protocol_info,      # ProtocolInfo 物件
    output_path="output/DMP.docx",    # 輸出路徑
    crf_domains=[...],                # CRF 領域清單（選填）
    milestones=[...],                 # 里程碑清單（選填）
    edc_system="EDC Name",            # EDC 系統名稱（選填）
    use_word_formatter=True           # 使用 WordFormatter（選填）
)
```

### create_dmp_with_defaults()
```python
from modules.dmp_generator import create_dmp_with_defaults

# 最簡單的方式 - 只需 6 個參數
create_dmp_with_defaults(
    protocol_number="PROTO-2025-001",
    protocol_title="My Study",
    sponsor="My Company",
    indication="Disease",
    phase="Phase III",
    output_path="DMP.docx"
)
```

## 範例程式碼

專案提供了多個完整範例：

```bash
# 執行所有範例
python examples/dmp_generator_example.py all

# 執行特定範例
python examples/dmp_generator_example.py 1    # 基礎範例
python examples/dmp_generator_example.py 2    # 完整範例
python examples/dmp_generator_example.py 3    # 快速建立
python examples/dmp_generator_example.py 4    # 自訂角色
python examples/dmp_generator_example.py 5    # 腫瘤學研究
```

### 範例 1：基礎 DMP
最簡單的 DMP 生成，使用預設設定。

### 範例 2：完整 DMP
包含所有功能的綜合性範例：
- 詳細的 Protocol 資訊
- 12 個 CRF 領域
- 6 個自訂驗證規則
- 11 個專案里程碑
- 2 個自訂章節
- 額外的資料管理角色

### 範例 3：快速建立
使用便利函數快速生成 DMP。

### 範例 4：自訂角色
展示如何定義自訂的資料管理組織架構。

### 範例 5：腫瘤學研究
腫瘤學臨床試驗的專門範例，包含：
- RECIST 1.1 腫瘤評估
- 影像資料管理
- 生物標記資料
- 中央影像審查程序

## 測試

執行完整測試套件：

```bash
# 執行所有測試（正常模式）
python -m modules.test_dmp_generator

# 詳細模式
python -m modules.test_dmp_generator -v

# 簡潔模式
python -m modules.test_dmp_generator -q
```

測試涵蓋範圍：
- ✅ 25 個單元測試
- ✅ 資料類別建立與驗證
- ✅ DMP 生成器核心功能
- ✅ 文檔生成與匯出
- ✅ 便利函數
- ✅ 預設值設定

## 生成的 DMP 文檔結構

生成的 DMP 文檔包含以下完整結構：

### 📄 封面頁
- 文檔標題
- Protocol 資訊
- 版本與日期

### 📑 主要章節（10 章）

**1. Introduction**
- DMP 目的
- 資料品質目標
- 法規合規性聲明（ICH GCP、21 CFR Part 11 等）

**2. Study Overview**
- Protocol 基本資訊表格
- 8 個關鍵資訊欄位

**3. Data Management Responsibilities**
- 預設包含 3 個標準角色
- 每個角色的詳細職責
- 聯絡資訊（如提供）

**4. Data Flow**
- 資料收集與輸入流程
- 10 步驟資料流程圖
- 外部資料傳輸程序

**5. CRF Design**
- CRF 開發流程（7 個步驟）
- CRF 領域表格（如提供）
- CRF 設計慣例（日期格式、單位、編碼等）

**6. Data Validation**
- 驗證策略（多層次驗證）
- 驗證檢查表格（預設 4 個 + 自訂檢查）
- 查詢管理流程

**7. Data Quality Control**
- QC 策略
- QC 活動與頻率表格（7 項活動）
- 品質指標與目標

**8. Database Lock**
- 資料庫鎖定標準（預設 9 項）
- 鎖定流程步驟表格（6 個步驟）
- 鎖定後變更程序

**9. Data Security**
- 存取控制
- 稽核軌跡
- 資料保護與隱私（GDPR）
- 備份與災難復原

**10. Archive**
- 存檔要求清單
- 保存期限表格
- 存檔格式與儲存規格

### 📚 附錄

**Appendix A: Abbreviations and Definitions**
- 15 個常用縮寫詞彙表

**Appendix B: Project Timeline**（如提供里程碑）
- 專案時程表
- 里程碑、描述、計劃日期、負責人

### ➕ 自訂章節（如提供）
- 研究特定考量
- 特殊資料管理程序
- 其他自訂內容

## 預設值

### 預設資料管理角色（3 個）
1. Data Management Lead
2. Clinical Data Manager
3. Data Entry Personnel

### 預設驗證檢查（4 個）
1. Required Field Check（Critical，Real-time）
2. Range Check（Major，Real-time）
3. Date Consistency（Major，Real-time）
4. Cross-form Validation（Major，Batch）

### 預設資料庫鎖定標準（9 項）
1. All CRFs completed
2. All queries resolved
3. Monitoring completed
4. SDV completed
5. Protocol deviations documented
6. QC checks completed
7. Medical coding completed
8. External data reconciled
9. Lock memo approved

## 格式設定

### 使用 WordFormatter（推薦）
```python
generator.generate_dmp_document(
    "output/DMP.docx",
    use_word_formatter=True  # 使用 WordFormatter 進行格式設定
)
```

優點：
- ✅ 專業的頁首頁尾
- ✅ 一致的字體與樣式
- ✅ 標準化的頁面格式
- ✅ 公司品牌元素（如提供 Logo）

### 基本格式
```python
generator.generate_dmp_document(
    "output/DMP.docx",
    use_word_formatter=False  # 使用基本格式
)
```

## 匯出資料

將 DMP 配置匯出為 Python 字典：

```python
config_dict = generator.export_to_dict()

# 包含以下鍵值：
# - protocol_info: Protocol 資訊
# - dm_roles: 資料管理角色清單
# - crf_domains: CRF 領域清單
# - validation_checks: 驗證檢查清單
# - milestones: 里程碑清單
```

## 疑難排解

### 問題：生成的文檔無法開啟
**解決方案：**
- 確認輸出路徑有寫入權限
- 檢查檔案是否被其他程式開啟
- 確認 python-docx 版本正確：`pip install --upgrade python-docx`

### 問題：WordFormatter 無法使用
**解決方案：**
- 確認 WordFormatter 模組存在於 modules 目錄
- 設定 `use_word_formatter=False` 使用基本格式

### 問題：表格格式不正確
**解決方案：**
- 使用 Microsoft Word 或 LibreOffice 開啟（不要使用線上版本）
- 某些樣式可能需要在 Word 中手動調整

## 最佳實踐

1. **Protocol 資訊完整性**
   - 盡可能提供完整的 Protocol 資訊
   - 包含 study_design、sample_size、study_duration 等選填欄位

2. **CRF 領域規劃**
   - 明確標示關鍵（critical）領域
   - 提供驗證規則數量估算
   - 詳細列出訪視時程

3. **里程碑設定**
   - 包含所有重要的專案里程碑
   - 使用一致的日期格式（DD-MMM-YYYY）
   - 明確指定負責人

4. **自訂章節**
   - 用於研究特定的資料管理考量
   - 善用子章節組織內容
   - 保持內容簡潔明瞭

5. **版本控制**
   - 在 Protocol 資訊中維護版本號
   - DMP 更新時遞增版本號
   - 在檔名中包含版本號（如 DMP_v1.0.docx）

## 常見使用情境

### 情境 1：新試驗 DMP 快速生成
```python
# 試驗啟動階段，需要快速生成基礎 DMP
create_dmp_with_defaults(
    protocol_number="PROTO-2025-001",
    protocol_title="Study Title",
    sponsor="Sponsor Name",
    indication="Indication",
    phase="Phase III",
    output_path="DMP_v1.0.docx"
)
```

### 情境 2：完整試驗 DMP（包含所有細節）
```python
# 試驗計劃階段，需要詳細的 DMP
generator = DMPGenerator(protocol_info)

# 添加所有 CRF 領域
for domain in crf_domains:
    generator.add_crf_domain(domain)

# 添加專案時程
for milestone in milestones:
    generator.add_milestone(milestone)

# 添加自訂內容
generator.add_custom_section(custom_section)

generator.generate_dmp_document("DMP_Complete_v1.0.docx")
```

### 情境 3：特殊試驗類型（如腫瘤學）
```python
# 腫瘤學試驗，需要特殊的資料管理程序
generator = DMPGenerator(protocol_info)

# 添加腫瘤學特定的 CRF 領域
generator.add_crf_domain(CRFDomain(
    domain_name="Tumor Assessment (RECIST 1.1)",
    description="...",
    visit_schedule=["Baseline", "Every 8 weeks"],
    is_critical=True
))

# 添加影像資料管理章節
generator.add_custom_section(DMPSection(
    section_number="11",
    title="Central Imaging Review",
    content="..."
))

generator.generate_dmp_document("DMP_Oncology_v1.0.docx")
```

## 支援與貢獻

如有問題或建議，請聯繫 Clinical Document Automation Team。

## 版本歷史

- **v1.0.0** (2025-11-18)
  - 首次發布
  - 10 個標準 DMP 章節
  - 完整的法規合規性
  - WordFormatter 整合
  - 完整的測試套件
  - 5 個詳細範例

## 授權

本模組為 Clinical Document Automation 專案的一部分。

---

**Clinical Document Automation Team**
*Making clinical data management easier, one document at a time.*
