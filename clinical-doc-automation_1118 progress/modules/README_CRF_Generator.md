# CRF Generator Module

## 概述

CRF (Case Report Form) Generator 是一個自動化生成臨床試驗病例報告表的Python模組。它支援標準CRF domains，並可擴展自定義domains，輸出為專業格式的Microsoft Word文件。

## 功能特點

### 1. 標準CRF Domains

模組內建以下7個標準臨床試驗domains：

- **Demographics（人口統計學）**: 受試者基本資訊（ID、年齡、性別、種族等）
- **Medical History（病史）**: 受試者醫療病史記錄
- **Vital Signs（生命徵象）**: 體溫、血壓、心率、呼吸率、體重、身高
- **Laboratory Tests（實驗室檢查）**: 實驗室檢測結果
- **Adverse Events（不良事件）**: AE/SAE報告
- **Concomitant Medications（併用藥物）**: 試驗期間使用的其他藥物
- **Study Drug Administration（試驗藥物給藥）**: 試驗藥物給藥記錄

### 2. 自定義Domains

- 支援自定義domain定義
- 靈活的欄位類型（text, numeric, date, checkbox, dropdown）
- 可設定必填/選填欄位
- 支援單位和選項設定

### 3. 專業文件格式

- 使用python-docx生成Word文件
- 專業的表格格式和樣式
- 清晰的欄位定義
- 完整的Coding Instructions（編碼說明）

### 4. 高度可擴展

- 模組化設計
- 易於添加新domains
- 支援domain模板導出
- 可客製化輸出格式

## 安裝依賴

```bash
pip install python-docx
```

## 快速開始

### 基本使用

```python
from modules.crf_generator import CRFGenerator

# 定義試驗資訊
protocol_info = {
    'study_title': 'A Phase III Study of Novel Drug X',
    'protocol_number': 'PROTO-2025-001',
    'sponsor': 'Pharmaceutical Company',
    'version': '1.0'
}

# 創建生成器
generator = CRFGenerator(protocol_info)

# 生成包含所有標準domains的CRF
crf_path = generator.generate_crf(
    output_path='my_study_CRF.docx',
    include_all_standard=True
)
```

### 選擇特定Domains

```python
# 只生成需要的domains
selected_domains = [
    'demographics',
    'vital_signs',
    'adverse_events'
]

crf_path = generator.generate_crf(
    domains=selected_domains,
    output_path='selected_CRF.docx'
)
```

### 添加自定義Domain

```python
from modules.crf_generator import CRFGenerator, CRFDomain

# 定義自定義domain
custom_domain = CRFDomain(
    name='Quality of Life Assessment',
    description='Patient-reported quality of life measures',
    fields=[
        {
            'name': 'assessment_date',
            'label': 'Assessment Date',
            'type': 'date',
            'required': True,
            'coding_instruction': 'Date QoL questionnaire was completed'
        },
        {
            'name': 'physical_score',
            'label': 'Physical Functioning Score',
            'type': 'numeric',
            'required': True,
            'coding_instruction': 'Score range 0-100, higher is better'
        },
        {
            'name': 'pain_level',
            'label': 'Pain Level',
            'type': 'dropdown',
            'required': True,
            'options': ['None', 'Mild', 'Moderate', 'Severe'],
            'coding_instruction': 'Subject-reported pain level'
        }
    ]
)

# 添加到生成器
generator = CRFGenerator(protocol_info)
generator.add_custom_domain(custom_domain)

# 生成包含自定義domain的CRF
crf_path = generator.generate_crf(
    domains=['demographics', 'quality_of_life_assessment'],
    output_path='custom_CRF.docx'
)
```

## 欄位類型說明

### 支援的欄位類型

1. **text**: 文字輸入欄位
2. **numeric**: 數值輸入欄位
3. **date**: 日期輸入欄位
4. **checkbox**: 核取方塊
5. **dropdown**: 下拉選單

### 欄位定義結構

```python
field = {
    'name': 'field_identifier',           # 欄位識別碼（必填）
    'label': 'Field Display Name',        # 顯示名稱（必填）
    'type': 'text',                       # 欄位類型（必填）
    'required': True,                     # 是否必填（必填）
    'unit': 'mg',                         # 單位（選填）
    'options': ['Option1', 'Option2'],    # 選項列表（dropdown/checkbox需要）
    'coding_instruction': 'Instructions'  # 編碼說明（選填但建議提供）
}
```

## 進階功能

### 1. 導出Domain模板

```python
# 導出單個domain作為獨立文件
generator.export_domain_template(
    domain_key='adverse_events',
    output_path='AE_template.docx'
)
```

### 2. 查看可用Domains

```python
# 列出所有可用的domains
available_domains = generator.get_available_domains()
print(f"Available domains: {', '.join(available_domains)}")
```

### 3. 驗證Domain結構

```python
# Domain會自動驗證結構
domain = CRFDomain(name='Test', description='Test domain', fields=[...])
is_valid = domain.validate()  # 返回 True/False
```

## 實際應用範例

### 範例1: 腫瘤學試驗CRF

```python
# 創建腫瘤評估domain
tumor_domain = CRFDomain(
    name='Tumor Assessment',
    description='RECIST 1.1 tumor response evaluation',
    fields=[
        {
            'name': 'assessment_date',
            'label': 'Assessment Date',
            'type': 'date',
            'required': True,
            'coding_instruction': 'Date of imaging assessment'
        },
        {
            'name': 'target_lesion_sum',
            'label': 'Sum of Target Lesions',
            'type': 'numeric',
            'required': True,
            'unit': 'mm',
            'coding_instruction': 'Sum of longest diameters'
        },
        {
            'name': 'overall_response',
            'label': 'Overall Response',
            'type': 'dropdown',
            'required': True,
            'options': ['CR', 'PR', 'SD', 'PD', 'Not Evaluable'],
            'coding_instruction': 'Per RECIST 1.1 criteria'
        }
    ]
)

generator.add_custom_domain(tumor_domain)
```

### 範例2: 心血管試驗CRF

```python
# 創建心電圖domain
ecg_domain = CRFDomain(
    name='Electrocardiogram (ECG)',
    description='12-lead ECG assessment',
    fields=[
        {
            'name': 'ecg_date',
            'label': 'ECG Date',
            'type': 'date',
            'required': True,
            'coding_instruction': 'Date ECG was performed'
        },
        {
            'name': 'qtc_interval',
            'label': 'QTc Interval',
            'type': 'numeric',
            'required': True,
            'unit': 'ms',
            'coding_instruction': 'QTc using Fridericia correction'
        },
        {
            'name': 'rhythm',
            'label': 'Rhythm',
            'type': 'dropdown',
            'required': True,
            'options': ['Sinus Rhythm', 'Atrial Fibrillation', 'Other'],
            'coding_instruction': 'Overall cardiac rhythm'
        }
    ]
)

generator.add_custom_domain(ecg_domain)
```

## 運行範例腳本

模組附帶完整的範例腳本，展示各種使用情境：

```bash
cd clinical-doc-automation/examples
python crf_generator_example.py
```

範例腳本包含：

1. **Example 1**: 基本CRF生成（所有標準domains）
2. **Example 2**: 選擇特定domains
3. **Example 3**: 添加自定義cardiac domains
4. **Example 4**: 完整腫瘤學試驗CRF
5. **Example 5**: 導出domain模板
6. **Example 6**: 列出所有可用domains

## API參考

### CRFGenerator類

#### 初始化
```python
CRFGenerator(protocol_info: Optional[Dict[str, Any]] = None)
```

#### 主要方法

- `generate_crf(domains, output_path, include_all_standard)`: 生成CRF文件
- `add_custom_domain(domain)`: 添加自定義domain
- `get_available_domains()`: 獲取可用domains列表
- `export_domain_template(domain_key, output_path)`: 導出domain模板

### CRFDomain類

#### 初始化
```python
CRFDomain(name: str, description: str, fields: List[Dict[str, Any]])
```

#### 方法

- `validate()`: 驗證domain結構

## 輸出文件結構

生成的CRF Word文件包含：

1. **文件標題**: Case Report Form (CRF)
2. **試驗資訊表**: 包含study title, protocol number, sponsor, version
3. **各Domain章節**:
   - Domain標題和描述
   - 欄位資料表（欄位名稱、類型、必填、值/回應）
   - Coding Instructions章節
4. **專業格式**:
   - 清晰的表格邊框
   - 標題列有背景色
   - 每個domain後有分頁

## 最佳實踐

1. **詳細的Coding Instructions**: 為每個欄位提供清晰的編碼說明
2. **使用標準術語**: 盡可能使用MedDRA、LOINC等標準術語
3. **明確的欄位定義**: 包含單位、正常範圍等資訊
4. **合理的必填設定**: 根據資料收集需求設定required欄位
5. **版本控制**: 在protocol_info中記錄CRF版本號

## 故障排除

### 常見問題

**Q: 生成的文件無法打開**
- 確認已安裝python-docx: `pip install python-docx`
- 檢查輸出路徑的寫入權限

**Q: 自定義domain未出現在CRF中**
- 確認domain結構已通過validate()驗證
- 檢查domain_key是否正確添加到domains列表

**Q: 表格格式異常**
- 確保使用最新版本的python-docx
- 檢查field定義中是否包含所有必需欄位

## 未來擴展

計劃中的功能：

- [ ] eCRF (電子CRF) HTML格式輸出
- [ ] 從EDC系統導入domain定義
- [ ] 自動生成edit checks
- [ ] 支援多語言CRF
- [ ] PDF格式輸出
- [ ] CDISC ODM格式導出

## 技術支援

如有問題或建議，請聯繫開發團隊。

## 版本歷史

- **v1.0 (2025-11-18)**: 初始版本
  - 7個標準CRF domains
  - 自定義domain支援
  - Word文件輸出
  - Coding instructions
  - 範例腳本

## 授權

本模組為臨床文件自動化項目的一部分。
