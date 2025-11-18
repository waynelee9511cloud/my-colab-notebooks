# DVP Generator Module

## 概述

DVP (Data Validation Plan) Generator 是一個自動生成臨床試驗資料驗證計畫的 Python 模組。它可以基於試驗書 (Protocol) 資訊和 CRF (Case Report Form) 設計自動生成全面的驗證規則，並輸出為 Word 文件格式。

## 功能特點

### 標準驗證檢查

1. **Range Checks (範圍檢查)**
   - 自動為數值型欄位生成範圍驗證
   - 支援最小值、最大值設定
   - 包含單位資訊

2. **Required Fields (必填欄位)**
   - 檢查必填欄位是否為空
   - Critical 嚴重等級

3. **Logical Checks (邏輯檢查)**
   - 條件式驗證 (例如：若選擇「是」則需填寫詳細資料)
   - 資料一致性檢查

4. **Cross-Form Validations (跨表單驗證)**
   - 檢查不同表單間的資料一致性
   - 例如：受試者 ID 在所有表單中一致

5. **Date Consistency (日期一致性)**
   - 日期邏輯檢查 (例如：結束日期應在開始日期之後)
   - 試驗重要日期順序檢查

6. **Protocol Deviation Checks (違反試驗書檢查)**
   - 收案/排除標準檢查
   - 訪視時間窗檢查
   - 禁用藥物檢查

### 驗證規則結構

每個驗證規則包含：
- **Rule ID**: 唯一識別碼 (例如：RNG-0001, REQ-0002)
- **Description**: 規則描述
- **Severity**: 嚴重等級 (Critical, Major, Minor)
- **Query Text**: 觸發時顯示的查詢文字
- **Validation Type**: 驗證類型
- **Form Name**: 相關表單名稱
- **Field Name**: 相關欄位名稱

## 安裝需求

```bash
pip install python-docx
```

## 快速開始

### 基本使用

```python
from modules.dvp_generator import (
    DVPGenerator,
    ProtocolInfo,
    CRFField,
    Severity
)

# 1. 定義試驗書資訊
protocol_info = ProtocolInfo(
    protocol_number="ABC-2025-001",
    protocol_title="A Phase III Study of Drug X",
    sponsor="ABC Pharmaceuticals",
    indication="Hypertension",
    phase="Phase III",
    version="1.0"
)

# 2. 定義 CRF 欄位
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
        field_name="weight",
        field_label="Weight",
        form_name="Demographics",
        data_type="numeric",
        required=True,
        min_value=40,
        max_value=200,
        units="kg"
    )
]

# 3. 建立生成器並生成規則
generator = DVPGenerator(protocol_info)
generator.add_crf_fields(crf_fields)
generator.generate_all_rules()

# 4. 生成 Word 文件
generator.generate_dvp_document("output/my_dvp.docx")
```

### 使用便利函式

```python
from modules.dvp_generator import create_dvp, ProtocolInfo, CRFField

# 一行完成所有操作
create_dvp(
    protocol_info=protocol_info,
    crf_fields=crf_fields,
    output_path="output/my_dvp.docx"
)
```

### 新增自訂驗證規則

```python
from modules.dvp_generator import Severity, ValidationType

# 新增自訂規則
generator.add_custom_rule(
    description="Verify ECOG Performance Status is 0-2 per protocol",
    query_text="Please verify ECOG status. Protocol requires 0-2.",
    severity=Severity.CRITICAL,
    validation_type=ValidationType.PROTOCOL_DEVIATION,
    form_name="Demographics",
    field_name="ecog_status",
    details={'allowed_values': ['0', '1', '2']}
)
```

## CRF 欄位定義

### 資料類型 (data_type)

- `numeric`: 數值型
- `date`: 日期型
- `text`: 文字型
- `dropdown`: 下拉選單型

### 欄位屬性

```python
CRFField(
    field_name="field_id",        # 欄位 ID (必填)
    field_label="Field Label",    # 欄位標籤 (必填)
    form_name="Form Name",        # 表單名稱 (必填)
    data_type="numeric",          # 資料類型 (必填)
    required=True,                # 是否必填
    min_value=0,                  # 最小值 (數值型)
    max_value=100,                # 最大值 (數值型)
    valid_values=["A", "B"],      # 有效值列表 (下拉選單)
    date_format="YYYY-MM-DD",     # 日期格式 (日期型)
    units="mg/dL"                 # 單位 (數值型)
)
```

## 嚴重等級 (Severity)

- **Critical**: 必須立即解決的問題，可能影響受試者安全或資料完整性
- **Major**: 重大問題，應盡快處理，可能影響資料品質
- **Minor**: 應審查的問題，但不會顯著影響資料品質

## 驗證類型 (ValidationType)

- `RANGE_CHECK`: 範圍檢查
- `REQUIRED_FIELD`: 必填欄位
- `LOGICAL_CHECK`: 邏輯檢查
- `CROSS_FORM`: 跨表單驗證
- `DATE_CONSISTENCY`: 日期一致性
- `PROTOCOL_DEVIATION`: 違反試驗書
- `CUSTOM`: 自訂驗證

## 輸出格式

生成的 DVP Word 文件包含：

1. **封面頁**
   - 試驗書編號、標題
   - 贊助商、適應症、期別
   - DVP 版本和日期

2. **簡介**
   - DVP 目的和範圍
   - 驗證規則概述

3. **驗證規則章節**
   - 依類型分組的驗證規則摘要表
   - 詳細驗證規則表格
   - 包含 Rule ID, Form, Field, Description, Severity, Query Text

4. **附錄**
   - 嚴重等級定義

## 匯出功能

### 匯出為字典/JSON

```python
# 匯出規則為字典格式
rules_dict = generator.export_rules_to_dict()

# 儲存為 JSON
import json
with open('rules.json', 'w') as f:
    json.dump(rules_dict, f, indent=2)
```

### 取得規則摘要

```python
# 取得各類型規則數量
summary = generator.get_rules_summary()
# 輸出: {'Range Check': 5, 'Required Field': 10, ...}
```

## 完整範例

請參考 `examples/dvp_example.py` 中的詳細範例：

1. **Example 1**: 基本使用
2. **Example 2**: 新增自訂規則
3. **Example 3**: 使用便利函式
4. **Example 4**: 匯出規則為 JSON
5. **Example 5**: 綜合實際案例

### 執行範例

```bash
cd clinical-doc-automation/examples
python dvp_example.py
```

執行後會在 `output/` 目錄生成多個範例 DVP 文件。

## 進階使用

### 批次處理多個試驗

```python
protocols = [
    ("STUDY-001", "Oncology Study", "Phase III"),
    ("STUDY-002", "Cardiology Study", "Phase II"),
]

for number, title, phase in protocols:
    protocol_info = ProtocolInfo(
        protocol_number=number,
        protocol_title=title,
        phase=phase,
        sponsor="My Company",
        indication="Various"
    )

    # ... 定義 CRF 欄位 ...

    create_dvp(
        protocol_info=protocol_info,
        crf_fields=crf_fields,
        output_path=f"output/dvp_{number}.docx"
    )
```

### 從資料庫讀取 CRF 定義

```python
import pandas as pd

# 從 Excel 讀取 CRF 定義
crf_df = pd.read_excel("crf_specification.xlsx")

crf_fields = []
for _, row in crf_df.iterrows():
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

# 生成 DVP
create_dvp(protocol_info, crf_fields, "output/dvp.docx")
```

### 整合到 EDC 系統

```python
# 匯出規則供 EDC 系統使用
rules = generator.export_rules_to_dict()

# 轉換為 EDC 系統格式
edc_rules = []
for rule in rules:
    edc_rule = {
        'id': rule['rule_id'],
        'form': rule['form_name'],
        'field': rule['field_name'],
        'check_type': rule['validation_type'],
        'severity': rule['severity'],
        'message': rule['query_text'],
        'parameters': rule['details']
    }
    edc_rules.append(edc_rule)

# 上傳到 EDC 系統...
```

## 最佳實踐

1. **完整定義 CRF 欄位**: 盡可能提供完整的欄位資訊 (範圍、單位、必填等)
2. **使用描述性命名**: 欄位名稱和表單名稱應具描述性
3. **適當的嚴重等級**: 根據影響程度選擇適當的 severity
4. **清晰的查詢文字**: Query text 應清楚說明問題和預期行動
5. **版本控制**: 為每個版本的 DVP 使用不同的版本號
6. **保存 JSON**: 同時匯出 JSON 格式以便追蹤和比對

## 疑難排解

### 常見問題

**Q: 如何安裝 python-docx?**
```bash
pip install python-docx
```

**Q: 生成的文件無法開啟?**
- 確認輸出路徑有寫入權限
- 確認路徑中的目錄都存在

**Q: 如何修改文件樣式?**
- 可以在生成後使用 Word 套用樣式範本
- 或修改 `dvp_generator.py` 中的樣式設定

**Q: 如何新增新的驗證類型?**
- 在 `ValidationType` enum 中新增類型
- 實作對應的生成方法
- 更新 `generate_all_rules()` 方法

## API 參考

### 主要類別

- `DVPGenerator`: 主要生成器類別
- `ProtocolInfo`: 試驗書資訊
- `CRFField`: CRF 欄位定義
- `ValidationRule`: 驗證規則
- `Severity`: 嚴重等級枚舉
- `ValidationType`: 驗證類型枚舉

### 主要方法

- `DVPGenerator.add_crf_fields(fields)`: 新增 CRF 欄位
- `DVPGenerator.generate_all_rules()`: 生成所有標準規則
- `DVPGenerator.add_custom_rule(...)`: 新增自訂規則
- `DVPGenerator.generate_dvp_document(path)`: 生成 Word 文件
- `DVPGenerator.export_rules_to_dict()`: 匯出規則為字典
- `DVPGenerator.get_rules_summary()`: 取得規則摘要
- `create_dvp(...)`: 便利函式

## 授權

This module is part of the Clinical Doc Automation project.

## 聯絡資訊

如有問題或建議，請聯絡開發團隊。
