# DVP Generator 快速入門指南

## 簡介

DVP (Data Validation Plan) Generator 是一個自動生成臨床試驗資料驗證計畫的工具，可以基於試驗書和 CRF 設計自動生成全面的驗證規則並輸出為 Word 文件。

## 安裝

```bash
pip install python-docx
```

## 快速開始

### 方法 1: 使用便利函式（推薦）

```python
from clinical-doc-automation.modules.dvp_generator import (
    create_dvp,
    ProtocolInfo,
    CRFField
)

# 定義試驗書資訊
protocol_info = ProtocolInfo(
    protocol_number="STUDY-2025-001",
    protocol_title="A Phase III Study of Drug X",
    sponsor="Pharma Company",
    indication="Hypertension",
    phase="Phase III"
)

# 定義 CRF 欄位
crf_fields = [
    CRFField(
        field_name="age",
        field_label="Age",
        form_name="Demographics",
        data_type="numeric",
        required=True,
        min_value=18,
        max_value=85,
        units="years"
    ),
    CRFField(
        field_name="systolic_bp",
        field_label="Systolic Blood Pressure",
        form_name="Vital Signs",
        data_type="numeric",
        required=True,
        min_value=90,
        max_value=200,
        units="mmHg"
    )
]

# 一行生成 DVP
create_dvp(
    protocol_info=protocol_info,
    crf_fields=crf_fields,
    output_path="output/my_dvp.docx"
)
```

### 方法 2: 使用 DVPGenerator 類別（進階）

```python
from clinical-doc-automation.modules.dvp_generator import (
    DVPGenerator,
    ProtocolInfo,
    CRFField,
    Severity,
    ValidationType
)

# 1. 建立生成器
generator = DVPGenerator(protocol_info)

# 2. 新增 CRF 欄位
generator.add_crf_fields(crf_fields)

# 3. 生成標準驗證規則
generator.generate_all_rules()

# 4. 新增自訂規則（選用）
generator.add_custom_rule(
    description="Verify BP meets inclusion criteria",
    query_text="Please verify BP ≥140/90 mmHg.",
    severity=Severity.CRITICAL,
    validation_type=ValidationType.PROTOCOL_DEVIATION,
    form_name="Vital Signs"
)

# 5. 生成文件
generator.generate_dvp_document("output/my_dvp.docx")

# 6. 匯出 JSON（選用）
rules = generator.export_rules_to_dict()
```

## 核心功能

### 自動生成的驗證類型

1. **Required Field**: 必填欄位檢查
2. **Range Check**: 數值範圍檢查
3. **Date Consistency**: 日期邏輯一致性
4. **Logical Check**: 條件式邏輯檢查
5. **Cross-Form Validation**: 跨表單驗證
6. **Protocol Deviation**: 違反試驗書檢查

### CRF 欄位定義

```python
CRFField(
    field_name="field_id",        # 欄位 ID
    field_label="Field Label",    # 欄位標籤
    form_name="Form Name",        # 表單名稱
    data_type="numeric",          # 類型: numeric, date, text, dropdown
    required=True,                # 是否必填
    min_value=0,                  # 最小值（數值型）
    max_value=100,                # 最大值（數值型）
    valid_values=["A", "B"],      # 有效值（下拉選單）
    units="mg/dL"                 # 單位
)
```

### 嚴重等級

- **Critical**: 必須立即解決，影響受試者安全或資料完整性
- **Major**: 重大問題，影響資料品質
- **Minor**: 需審查但不顯著影響品質

## 輸出內容

生成的 Word 文件包含：

1. 封面頁（試驗書資訊）
2. 簡介（DVP 目的和範圍）
3. 驗證規則摘要表
4. 詳細驗證規則（依類型分組）
5. 附錄（嚴重等級定義）

每個驗證規則包含：
- Rule ID（唯一識別碼）
- Form（表單名稱）
- Field（欄位名稱）
- Description（規則描述）
- Severity（嚴重等級）
- Query Text（查詢文字）

## 範例

完整範例請參考：
- `/examples/quick_demo.py` - 快速示範
- `/examples/dvp_example.py` - 完整範例（5個實際案例）
- `/examples/test_dvp_generator.py` - 單元測試

執行快速示範：
```bash
cd clinical-doc-automation/examples
python quick_demo.py
```

## 常用情境

### 情境 1: 從 Excel 讀取 CRF 定義

```python
import pandas as pd

# 從 Excel 讀取
df = pd.read_excel("crf_spec.xlsx")

crf_fields = []
for _, row in df.iterrows():
    field = CRFField(
        field_name=row['field_name'],
        field_label=row['field_label'],
        form_name=row['form_name'],
        data_type=row['data_type'],
        required=row['required'],
        min_value=row.get('min_value'),
        max_value=row.get('max_value')
    )
    crf_fields.append(field)

create_dvp(protocol_info, crf_fields, "output/dvp.docx")
```

### 情境 2: 批次處理多個試驗

```python
studies = [
    ("STUDY-001", "Oncology Study", "Phase III"),
    ("STUDY-002", "Cardiology Study", "Phase II")
]

for number, title, phase in studies:
    protocol = ProtocolInfo(
        protocol_number=number,
        protocol_title=title,
        phase=phase,
        sponsor="My Company",
        indication="Various"
    )
    create_dvp(protocol, crf_fields, f"output/dvp_{number}.docx")
```

### 情境 3: 匯出為 JSON 供 EDC 使用

```python
generator = DVPGenerator(protocol_info)
generator.add_crf_fields(crf_fields)
generator.generate_all_rules()

# 匯出 JSON
rules = generator.export_rules_to_dict()

import json
with open('edc_rules.json', 'w') as f:
    json.dump(rules, f, indent=2)
```

## 進階功能

### 取得規則摘要

```python
summary = generator.get_rules_summary()
# {'Range Check': 5, 'Required Field': 10, ...}
```

### 自訂驗證規則

```python
generator.add_custom_rule(
    description="Check ECOG status is 0-2",
    query_text="Please verify ECOG status (0-2 required).",
    severity=Severity.CRITICAL,
    validation_type=ValidationType.PROTOCOL_DEVIATION,
    form_name="Demographics",
    field_name="ecog_status",
    details={'allowed_values': ['0', '1', '2']}
)
```

## 檔案結構

```
clinical-doc-automation/
├── modules/
│   ├── dvp_generator.py          # 主模組
│   └── README_DVP.md             # 詳細文件
├── examples/
│   ├── quick_demo.py             # 快速示範
│   ├── dvp_example.py            # 完整範例
│   └── test_dvp_generator.py    # 測試
└── output/
    ├── demo_dvp.docx             # 生成的 DVP 文件
    └── demo_dvp_rules.json       # 匯出的規則
```

## 疑難排解

**Q: 找不到 docx 模組？**
```bash
pip install python-docx
```

**Q: 如何修改文件樣式？**
修改 `dvp_generator.py` 中的 `_add_*` 方法，或在生成後套用 Word 樣式範本。

**Q: 支援哪些資料類型？**
numeric（數值）、date（日期）、text（文字）、dropdown（下拉選單）

## 詳細文件

完整 API 參考和進階用法，請參閱：
- `/modules/README_DVP.md` - 完整文件

## 授權

Clinical Doc Automation Project

---

**提示**: 首次使用建議先運行 `quick_demo.py` 查看生成結果。
