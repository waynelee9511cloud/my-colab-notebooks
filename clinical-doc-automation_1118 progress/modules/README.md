# Word文件格式化引擎 (WordFormatter)

用於確保生成的臨床試驗文件符合公司規範的專業格式化引擎。

## 功能特點

### 1. 頁面格式設定
- 支援A4和Letter等標準頁面大小
- 自訂邊距設定
- 橫向/直向頁面方向
- 頁首頁尾距離設定

### 2. 字體樣式管理
- **標題字體**: Calibri/Arial，可自訂大小和顏色
- **內文字體**: 預設Calibri 11pt
- **表格字體**: 統一的表格格式
- 支援中英文字體設定
- 多層級標題樣式（Heading 1-3）

### 3. 頁首設定
- 公司Logo位置（可選）
- 文件標題
- Protocol編號
- 版本資訊
- 自動日期顯示

### 4. 頁尾設定
- 自動頁碼（Page X of Y格式）
- CONFIDENTIAL機密聲明
- 文件日期
- 自訂文字

### 5. 進階功能
- 從範本文件讀取樣式
- 套用臨床試驗文件標準範本
- 自動生成封面頁
- 複雜表格格式化
- 完整的配置系統

## 安裝

```bash
pip install python-docx pillow
```

## 快速開始

### 範例1: 基本使用

```python
from modules.word_formatter import WordFormatter

# 建立格式化引擎
formatter = WordFormatter()

# 建立新文件
formatter.create_document()

# 設定頁面格式
formatter.set_page_format(page_size='A4', orientation='portrait')

# 設定頁首
formatter.set_header(
    document_title="Clinical Study Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 設定頁尾
formatter.set_footer(
    confidential=True,
    include_page_numbers=True
)

# 添加內容
formatter.apply_title_style("1. Introduction", level=2)
formatter.apply_body_style("This is the protocol introduction...")

# 儲存文件
formatter.save_document("output/protocol.docx")
```

### 範例2: 使用便利函數快速建立文件

```python
from modules.word_formatter import create_clinical_document

# 一行代碼建立標準臨床試驗文件
formatter = create_clinical_document(
    document_title="Clinical Study Protocol",
    protocol_number="ABC-2025-001",
    version="2.0",
    sponsor="ABC Pharmaceutical Company",
    indication="Type 2 Diabetes Mellitus",
    output_path="output/protocol.docx"
)

# 繼續添加內容
formatter.apply_title_style("1. STUDY OBJECTIVES", level=1)
formatter.apply_body_style("The primary objective is...")

# 儲存
formatter.save_document("output/protocol.docx")
```

### 範例3: 自訂配置

```python
from modules.word_formatter import WordFormatter
from docx.shared import RGBColor, Inches

# 自訂配置
custom_config = {
    'title_font': 'Arial',
    'body_font': 'Arial',
    'title_size': 18,
    'body_size': 12,
    'title_color': RGBColor(0, 102, 204),
    'margin_top': Inches(1.25),
    'line_spacing': 1.5,
    'confidential_text': 'CONFIDENTIAL & PROPRIETARY',
}

# 使用自訂配置建立格式化引擎
formatter = WordFormatter(config=custom_config)
formatter.create_document()

# ... 繼續使用
```

### 範例4: 添加表格

```python
# 建立表格
table = formatter.doc.add_table(rows=4, cols=2)
formatter.apply_table_style(table)

# 填入資料
table.rows[0].cells[0].text = 'Study Phase'
table.rows[0].cells[1].text = 'Phase III'
table.rows[1].cells[0].text = 'Sample Size'
table.rows[1].cells[1].text = '300 subjects'
# ...
```

### 範例5: 包含Logo

```python
formatter = create_clinical_document(
    document_title="Clinical Study Report",
    protocol_number="CSR-2025-001",
    version="Final 1.0",
    logo_path="templates/company_logo.png",  # Logo路徑
    output_path="output/report.docx"
)
```

## 完整API參考

### WordFormatter類

#### 初始化
```python
formatter = WordFormatter(config=None)
```
- `config`: 可選的配置字典，會覆蓋預設配置

#### 主要方法

##### create_document(template_path=None)
建立新文件或從範本載入
- `template_path`: 範本文件路徑（可選）
- 返回: Document物件

##### set_page_format(page_size='A4', orientation='portrait', ...)
設定頁面格式
- `page_size`: 頁面大小 ('A4', 'Letter')
- `orientation`: 頁面方向 ('portrait', 'landscape')
- `margin_top/bottom/left/right`: 邊距設定

##### set_header(document_title, protocol_number, version, logo_path=None, include_date=True)
設定文件頁首
- `document_title`: 文件標題
- `protocol_number`: Protocol編號
- `version`: 版本資訊
- `logo_path`: 公司Logo路徑（可選）
- `include_date`: 是否包含日期

##### set_footer(confidential=True, include_page_numbers=True, include_date=True, custom_text=None)
設定文件頁尾
- `confidential`: 是否顯示機密聲明
- `include_page_numbers`: 是否包含頁碼
- `include_date`: 是否包含日期
- `custom_text`: 自訂文字

##### apply_title_style(text, level=1)
添加並套用標題樣式
- `text`: 標題文字
- `level`: 標題層級（1-3）
- 返回: 段落物件

##### apply_body_style(text, alignment='left')
添加並套用內文樣式
- `text`: 內文文字
- `alignment`: 對齊方式 ('left', 'center', 'right', 'justify')
- 返回: 段落物件

##### apply_table_style(table, style_name='Light Grid Accent 1', header_row=True, auto_fit=True)
套用表格樣式
- `table`: 表格物件
- `style_name`: 表格樣式名稱
- `header_row`: 是否有標題列
- `auto_fit`: 是否自動調整欄寬

##### apply_clinical_trial_template(document_title, protocol_number, version, sponsor="", indication="", logo_path=None)
套用臨床試驗文件標準範本
- 自動設定頁面格式、頁首、頁尾
- 生成標準封面頁

##### save_document(output_path)
儲存文件
- `output_path`: 輸出文件路徑

### 便利函數

#### create_clinical_document(...)
快速建立臨床試驗文件
```python
formatter = create_clinical_document(
    document_title="Protocol Title",
    protocol_number="PRO-2025-001",
    version="1.0",
    output_path="output.docx",
    sponsor="Company Name",
    indication="Disease",
    logo_path=None,
    custom_config=None
)
```

## 預設配置

```python
DEFAULT_CONFIG = {
    # 頁面設定
    'page_size': 'A4',
    'margin_top': Inches(1.0),
    'margin_bottom': Inches(1.0),
    'margin_left': Inches(1.0),
    'margin_right': Inches(1.0),

    # 字體設定
    'title_font': 'Calibri',
    'title_size': 16,
    'title_bold': True,
    'title_color': RGBColor(0, 51, 102),  # 深藍色

    'heading1_font': 'Calibri',
    'heading1_size': 14,
    'heading1_bold': True,

    'body_font': 'Calibri',
    'body_size': 11,
    'body_bold': False,

    'table_font': 'Calibri',
    'table_size': 10,

    # 行距設定
    'line_spacing': 1.15,
    'paragraph_spacing_after': Pt(10),

    # 頁首頁尾
    'confidential_text': 'CONFIDENTIAL',
    'show_page_numbers': True,
}
```

## 使用範例

完整的使用範例請參考 `examples/word_formatter_example.py`，包含：

1. **範例1**: 基本使用
2. **範例2**: 完整的Protocol文件
3. **範例3**: 自訂配置
4. **範例4**: 包含Logo的文件
5. **範例5**: 從現有範本載入
6. **範例6**: 複雜表格格式化

執行範例：
```bash
# 執行所有範例
python examples/word_formatter_example.py --all

# 執行特定範例
python examples/word_formatter_example.py --example 1
```

## 臨床試驗文件類型支援

此格式化引擎適用於以下臨床試驗文件：

- Clinical Study Protocol (研究計畫書)
- Investigator's Brochure (研究者手冊)
- Clinical Study Report (臨床試驗報告)
- Informed Consent Form (受試者同意書)
- Case Report Form (病例報告表)
- Study Visit Schedule (訪視時程表)
- Safety Report (安全性報告)

## 注意事項

1. **字體支援**: 確保系統已安裝Calibri或Arial字體
2. **Logo格式**: Logo圖片建議使用PNG格式，解析度至少300dpi
3. **範本文件**: 使用範本時，請確保範本文件格式正確
4. **中文支援**: 已支援中英文混合內容
5. **版本控制**: 建議將生成的文件納入版本控制系統

## 進階應用

### 批次處理多個文件

```python
protocols = [
    {'number': 'PRO-001', 'title': 'Study A'},
    {'number': 'PRO-002', 'title': 'Study B'},
]

for protocol in protocols:
    formatter = create_clinical_document(
        document_title=protocol['title'],
        protocol_number=protocol['number'],
        version="1.0",
        output_path=f"output/{protocol['number']}.docx"
    )
    # 添加內容...
    formatter.save_document(f"output/{protocol['number']}.docx")
```

### 整合到文件生成流程

```python
# 結合AI生成內容
from modules.word_formatter import WordFormatter

formatter = WordFormatter()
formatter.create_document()
formatter.apply_clinical_trial_template(...)

# 使用AI生成的內容
sections = generate_protocol_content()  # 您的AI生成函數

for section in sections:
    formatter.apply_title_style(section['title'], level=2)
    formatter.apply_body_style(section['content'])

formatter.save_document("output/ai_generated_protocol.docx")
```

## 支援與貢獻

如有問題或建議，請聯繫開發團隊。

## 授權

Copyright © 2025 Clinical Document Automation Team
