"""
Word文件格式化引擎 - 配置範例
展示如何為不同公司或文件類型建立自訂配置
"""

from docx.shared import RGBColor, Inches, Pt


# 範例1: 標準臨床試驗文件配置
STANDARD_CLINICAL_CONFIG = {
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
    'heading1_color': RGBColor(0, 51, 102),

    'heading2_font': 'Calibri',
    'heading2_size': 12,
    'heading2_bold': True,
    'heading2_color': RGBColor(0, 51, 102),

    'body_font': 'Calibri',
    'body_size': 11,
    'body_bold': False,
    'body_color': RGBColor(0, 0, 0),

    'table_font': 'Calibri',
    'table_size': 10,

    # 行距設定
    'line_spacing': 1.15,
    'paragraph_spacing_before': Pt(0),
    'paragraph_spacing_after': Pt(10),

    # 頁首頁尾
    'confidential_text': 'CONFIDENTIAL',
    'show_page_numbers': True,

    # 公司資訊
    'company_name': 'Clinical Research Organization',
}


# 範例2: FDA提交文件配置（更正式）
FDA_SUBMISSION_CONFIG = {
    # 頁面設定 - FDA通常要求較大的邊距
    'margin_top': Inches(1.25),
    'margin_bottom': Inches(1.25),
    'margin_left': Inches(1.5),
    'margin_right': Inches(1.0),

    # 字體設定 - FDA偏好Times New Roman
    'title_font': 'Times New Roman',
    'heading1_font': 'Times New Roman',
    'heading2_font': 'Times New Roman',
    'body_font': 'Times New Roman',
    'table_font': 'Times New Roman',

    'title_size': 16,
    'heading1_size': 14,
    'heading2_size': 12,
    'body_size': 12,  # FDA通常要求12pt
    'table_size': 11,

    # 顏色 - 黑色為主
    'title_color': RGBColor(0, 0, 0),
    'heading1_color': RGBColor(0, 0, 0),
    'heading2_color': RGBColor(0, 0, 0),

    # 行距 - 雙倍行距
    'line_spacing': 2.0,
    'paragraph_spacing_after': Pt(0),

    'confidential_text': 'CONFIDENTIAL - FOR REGULATORY SUBMISSION',
}


# 範例3: 歐盟EMA提交文件配置
EMA_SUBMISSION_CONFIG = {
    # 頁面設定
    'page_size': 'A4',  # EMA使用A4
    'margin_top': Inches(1.0),
    'margin_bottom': Inches(1.0),
    'margin_left': Inches(1.0),
    'margin_right': Inches(1.0),

    # 字體設定
    'title_font': 'Arial',
    'heading1_font': 'Arial',
    'heading2_font': 'Arial',
    'body_font': 'Arial',
    'table_font': 'Arial',

    'title_size': 14,
    'heading1_size': 12,
    'heading2_size': 11,
    'body_size': 11,
    'table_size': 10,

    # 顏色
    'title_color': RGBColor(0, 0, 0),
    'heading1_color': RGBColor(0, 0, 0),

    # 行距
    'line_spacing': 1.5,

    'confidential_text': 'CONFIDENTIAL - EMA SUBMISSION',
}


# 範例4: 內部文件配置（較輕鬆的格式）
INTERNAL_DOCUMENT_CONFIG = {
    # 字體設定 - 使用現代字體
    'title_font': 'Calibri',
    'body_font': 'Calibri',
    'title_size': 18,
    'body_size': 11,

    # 使用公司品牌色
    'title_color': RGBColor(0, 102, 204),  # 公司藍色
    'heading1_color': RGBColor(0, 102, 204),
    'heading2_color': RGBColor(64, 64, 64),  # 深灰色

    # 較窄的邊距
    'margin_top': Inches(0.75),
    'margin_bottom': Inches(0.75),
    'margin_left': Inches(0.75),
    'margin_right': Inches(0.75),

    # 單倍行距
    'line_spacing': 1.0,

    'confidential_text': 'INTERNAL USE ONLY',
}


# 範例5: 生物製藥公司配置
BIOPHARMA_CONFIG = {
    # 頁面設定
    'margin_top': Inches(1.0),
    'margin_bottom': Inches(1.0),
    'margin_left': Inches(1.25),
    'margin_right': Inches(1.0),

    # 字體設定
    'title_font': 'Arial',
    'heading1_font': 'Arial',
    'heading2_font': 'Arial',
    'body_font': 'Calibri',  # 內文使用Calibri更易讀
    'table_font': 'Calibri',

    'title_size': 16,
    'heading1_size': 14,
    'heading2_size': 12,
    'body_size': 11,
    'table_size': 10,

    # 公司品牌色
    'title_color': RGBColor(0, 51, 102),  # 深藍色
    'heading1_color': RGBColor(0, 102, 153),  # 中藍色
    'heading2_color': RGBColor(51, 51, 51),  # 深灰色

    # 行距
    'line_spacing': 1.15,
    'paragraph_spacing_after': Pt(10),

    # 頁首頁尾
    'confidential_text': 'CONFIDENTIAL & PROPRIETARY',
    'company_name': 'BioPharma Research Inc.',
}


# 範例6: CRO (Contract Research Organization) 配置
CRO_CONFIG = {
    # 頁面設定
    'margin_top': Inches(1.0),
    'margin_bottom': Inches(1.0),
    'margin_left': Inches(1.0),
    'margin_right': Inches(1.0),

    # 字體設定 - 專業且易讀
    'title_font': 'Calibri',
    'heading1_font': 'Calibri',
    'heading2_font': 'Calibri',
    'body_font': 'Calibri',
    'table_font': 'Calibri',

    'title_size': 16,
    'title_bold': True,
    'heading1_size': 14,
    'heading1_bold': True,
    'heading2_size': 12,
    'heading2_bold': True,
    'body_size': 11,
    'table_size': 10,

    # 顏色方案
    'title_color': RGBColor(0, 51, 102),
    'heading1_color': RGBColor(0, 51, 102),
    'heading2_color': RGBColor(0, 51, 102),

    # 行距
    'line_spacing': 1.15,
    'paragraph_spacing_before': Pt(0),
    'paragraph_spacing_after': Pt(10),

    # 頁首頁尾
    'confidential_text': 'CONFIDENTIAL',
    'show_page_numbers': True,
    'page_number_format': 'Page {0} of {1}',

    'company_name': 'Global CRO Services',
}


# 範例7: ICH GCP標準配置
ICH_GCP_CONFIG = {
    # ICH (International Council for Harmonisation) GCP標準格式
    'page_size': 'A4',

    # 字體設定
    'title_font': 'Arial',
    'heading1_font': 'Arial',
    'heading2_font': 'Arial',
    'body_font': 'Arial',
    'table_font': 'Arial',

    'title_size': 14,
    'heading1_size': 12,
    'heading2_size': 11,
    'body_size': 11,
    'table_size': 10,

    # 黑色為主
    'title_color': RGBColor(0, 0, 0),
    'heading1_color': RGBColor(0, 0, 0),
    'heading2_color': RGBColor(0, 0, 0),

    # 標準邊距
    'margin_top': Inches(1.0),
    'margin_bottom': Inches(1.0),
    'margin_left': Inches(1.0),
    'margin_right': Inches(1.0),

    # 1.5倍行距
    'line_spacing': 1.5,

    'confidential_text': 'CONFIDENTIAL',
}


# 配置選擇器
CONFIGS = {
    'standard': STANDARD_CLINICAL_CONFIG,
    'fda': FDA_SUBMISSION_CONFIG,
    'ema': EMA_SUBMISSION_CONFIG,
    'internal': INTERNAL_DOCUMENT_CONFIG,
    'biopharma': BIOPHARMA_CONFIG,
    'cro': CRO_CONFIG,
    'ich_gcp': ICH_GCP_CONFIG,
}


def get_config(config_name='standard'):
    """
    取得指定的配置

    Args:
        config_name: 配置名稱 ('standard', 'fda', 'ema', 'internal', 'biopharma', 'cro', 'ich_gcp')

    Returns:
        配置字典
    """
    if config_name not in CONFIGS:
        print(f"警告：找不到配置 '{config_name}'，使用標準配置")
        return STANDARD_CLINICAL_CONFIG

    return CONFIGS[config_name].copy()


def print_config_info():
    """列印所有可用配置的資訊"""
    print("\n可用的配置：")
    print("=" * 60)

    config_descriptions = {
        'standard': '標準臨床試驗文件配置（預設）',
        'fda': 'FDA提交文件配置（Times New Roman，雙倍行距）',
        'ema': '歐盟EMA提交文件配置（Arial，A4）',
        'internal': '內部文件配置（較輕鬆的格式）',
        'biopharma': '生物製藥公司配置（品牌色彩）',
        'cro': 'CRO配置（專業且易讀）',
        'ich_gcp': 'ICH GCP標準配置（國際標準）',
    }

    for name, description in config_descriptions.items():
        print(f"\n{name}:")
        print(f"  {description}")
        config = CONFIGS[name]
        print(f"  - 字體: {config.get('body_font', 'Calibri')} {config.get('body_size', 11)}pt")
        print(f"  - 行距: {config.get('line_spacing', 1.15)}")
        print(f"  - 機密文字: {config.get('confidential_text', 'CONFIDENTIAL')}")


# 使用範例
if __name__ == "__main__":
    print_config_info()

    print("\n\n使用範例：")
    print("=" * 60)
    print("""
# 方法1: 直接匯入配置
from examples.config_example import FDA_SUBMISSION_CONFIG
from modules.word_formatter import WordFormatter

formatter = WordFormatter(config=FDA_SUBMISSION_CONFIG)

# 方法2: 使用get_config函數
from examples.config_example import get_config
from modules.word_formatter import WordFormatter

config = get_config('fda')
formatter = WordFormatter(config=config)

# 方法3: 自訂配置
from examples.config_example import get_config
from docx.shared import RGBColor

# 基於標準配置進行修改
config = get_config('standard')
config['title_color'] = RGBColor(255, 0, 0)  # 改為紅色
config['company_name'] = 'My Company'

formatter = WordFormatter(config=config)
    """)
