# Word文件格式化引擎 - 快速入門指南

## 5分鐘快速上手

### 步驟1: 安裝依賴

```bash
pip install python-docx pillow
```

或使用項目的requirements.txt：

```bash
pip install -r requirements.txt
```

### 步驟2: 建立第一個文件

建立一個新的Python檔案 `my_first_document.py`：

```python
from modules.word_formatter import create_clinical_document

# 建立一個標準的臨床試驗Protocol文件
formatter = create_clinical_document(
    document_title="Clinical Study Protocol",
    protocol_number="ABC-2025-001",
    version="1.0",
    sponsor="ABC Pharmaceutical Company",
    indication="Type 2 Diabetes Mellitus",
    output_path="output/my_protocol.docx"
)

# 添加第一章
formatter.apply_title_style("1. INTRODUCTION", level=1)
formatter.apply_body_style(
    "This protocol describes a Phase III clinical trial to evaluate "
    "the efficacy and safety of ABC-001 in patients with Type 2 Diabetes.",
    alignment='justify'
)

# 添加第二章
formatter.apply_title_style("2. STUDY OBJECTIVES", level=1)
formatter.apply_title_style("2.1 Primary Objective", level=2)
formatter.apply_body_style(
    "To demonstrate the superiority of ABC-001 compared to placebo "
    "in reducing HbA1c levels.",
    alignment='justify'
)

# 儲存文件
formatter.save_document("output/my_protocol.docx")

print("文件建立完成！")
```

### 步驟3: 執行程式

```bash
python my_first_document.py
```

恭喜！您已經建立了第一個符合公司規範的臨床試驗文件！

---

## 常見使用場景

### 場景1: 建立Protocol Synopsis

```python
from modules.word_formatter import WordFormatter

formatter = WordFormatter()
formatter.create_document()
formatter.set_page_format()

# 設定頁首頁尾
formatter.set_header(
    document_title="Protocol Synopsis",
    protocol_number="PRO-2025-001",
    version="1.0"
)
formatter.set_footer()

# 建立Synopsis表格
table = formatter.doc.add_table(rows=8, cols=2)
formatter.apply_table_style(table)

# 填入資料
data = [
    ['Protocol Title', 'A Phase III Study of ABC-001'],
    ['Protocol Number', 'PRO-2025-001'],
    ['Study Phase', 'Phase III'],
    ['Indication', 'Type 2 Diabetes Mellitus'],
    ['Study Design', 'Randomized, Double-Blind'],
    ['Sample Size', '300 subjects'],
    ['Treatment Duration', '24 weeks']
]

for i, (key, value) in enumerate(data):
    table.rows[i].cells[0].text = key
    table.rows[i].cells[1].text = value

formatter.save_document("output/synopsis.docx")
```

### 場景2: 建立包含Logo的文件

```python
from modules.word_formatter import create_clinical_document

formatter = create_clinical_document(
    document_title="Clinical Study Report",
    protocol_number="CSR-2025-001",
    version="Final 1.0",
    logo_path="templates/company_logo.png",  # 放置您的Logo
    output_path="output/csr.docx"
)

# 添加執行摘要
formatter.apply_title_style("EXECUTIVE SUMMARY", level=1)
formatter.apply_body_style("This study demonstrated...")

formatter.save_document("output/csr.docx")
```

### 場景3: 自訂公司規範格式

```python
from modules.word_formatter import WordFormatter
from docx.shared import RGBColor, Inches

# 定義公司專屬格式
company_config = {
    'title_font': 'Arial',
    'body_font': 'Arial',
    'title_size': 18,
    'title_color': RGBColor(0, 102, 204),  # 公司品牌藍色
    'margin_left': Inches(1.5),
    'margin_right': Inches(1.0),
    'confidential_text': 'CONFIDENTIAL & PROPRIETARY',
    'company_name': 'Your Company Name'
}

# 使用自訂格式
formatter = WordFormatter(config=company_config)
formatter.create_document()
formatter.apply_clinical_trial_template(
    document_title="Investigator's Brochure",
    protocol_number="IB-2025-001",
    version="2.0"
)

# 繼續添加內容...
```

### 場景4: 批次生成多個文件

```python
from modules.word_formatter import create_clinical_document

# 定義要建立的文件清單
documents = [
    {
        'title': 'Clinical Study Protocol',
        'number': 'PRO-2025-001',
        'type': 'protocol'
    },
    {
        'title': 'Informed Consent Form',
        'number': 'ICF-2025-001',
        'type': 'icf'
    },
    {
        'title': 'Case Report Form',
        'number': 'CRF-2025-001',
        'type': 'crf'
    }
]

# 批次建立
for doc in documents:
    formatter = create_clinical_document(
        document_title=doc['title'],
        protocol_number=doc['number'],
        version="1.0",
        output_path=f"output/{doc['type']}.docx"
    )

    # 根據文件類型添加不同內容
    if doc['type'] == 'protocol':
        formatter.apply_title_style("1. INTRODUCTION", level=1)
        formatter.apply_body_style("Protocol content here...")
    elif doc['type'] == 'icf':
        formatter.apply_title_style("INFORMED CONSENT", level=1)
        formatter.apply_body_style("You are being invited...")
    elif doc['type'] == 'crf':
        formatter.apply_title_style("CASE REPORT FORM", level=1)
        formatter.apply_body_style("Subject information...")

    formatter.save_document(f"output/{doc['type']}.docx")
    print(f"{doc['title']} 建立完成！")
```

---

## 進階技巧

### 技巧1: 建立複雜的訪視時程表

```python
formatter = WordFormatter()
formatter.create_document()
formatter.set_page_format()

formatter.apply_title_style("SCHEDULE OF ASSESSMENTS", level=1)

# 建立表格
table = formatter.doc.add_table(rows=10, cols=8)
formatter.apply_table_style(table)

# 設定表頭
visits = ['Assessment', 'Screening', 'Baseline', 'Week 4', 'Week 8', 'Week 12', 'Week 24', 'Follow-up']
for i, visit in enumerate(visits):
    table.rows[0].cells[i].text = visit

# 填入評估項目
assessments = [
    ['Informed Consent', 'X', '', '', '', '', '', ''],
    ['Demographics', 'X', '', '', '', '', '', ''],
    ['Physical Exam', 'X', 'X', '', 'X', '', 'X', 'X'],
    ['Vital Signs', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['Lab Tests', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['ECG', 'X', 'X', '', '', '', 'X', ''],
    ['HbA1c', 'X', 'X', '', '', '', 'X', ''],
    ['AE Assessment', '', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['Drug Dispensing', '', 'X', 'X', 'X', 'X', '', '']
]

for i, row_data in enumerate(assessments, start=1):
    for j, cell_data in enumerate(row_data):
        table.rows[i].cells[j].text = cell_data

formatter.save_document("output/visit_schedule.docx")
```

### 技巧2: 整合AI生成內容

```python
from modules.word_formatter import WordFormatter
# 假設您有一個AI生成內容的函數
# from my_ai_module import generate_protocol_section

formatter = WordFormatter()
formatter.create_document()
formatter.apply_clinical_trial_template(
    document_title="AI Generated Protocol",
    protocol_number="AI-2025-001",
    version="1.0"
)

# AI生成各章節內容
sections = [
    {'title': '1. INTRODUCTION', 'level': 1},
    {'title': '2. STUDY OBJECTIVES', 'level': 1},
    {'title': '3. STUDY DESIGN', 'level': 1},
]

for section in sections:
    # 添加標題
    formatter.apply_title_style(section['title'], level=section['level'])

    # 使用AI生成內容（這裡用示例文字代替）
    # ai_content = generate_protocol_section(section['title'])
    ai_content = f"AI generated content for {section['title']}..."

    formatter.apply_body_style(ai_content, alignment='justify')

formatter.save_document("output/ai_protocol.docx")
```

---

## 疑難排解

### 問題1: 找不到python-docx模組

**解決方案：**
```bash
pip install --upgrade python-docx
```

### 問題2: 中文字體顯示不正確

**解決方案：**
確保配置中設定了支援中文的字體：
```python
config = {
    'title_font': 'Calibri',  # 或 'Microsoft YaHei', 'SimSun'
    'body_font': 'Calibri'
}
```

### 問題3: Logo無法顯示

**解決方案：**
1. 確認Logo檔案存在
2. 使用PNG或JPG格式
3. 檢查檔案路徑是否正確

```python
import os
logo_path = "templates/logo.png"
if os.path.exists(logo_path):
    formatter.set_header(..., logo_path=logo_path)
else:
    print(f"Logo不存在: {logo_path}")
```

### 問題4: 表格樣式無法套用

**解決方案：**
使用Word內建的表格樣式名稱：
```python
# 常見的表格樣式
table_styles = [
    'Light Grid Accent 1',
    'Light Shading Accent 1',
    'Medium Shading 1 Accent 1',
    'Table Grid'
]

formatter.apply_table_style(table, style_name='Light Grid Accent 1')
```

---

## 最佳實踐

### 1. 使用配置檔案

建立 `config.py`：
```python
from docx.shared import RGBColor, Inches

COMPANY_CONFIG = {
    'title_font': 'Arial',
    'body_font': 'Calibri',
    'title_size': 16,
    'title_color': RGBColor(0, 51, 102),
    'margin_top': Inches(1.0),
    'confidential_text': 'CONFIDENTIAL',
}
```

使用配置：
```python
from config import COMPANY_CONFIG
from modules.word_formatter import WordFormatter

formatter = WordFormatter(config=COMPANY_CONFIG)
```

### 2. 建立範本庫

在 `templates/` 目錄下存放：
- `protocol_template.docx` - Protocol範本
- `icf_template.docx` - ICF範本
- `company_logo.png` - 公司Logo

### 3. 文件版本控制

在文件中包含版本歷史：
```python
formatter.apply_title_style("DOCUMENT HISTORY", level=1)

history_table = formatter.doc.add_table(rows=4, cols=4)
formatter.apply_table_style(history_table)

# 表頭
history_table.rows[0].cells[0].text = 'Version'
history_table.rows[0].cells[1].text = 'Date'
history_table.rows[0].cells[2].text = 'Author'
history_table.rows[0].cells[3].text = 'Changes'

# 版本記錄
history_table.rows[1].cells[0].text = '1.0'
history_table.rows[1].cells[1].text = '2025-01-15'
history_table.rows[1].cells[2].text = 'John Doe'
history_table.rows[1].cells[3].text = 'Initial version'
```

---

## 下一步

1. 查看完整API文檔：`modules/README.md`
2. 執行範例程式：`python examples/word_formatter_example.py --all`
3. 根據公司需求自訂配置
4. 整合到現有的文件生成流程

## 需要協助？

- 查看詳細文檔：`modules/README.md`
- 查看範例代碼：`examples/word_formatter_example.py`
- 聯繫開發團隊

---

**祝您使用愉快！**
