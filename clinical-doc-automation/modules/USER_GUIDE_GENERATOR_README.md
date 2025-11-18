# EDC/ePRO User Guide Generator Module

## 概述

User Guide Generator 是一個自動生成 EDC/ePRO 系統使用者指南的模組。它基於 Protocol 資訊和 CRF 設計，自動產生完整、專業的 Word 格式使用者指南文件。

## 主要功能

### 1. 自動生成完整的使用者指南
- **封面頁**：包含 Protocol 資訊、版本和日期
- **簡介**：說明指南目的和適用對象
- **系統登入**：詳細的登入步驟和疑難排解
- **系統導航**：介面概覽和操作說明
- **資料輸入說明**：針對每個 CRF 的詳細操作步驟
- **疑問管理**：Query 處理流程和最佳實踐
- **報表產生**：報表類型和產生步驟
- **附錄**：聯絡資訊、縮寫表和修訂歷史

### 2. 截圖管理功能
- 自動標記需要截圖的位置
- 提供截圖說明文字和尺寸要求
- 生成截圖需求清單文件
- 支援後續插入實際截圖

### 3. 專業文件格式
- 使用 python-docx 生成 Word 文件
- 自訂樣式和格式
- 專業的章節結構
- 清晰的步驟說明

## 安裝需求

```bash
pip install python-docx
```

## 使用方法

### 基本使用

```python
from modules.user_guide_generator import UserGuideGenerator

# 準備 Protocol 資訊
protocol_info = {
    'protocol_id': 'PROTO-2025-001',
    'protocol_title': 'Study Title',
    'sponsor': 'Sponsor Name',
    'version': '1.0',
    'date': '2025-11-18'
}

# 準備 CRF 設計
crf_design = {
    'forms': [
        {
            'form_name': 'demographics',
            'form_title': 'Demographics',
            'visit': 'Screening',
            'fields': [
                {
                    'field_name': 'subject_initials',
                    'field_label': 'Subject Initials',
                    'field_type': 'text',
                    'required': True,
                    'validation': '3 letters only'
                },
                # 更多欄位...
            ]
        },
        # 更多表單...
    ]
}

# 建立生成器
generator = UserGuideGenerator(
    protocol_info=protocol_info,
    crf_design=crf_design,
    system_name="My EDC System"
)

# 生成使用者指南
output_path = "user_guide.docx"
generator.generate(output_path)
```

### 截圖管理

```python
# 取得所有截圖需求
screenshots = generator.get_screenshot_list()

# 顯示截圖需求
for screenshot in screenshots:
    print(f"Section: {screenshot.section}")
    print(f"Step: {screenshot.step}")
    print(f"Description: {screenshot.description}")
    print(f"Size: {screenshot.width} x {screenshot.height} inches")
    print()

# 匯出截圖需求清單
generator.export_screenshot_list("screenshot_requirements.txt")
```

### 不包含附錄

```python
# 生成不包含附錄的使用者指南
generator.generate(output_path, include_appendix=False)
```

## 資料結構

### Protocol Information

```python
protocol_info = {
    'protocol_id': str,        # Protocol ID
    'protocol_title': str,     # Protocol 標題
    'sponsor': str,            # 贊助商名稱
    'version': str,            # 文件版本
    'date': str                # 日期 (YYYY-MM-DD)
}
```

### CRF Design

```python
crf_design = {
    'forms': [
        {
            'form_name': str,      # 表單名稱（系統識別用）
            'form_title': str,     # 表單標題（顯示用）
            'visit': str,          # 訪視時間點
            'fields': [
                {
                    'field_name': str,        # 欄位名稱
                    'field_label': str,       # 欄位標籤
                    'field_type': str,        # 欄位類型
                    'required': bool,         # 是否必填
                    'validation': str         # 驗證規則
                }
            ]
        }
    ]
}
```

### 支援的欄位類型

- `text` / `string` - 文字欄位
- `number` / `integer` / `decimal` - 數字欄位
- `date` - 日期欄位
- `dropdown` / `select` - 下拉選單
- `radio` - 單選按鈕
- `checkbox` - 核取方塊
- `textarea` - 文字區域

## 輸出檔案

執行生成後，會產生以下檔案：

1. **user_guide.docx** - 完整的使用者指南 Word 文件
2. **user_guide_screenshots.txt** - 截圖需求清單

## Screenshot Placeholder 類別

```python
class ScreenshotPlaceholder:
    """截圖佔位符類別"""

    def __init__(self, section, step, description, width=6.0, height=4.0):
        self.section = section          # 所屬章節
        self.step = step                # 步驟編號
        self.description = description  # 截圖說明
        self.width = width              # 寬度（英寸）
        self.height = height            # 高度（英寸）
        self.inserted = False           # 是否已插入實際截圖
```

## 範例

詳細的使用範例請參考：
- `examples/example_user_guide_generation.py`

執行範例：

```bash
# 執行所有範例
python examples/example_user_guide_generation.py

# 執行特定範例
python examples/example_user_guide_generation.py 1  # 基本使用
python examples/example_user_guide_generation.py 2  # 自訂 Protocol
python examples/example_user_guide_generation.py 3  # 截圖管理
python examples/example_user_guide_generation.py 4  # 最小 CRF
python examples/example_user_guide_generation.py 5  # 不含附錄
```

## 自訂化

### 修改文件樣式

```python
# 繼承 UserGuideGenerator 並覆寫樣式設定
class CustomUserGuideGenerator(UserGuideGenerator):
    def _setup_document_styles(self):
        super()._setup_document_styles()
        # 新增自訂樣式
        # ...
```

### 新增自訂章節

```python
class ExtendedUserGuideGenerator(UserGuideGenerator):
    def generate(self, output_path, include_appendix=True):
        # 呼叫原有的生成方法
        super().generate(output_path, include_appendix)

        # 新增自訂章節
        self._add_custom_section()

    def _add_custom_section(self):
        self._add_heading("Custom Section", level=1)
        self._add_paragraph("Custom content...")
```

## 最佳實踐

1. **資料完整性**
   - 確保 protocol_info 包含所有必要資訊
   - 提供詳細的 CRF 欄位驗證規則

2. **截圖管理**
   - 生成文件後立即檢視截圖需求清單
   - 規劃截圖拍攝順序和內容
   - 使用一致的截圖風格和解析度

3. **文件維護**
   - 使用版本控制追蹤文件變更
   - 定期更新修訂歷史
   - 保存生成參數供日後參考

4. **質量檢查**
   - 生成後檢查所有章節內容
   - 驗證表單和欄位資訊正確性
   - 確認步驟說明清晰易懂

## 疑難排解

### 常見問題

**Q: 生成的文件無法開啟**
A: 確保已安裝 python-docx 並且版本正確

**Q: 截圖佔位符未顯示**
A: 檢查 Word 設定是否顯示表格邊框

**Q: 中文字顯示異常**
A: 確保系統已安裝中文字型

**Q: 表單資訊不完整**
A: 檢查 crf_design 資料結構是否完整

## 技術支援

如有問題或建議，請聯絡開發團隊。

## 版本歷史

- **v1.0.0** (2025-11-18)
  - 初始版本
  - 支援基本使用者指南生成
  - 截圖管理功能
  - 完整的 CRF 資料輸入說明

## 授權

Copyright © 2025 Clinical Documentation Automation Team
