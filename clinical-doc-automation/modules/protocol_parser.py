"""
智能Protocol PDF解析器模組

此模組用於從臨床試驗Protocol文件中自動提取關鍵資訊。
使用Google Gemini API進行智能文本分析和資訊提取。

作者: Clinical Data Automation Team
日期: 2025-11-18
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import re

try:
    import pdfplumber
except ImportError:
    raise ImportError("請安裝 pdfplumber: pip install pdfplumber")

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("請安裝 google-generativeai: pip install google-generativeai")


# 設置logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProtocolInfo:
    """Protocol資訊結構"""
    study_title: Optional[str] = None
    protocol_number: Optional[str] = None
    sponsor: Optional[str] = None
    phase: Optional[str] = None
    study_design: Optional[str] = None
    target_population: Optional[str] = None
    sample_size: Optional[str] = None
    visit_schedule: Optional[List[str]] = None
    primary_endpoints: Optional[List[str]] = None
    secondary_endpoints: Optional[List[str]] = None
    inclusion_criteria: Optional[List[str]] = None
    exclusion_criteria: Optional[List[str]] = None
    crf_domains: Optional[List[str]] = None
    raw_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict:
        """轉換為字典格式"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """轉換為JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class ProtocolParser:
    """
    Protocol PDF解析器

    使用PDF讀取工具和Google Gemini API來智能提取臨床試驗Protocol中的關鍵資訊。
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        """
        初始化解析器

        Args:
            api_key: Google Gemini API金鑰，如果未提供則從環境變數GEMINI_API_KEY讀取
            model_name: 使用的Gemini模型名稱，預設為gemini-1.5-flash（免費版）
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("未提供API金鑰，請設置GEMINI_API_KEY環境變數或在初始化時提供api_key參數")

        self.model_name = model_name
        self._configure_gemini()

    def _configure_gemini(self):
        """配置Gemini API"""
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"成功配置Gemini API，使用模型: {self.model_name}")
            except Exception as e:
                logger.error(f"配置Gemini API失敗: {str(e)}")
                self.model = None
        else:
            self.model = None

    def extract_text_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None) -> str:
        """
        從PDF檔案中提取文本

        Args:
            pdf_path: PDF檔案路徑
            max_pages: 最大讀取頁數，None表示讀取全部

        Returns:
            提取的文本內容
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF檔案不存在: {pdf_path}")

            logger.info(f"開始讀取PDF: {pdf_path}")
            text_content = []

            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_read = min(max_pages, total_pages) if max_pages else total_pages

                logger.info(f"PDF總頁數: {total_pages}，將讀取: {pages_to_read}頁")

                for i, page in enumerate(pdf.pages[:pages_to_read]):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"--- Page {i+1} ---\n{page_text}")

                    if (i + 1) % 10 == 0:
                        logger.info(f"已讀取 {i+1}/{pages_to_read} 頁")

            full_text = "\n\n".join(text_content)
            logger.info(f"成功提取文本，總字數: {len(full_text)}")
            return full_text

        except Exception as e:
            logger.error(f"提取PDF文本時發生錯誤: {str(e)}")
            raise

    def _create_extraction_prompt(self, text: str) -> str:
        """
        創建用於資訊提取的提示詞

        Args:
            text: PDF文本內容

        Returns:
            格式化的提示詞
        """
        prompt = f"""
你是一位專業的臨床試驗文件分析專家。請從以下Protocol文件中提取關鍵資訊，並以JSON格式返回。

請提取以下資訊（如果文件中沒有某項資訊，請使用null）：

1. **study_title**: 試驗標題（完整標題）
2. **protocol_number**: 試驗編號/Protocol編號
3. **sponsor**: 贊助商名稱
4. **phase**: 試驗階段（如Phase I, Phase II, Phase III, Phase IV）
5. **study_design**: 試驗設計（如隨機雙盲對照試驗、開放標籤試驗等）
6. **target_population**: 目標族群描述
7. **sample_size**: 樣本數（計劃收案人數）
8. **visit_schedule**: 訪視時程（以列表形式列出各訪視時間點，如["Screening", "Day 1", "Week 4", "Week 8"]）
9. **primary_endpoints**: 主要終點指標（列表形式）
10. **secondary_endpoints**: 次要終點指標（列表形式）
11. **inclusion_criteria**: 納入標準（列表形式，每個標準為一個項目）
12. **exclusion_criteria**: 排除標準（列表形式，每個標準為一個項目）
13. **crf_domains**: 需要的CRF領域（列表形式，如["Demographics", "Vital Signs", "Adverse Events", "Concomitant Medications", "Laboratory", "ECG", "Physical Examination", "Efficacy Assessments"]）

請確保返回的JSON格式正確，並且所有列表項目都是字符串。

Protocol文件內容:
{text[:50000]}

請以以下JSON格式返回（不要包含其他說明文字，只返回JSON）:
{{
    "study_title": "...",
    "protocol_number": "...",
    "sponsor": "...",
    "phase": "...",
    "study_design": "...",
    "target_population": "...",
    "sample_size": "...",
    "visit_schedule": [...],
    "primary_endpoints": [...],
    "secondary_endpoints": [...],
    "inclusion_criteria": [...],
    "exclusion_criteria": [...],
    "crf_domains": [...]
}}
"""
        return prompt

    def extract_info_with_gemini(self, text: str) -> Dict[str, Any]:
        """
        使用Gemini API提取資訊

        Args:
            text: PDF文本內容

        Returns:
            提取的結構化資訊
        """
        if not self.model:
            raise ValueError("Gemini API未正確配置，請檢查API金鑰")

        try:
            logger.info("開始使用Gemini API提取資訊...")
            prompt = self._create_extraction_prompt(text)

            # 呼叫Gemini API
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # 降低隨機性，提高準確性
                    max_output_tokens=4096,
                )
            )

            # 提取回應文本
            response_text = response.text.strip()
            logger.info(f"收到Gemini回應，長度: {len(response_text)}")

            # 嘗試解析JSON
            # 移除可能的markdown代碼塊標記
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            response_text = response_text.strip()

            try:
                extracted_info = json.loads(response_text)
                logger.info("成功解析JSON回應")
                return extracted_info
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失敗: {str(e)}")
                logger.debug(f"原始回應: {response_text[:500]}")
                # 返回原始文本以供調試
                return {"raw_response": response_text, "parse_error": str(e)}

        except Exception as e:
            logger.error(f"使用Gemini提取資訊時發生錯誤: {str(e)}")
            raise

    def parse_protocol(self, pdf_path: str, max_pages: Optional[int] = None) -> ProtocolInfo:
        """
        解析Protocol PDF檔案

        Args:
            pdf_path: PDF檔案路徑
            max_pages: 最大讀取頁數，None表示讀取全部

        Returns:
            ProtocolInfo物件，包含提取的所有資訊
        """
        try:
            # 1. 提取PDF文本
            logger.info(f"開始解析Protocol: {pdf_path}")
            text = self.extract_text_from_pdf(pdf_path, max_pages)

            # 2. 使用Gemini提取資訊
            extracted_info = self.extract_info_with_gemini(text)

            # 3. 創建ProtocolInfo物件
            protocol_info = ProtocolInfo(
                study_title=extracted_info.get("study_title"),
                protocol_number=extracted_info.get("protocol_number"),
                sponsor=extracted_info.get("sponsor"),
                phase=extracted_info.get("phase"),
                study_design=extracted_info.get("study_design"),
                target_population=extracted_info.get("target_population"),
                sample_size=extracted_info.get("sample_size"),
                visit_schedule=extracted_info.get("visit_schedule"),
                primary_endpoints=extracted_info.get("primary_endpoints"),
                secondary_endpoints=extracted_info.get("secondary_endpoints"),
                inclusion_criteria=extracted_info.get("inclusion_criteria"),
                exclusion_criteria=extracted_info.get("exclusion_criteria"),
                crf_domains=extracted_info.get("crf_domains"),
                raw_data=extracted_info
            )

            logger.info("Protocol解析完成")
            return protocol_info

        except Exception as e:
            logger.error(f"解析Protocol時發生錯誤: {str(e)}")
            raise

    def save_to_json(self, protocol_info: ProtocolInfo, output_path: str):
        """
        將提取的資訊保存為JSON檔案

        Args:
            protocol_info: ProtocolInfo物件
            output_path: 輸出檔案路徑
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(protocol_info.to_json())

            logger.info(f"成功保存JSON檔案: {output_path}")

        except Exception as e:
            logger.error(f"保存JSON檔案時發生錯誤: {str(e)}")
            raise


# ===== 範例使用代碼 =====

def example_usage():
    """
    範例使用代碼

    展示如何使用ProtocolParser來解析Protocol PDF檔案
    """
    print("=" * 80)
    print("Protocol PDF解析器 - 範例使用")
    print("=" * 80)

    # 1. 設置API金鑰（方式一：環境變數）
    # export GEMINI_API_KEY="your-api-key-here"

    # 方式二：直接提供
    api_key = "YOUR_GEMINI_API_KEY"  # 替換為您的實際API金鑰

    # 2. 初始化解析器
    parser = ProtocolParser(api_key=api_key)

    # 3. 解析Protocol PDF
    pdf_path = "/path/to/your/protocol.pdf"  # 替換為實際的PDF路徑

    try:
        # 選項1: 讀取全部頁面
        protocol_info = parser.parse_protocol(pdf_path)

        # 選項2: 只讀取前50頁（對於大型文件）
        # protocol_info = parser.parse_protocol(pdf_path, max_pages=50)

        # 4. 顯示提取的資訊
        print("\n提取的Protocol資訊:")
        print("-" * 80)
        print(f"試驗標題: {protocol_info.study_title}")
        print(f"Protocol編號: {protocol_info.protocol_number}")
        print(f"贊助商: {protocol_info.sponsor}")
        print(f"試驗階段: {protocol_info.phase}")
        print(f"試驗設計: {protocol_info.study_design}")
        print(f"目標族群: {protocol_info.target_population}")
        print(f"樣本數: {protocol_info.sample_size}")

        print("\n訪視時程:")
        if protocol_info.visit_schedule:
            for visit in protocol_info.visit_schedule:
                print(f"  - {visit}")

        print("\n主要終點:")
        if protocol_info.primary_endpoints:
            for endpoint in protocol_info.primary_endpoints:
                print(f"  - {endpoint}")

        print("\n次要終點:")
        if protocol_info.secondary_endpoints:
            for endpoint in protocol_info.secondary_endpoints:
                print(f"  - {endpoint}")

        print("\n納入標準:")
        if protocol_info.inclusion_criteria:
            for i, criterion in enumerate(protocol_info.inclusion_criteria[:5], 1):
                print(f"  {i}. {criterion}")
            if len(protocol_info.inclusion_criteria) > 5:
                print(f"  ... 還有 {len(protocol_info.inclusion_criteria) - 5} 項")

        print("\n排除標準:")
        if protocol_info.exclusion_criteria:
            for i, criterion in enumerate(protocol_info.exclusion_criteria[:5], 1):
                print(f"  {i}. {criterion}")
            if len(protocol_info.exclusion_criteria) > 5:
                print(f"  ... 還有 {len(protocol_info.exclusion_criteria) - 5} 項")

        print("\nCRF領域:")
        if protocol_info.crf_domains:
            for domain in protocol_info.crf_domains:
                print(f"  - {domain}")

        # 5. 保存為JSON檔案
        output_path = "/path/to/output/protocol_info.json"  # 替換為實際的輸出路徑
        parser.save_to_json(protocol_info, output_path)
        print(f"\n✓ JSON檔案已保存至: {output_path}")

        # 6. 也可以直接獲取JSON字符串
        json_str = protocol_info.to_json()
        print("\nJSON格式:")
        print(json_str[:500] + "...")

    except FileNotFoundError:
        print(f"錯誤: 找不到PDF檔案 {pdf_path}")
        print("請將 pdf_path 變數替換為實際的PDF檔案路徑")
    except Exception as e:
        print(f"錯誤: {str(e)}")
        import traceback
        traceback.print_exc()


def quick_start_guide():
    """
    快速開始指南
    """
    guide = """
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    Protocol PDF解析器 - 快速開始指南                        ║
    ╚════════════════════════════════════════════════════════════════════════════╝

    【安裝依賴】
    pip install pdfplumber google-generativeai

    【獲取Gemini API金鑰】
    1. 訪問 https://makersuite.google.com/app/apikey
    2. 創建新的API金鑰（免費）
    3. 複製API金鑰

    【基本使用】

    from protocol_parser import ProtocolParser

    # 初始化解析器
    parser = ProtocolParser(api_key="YOUR_API_KEY")

    # 解析Protocol
    protocol_info = parser.parse_protocol("protocol.pdf")

    # 保存結果
    parser.save_to_json(protocol_info, "output.json")

    # 訪問特定資訊
    print(protocol_info.study_title)
    print(protocol_info.protocol_number)
    print(protocol_info.crf_domains)

    【進階選項】

    # 只讀取前30頁（加快處理速度）
    protocol_info = parser.parse_protocol("protocol.pdf", max_pages=30)

    # 使用環境變數設置API金鑰
    import os
    os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
    parser = ProtocolParser()  # 自動從環境變數讀取

    # 使用不同的模型
    parser = ProtocolParser(
        api_key="YOUR_API_KEY",
        model_name="gemini-1.5-pro"  # 更強大但可能有額度限制
    )

    【常見CRF領域】
    - Demographics (人口學資料)
    - Vital Signs (生命徵象)
    - Adverse Events (不良事件)
    - Concomitant Medications (併用藥物)
    - Laboratory (實驗室檢查)
    - ECG (心電圖)
    - Physical Examination (身體檢查)
    - Medical History (病史)
    - Efficacy Assessments (療效評估)
    - Quality of Life (生活品質)
    - Pharmacokinetics (藥物動力學)

    【注意事項】
    - Gemini 1.5 Flash 是免費的，適合大多數使用場景
    - 對於超大型PDF（>100頁），建議使用max_pages參數
    - API有速率限制，大量處理時請注意間隔
    - 建議將API金鑰存儲在環境變數中，不要硬編碼

    【錯誤處理】

    try:
        protocol_info = parser.parse_protocol("protocol.pdf")
    except FileNotFoundError:
        print("PDF檔案不存在")
    except ValueError:
        print("API金鑰未設置")
    except Exception as e:
        print(f"發生錯誤: {e}")

    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                           需要幫助？                                        ║
    ║  查看日誌輸出以獲取詳細的處理資訊和錯誤診斷                                 ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(guide)


if __name__ == "__main__":
    # 顯示快速開始指南
    quick_start_guide()

    print("\n" + "=" * 80)
    print("如要運行範例，請取消註釋以下行並設置正確的API金鑰和檔案路徑:")
    print("=" * 80)
    # example_usage()
