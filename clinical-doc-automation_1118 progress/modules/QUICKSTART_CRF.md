# CRF Generator - 快速入門指南

## 5分鐘快速開始

### 1. 安裝依賴

```bash
pip install python-docx
```

### 2. 基本使用 - 3行代碼生成CRF

```python
from modules.crf_generator import CRFGenerator

protocol_info = {
    'study_title': '您的試驗標題',
    'protocol_number': 'PROTO-001',
    'sponsor': '贊助商名稱',
    'version': '1.0'
}

generator = CRFGenerator(protocol_info)
crf_file = generator.generate_crf(output_path='my_CRF.docx')
```

就這麼簡單！您的CRF文件已經生成了。

---

## 常用範例

### 範例 1: 生成包含所有標準domains的完整CRF

```python
from modules.crf_generator import CRFGenerator

protocol_info = {
    'study_title': 'Phase III Study of Novel Drug',
    'protocol_number': 'STUDY-2025-001',
    'sponsor': 'Pharma Company',
    'version': '1.0'
}

generator = CRFGenerator(protocol_info)

# 生成包含所有7個標準domains的CRF
crf_file = generator.generate_crf(
    output_path='complete_CRF.docx',
    include_all_standard=True
)

print(f"CRF已生成: {crf_file}")
```

**輸出**: 包含以下domains的完整CRF文件
- Demographics
- Medical History
- Vital Signs
- Laboratory Tests
- Adverse Events
- Concomitant Medications
- Study Drug Administration

---

### 範例 2: 只生成需要的特定domains

```python
from modules.crf_generator import CRFGenerator

protocol_info = {
    'study_title': 'Safety Study in Healthy Volunteers',
    'protocol_number': 'SAFETY-001',
    'sponsor': 'Research Institute',
    'version': '1.0'
}

generator = CRFGenerator(protocol_info)

# 只選擇需要的domains
selected_domains = [
    'demographics',
    'vital_signs',
    'adverse_events',
    'study_drug_administration'
]

crf_file = generator.generate_crf(
    domains=selected_domains,
    output_path='safety_study_CRF.docx'
)
```

---

### 範例 3: 添加自定義domain

```python
from modules.crf_generator import CRFGenerator, CRFDomain

# 定義自定義domain
pain_assessment = CRFDomain(
    name='Pain Assessment',
    description='Visual Analog Scale pain assessment',
    fields=[
        {
            'name': 'assessment_date',
            'label': 'Assessment Date',
            'type': 'date',
            'required': True,
            'coding_instruction': 'Date of pain assessment'
        },
        {
            'name': 'vas_score',
            'label': 'VAS Pain Score',
            'type': 'numeric',
            'required': True,
            'unit': '0-100',
            'coding_instruction': 'Visual Analog Scale score (0=no pain, 100=worst pain)'
        },
        {
            'name': 'pain_location',
            'label': 'Pain Location',
            'type': 'dropdown',
            'required': True,
            'options': ['Head', 'Chest', 'Abdomen', 'Back', 'Limbs', 'Other'],
            'coding_instruction': 'Primary location of pain'
        },
        {
            'name': 'pain_interference',
            'label': 'Interference with Daily Activities',
            'type': 'dropdown',
            'required': True,
            'options': ['Not at all', 'A little bit', 'Moderately', 'Quite a bit', 'Extremely'],
            'coding_instruction': 'How much pain interferes with daily activities'
        }
    ]
)

# 創建生成器並添加自定義domain
protocol_info = {
    'study_title': 'Pain Management Study',
    'protocol_number': 'PAIN-2025-001',
    'sponsor': 'Pain Research Center',
    'version': '1.0'
}

generator = CRFGenerator(protocol_info)
generator.add_custom_domain(pain_assessment)

# 生成CRF
crf_file = generator.generate_crf(
    domains=['demographics', 'pain_assessment', 'adverse_events'],
    output_path='pain_study_CRF.docx'
)
```

---

### 範例 4: 腫瘤學研究CRF（含RECIST評估）

```python
from modules.crf_generator import CRFGenerator, CRFDomain

# 定義腫瘤評估domain
tumor_assessment = CRFDomain(
    name='Tumor Assessment (RECIST 1.1)',
    description='Tumor response evaluation using RECIST 1.1 criteria',
    fields=[
        {
            'name': 'assessment_date',
            'label': 'Assessment Date',
            'type': 'date',
            'required': True,
            'coding_instruction': 'Date of radiological assessment'
        },
        {
            'name': 'imaging_type',
            'label': 'Imaging Modality',
            'type': 'dropdown',
            'required': True,
            'options': ['CT Scan', 'MRI', 'PET-CT'],
            'coding_instruction': 'Type of imaging used'
        },
        {
            'name': 'target_lesions_sum',
            'label': 'Sum of Target Lesion Diameters',
            'type': 'numeric',
            'required': True,
            'unit': 'mm',
            'coding_instruction': 'Sum of longest diameters of all target lesions'
        },
        {
            'name': 'new_lesions',
            'label': 'New Lesions Present',
            'type': 'dropdown',
            'required': True,
            'options': ['Yes', 'No'],
            'coding_instruction': 'Are there any new lesions?'
        },
        {
            'name': 'overall_response',
            'label': 'Overall Response',
            'type': 'dropdown',
            'required': True,
            'options': ['CR - Complete Response', 'PR - Partial Response', 'SD - Stable Disease', 'PD - Progressive Disease', 'Not Evaluable'],
            'coding_instruction': 'Overall response per RECIST 1.1'
        }
    ]
)

protocol_info = {
    'study_title': 'Phase II Study in Advanced NSCLC',
    'protocol_number': 'ONCO-2025-456',
    'sponsor': 'Oncology Research Group',
    'version': '2.0'
}

generator = CRFGenerator(protocol_info)
generator.add_custom_domain(tumor_assessment)

crf_file = generator.generate_crf(
    domains=['demographics', 'medical_history', 'tumor_assessment_(recist_1.1)',
             'adverse_events', 'study_drug_administration'],
    output_path='oncology_CRF.docx'
)
```

---

### 範例 5: 導出單個domain作為模板

```python
from modules.crf_generator import CRFGenerator

generator = CRFGenerator()

# 導出不良事件模板
generator.export_domain_template(
    domain_key='adverse_events',
    output_path='AE_template.docx'
)

# 導出生命徵象模板
generator.export_domain_template(
    domain_key='vital_signs',
    output_path='VS_template.docx'
)
```

---

## 欄位類型參考

### 支援的5種欄位類型

#### 1. Text（文字）
```python
{
    'name': 'field_name',
    'label': 'Field Label',
    'type': 'text',
    'required': True,
    'coding_instruction': '說明文字'
}
```

#### 2. Numeric（數值）
```python
{
    'name': 'field_name',
    'label': 'Field Label',
    'type': 'numeric',
    'required': True,
    'unit': 'mg',  # 可選：單位
    'coding_instruction': '說明文字'
}
```

#### 3. Date（日期）
```python
{
    'name': 'field_name',
    'label': 'Field Label',
    'type': 'date',
    'required': True,
    'coding_instruction': 'Format: DD-MMM-YYYY'
}
```

#### 4. Checkbox（核取方塊）
```python
{
    'name': 'field_name',
    'label': 'Field Label',
    'type': 'checkbox',
    'required': True,
    'options': ['Yes', 'No'],
    'coding_instruction': '說明文字'
}
```

#### 5. Dropdown（下拉選單）
```python
{
    'name': 'field_name',
    'label': 'Field Label',
    'type': 'dropdown',
    'required': True,
    'options': ['Option 1', 'Option 2', 'Option 3'],
    'coding_instruction': '說明文字'
}
```

---

## 常用命令參考

### 查看可用的domains
```python
generator = CRFGenerator()
domains = generator.get_available_domains()
print(f"Available domains: {', '.join(domains)}")
```

### 生成所有標準domains
```python
generator.generate_crf(include_all_standard=True)
```

### 生成特定domains
```python
generator.generate_crf(domains=['demographics', 'vital_signs'])
```

### 添加自定義domain
```python
custom_domain = CRFDomain(name='...', description='...', fields=[...])
generator.add_custom_domain(custom_domain)
```

### 驗證domain
```python
is_valid = domain.validate()
```

---

## 實用提示

### 1. Coding Instructions最佳實踐
- 明確說明資料格式要求
- 包含單位和正常範圍
- 參考標準術語（MedDRA, LOINC等）
- 提供填寫範例

### 2. 欄位設計建議
- 使用清晰描述性的label
- 適當設定required欄位
- dropdown選項要完整且互斥
- numeric欄位要包含unit

### 3. 文件組織
- 相關欄位組織在同一domain
- domain順序符合工作流程
- 考慮資料收集的時間點

### 4. 版本控制
- 在protocol_info中記錄版本號
- 輸出檔名包含日期或版本
- 保留歷史版本供參考

---

## 故障排除

### 問題：ModuleNotFoundError: No module named 'docx'
**解決**:
```bash
pip install python-docx
```

### 問題：生成的文件無法打開
**解決**:
- 檢查輸出路徑的寫入權限
- 確認python-docx版本 >= 0.8.11
- 檢查磁碟空間

### 問題：自定義domain未出現
**解決**:
- 確認domain.validate()返回True
- 檢查domain名稱轉換（空格變底線，小寫）
- 確認domain已添加到domains列表

### 問題：表格格式異常
**解決**:
- 更新python-docx到最新版本
- 檢查欄位定義中的必需keys
- 確認options格式正確（list of strings）

---

## 進階技巧

### 1. 從配置文件載入domains
```python
import json

with open('domains_config.json', 'r') as f:
    config = json.load(f)

for domain_def in config['domains']:
    domain = CRFDomain(**domain_def)
    generator.add_custom_domain(domain)
```

### 2. 批量生成多個CRF
```python
studies = [
    {'protocol_number': 'STUDY-001', 'domains': ['demographics', 'vital_signs']},
    {'protocol_number': 'STUDY-002', 'domains': ['demographics', 'adverse_events']},
]

for study in studies:
    protocol_info = {
        'study_title': f"Study {study['protocol_number']}",
        'protocol_number': study['protocol_number'],
        'sponsor': 'Company',
        'version': '1.0'
    }

    generator = CRFGenerator(protocol_info)
    output_file = f"CRF_{study['protocol_number']}.docx"
    generator.generate_crf(domains=study['domains'], output_path=output_file)
```

### 3. 自動從Protocol提取資訊生成CRF
```python
# 這是一個概念性範例，需要配合Protocol Parser使用
from modules.protocol_parser import ProtocolParser  # 假設有這個模組

# 解析protocol
parser = ProtocolParser('protocol.pdf')
protocol_data = parser.extract_information()

# 使用提取的資訊生成CRF
protocol_info = {
    'study_title': protocol_data['title'],
    'protocol_number': protocol_data['protocol_number'],
    'sponsor': protocol_data['sponsor'],
    'version': '1.0'
}

generator = CRFGenerator(protocol_info)
# ... 添加相應的domains
```

---

## 更多資源

- **完整文檔**: 查看 `README_CRF_Generator.md`
- **範例腳本**: 查看 `examples/crf_generator_example.py`
- **測試腳本**: 查看 `modules/test_crf_generator.py`
- **源代碼**: 查看 `modules/crf_generator.py`

---

## 支援

如有問題或建議，請聯繫開發團隊。

**Happy CRF Generating!** 🎉
