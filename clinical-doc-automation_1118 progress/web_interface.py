"""
臨床試驗文件自動化系統 - Web UI 介面

此模組提供一個基於Gradio的Web介面，讓使用者可以透過瀏覽器使用臨床試驗文件自動化系統。

功能：
- 上傳Protocol PDF
- 設定Gemini API Key
- 上傳公司Logo（選填）
- 選擇要生成的文件類型（CRF、DVP、User Guide、DMP）
- 自訂Protocol資訊
- 預覽生成的文件資訊
- 一鍵生成並下載
- 顯示進度條

作者: Clinical Data Automation Team
日期: 2025-11-18
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import traceback

# 添加模組路徑
sys.path.insert(0, str(Path(__file__).parent))

try:
    import gradio as gr
except ImportError:
    print("請安裝 Gradio: pip install gradio")
    sys.exit(1)

# 導入模組
try:
    from modules.protocol_parser import ProtocolParser, ProtocolInfo
    from modules.crf_generator import CRFGenerator
    from modules.dvp_generator import DVPGenerator
    from modules.user_guide_generator import UserGuideGenerator
    from modules.word_formatter import WordFormatter
except ImportError as e:
    print(f"模組導入錯誤: {e}")
    print("請確保所有模組都已安裝")
    traceback.print_exc()


class ClinicalDocWebUI:
    """臨床試驗文件自動化Web UI"""

    def __init__(self):
        """初始化Web UI"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="clinical_doc_"))
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        # 初始化狀態
        self.protocol_info = None
        self.pdf_path = None
        self.logo_path = None
        self.api_key = None

        # 文件類型選項
        self.doc_types = {
            "CRF": "病例報告表 (Case Report Form)",
            "DVP": "資料驗證計劃 (Data Validation Plan)",
            "User Guide": "使用者指南 (User Guide)",
            "DMP": "資料管理計劃 (Data Management Plan)"
        }

    def upload_pdf(self, file) -> Tuple[str, str]:
        """
        上傳Protocol PDF

        Args:
            file: 上傳的檔案

        Returns:
            (狀態訊息, PDF路徑)
        """
        if file is None:
            return "❌ 請選擇PDF檔案", ""

        try:
            # 儲存檔案
            pdf_path = self.temp_dir / "protocol.pdf"
            shutil.copy(file.name, pdf_path)
            self.pdf_path = str(pdf_path)

            # 獲取檔案資訊
            file_size = pdf_path.stat().st_size / 1024  # KB

            return f"✅ PDF已上傳成功！\n檔案大小: {file_size:.1f} KB", self.pdf_path

        except Exception as e:
            return f"❌ 上傳失敗: {str(e)}", ""

    def upload_logo(self, file) -> str:
        """
        上傳公司Logo

        Args:
            file: 上傳的圖片檔案

        Returns:
            狀態訊息
        """
        if file is None:
            return "ℹ️ 未上傳Logo（選填）"

        try:
            # 儲存Logo
            logo_path = self.temp_dir / "logo.png"
            shutil.copy(file.name, logo_path)
            self.logo_path = str(logo_path)

            return f"✅ Logo已上傳成功！\n路徑: {logo_path.name}"

        except Exception as e:
            return f"❌ Logo上傳失敗: {str(e)}"

    def set_api_key(self, api_key: str) -> str:
        """
        設定Gemini API Key

        Args:
            api_key: API金鑰

        Returns:
            狀態訊息
        """
        if not api_key or api_key.strip() == "":
            return "❌ 請輸入有效的API Key"

        self.api_key = api_key.strip()
        os.environ["GEMINI_API_KEY"] = self.api_key

        return "✅ API Key已設定成功！"

    def parse_protocol(self, progress=gr.Progress()) -> Tuple[str, str]:
        """
        解析Protocol PDF

        Args:
            progress: Gradio進度條

        Returns:
            (狀態訊息, Protocol資訊JSON)
        """
        if not self.api_key:
            return "❌ 請先設定API Key", ""

        if not self.pdf_path or not Path(self.pdf_path).exists():
            return "❌ 請先上傳PDF檔案", ""

        try:
            progress(0, desc="初始化解析器...")

            # 初始化解析器
            parser = ProtocolParser(
                api_key=self.api_key,
                model_name="gemini-2.5-pro"
            )

            progress(0.2, desc="讀取PDF文本...")

            # 解析Protocol
            progress(0.4, desc="AI分析中（可能需要30-60秒）...")

            self.protocol_info = parser.parse_protocol(
                pdf_path=self.pdf_path,
                max_pages=None
            )

            progress(0.9, desc="整理結果...")

            # 生成JSON
            protocol_json = self.protocol_info.to_json(indent=2)

            progress(1.0, desc="完成！")

            return "✅ Protocol解析完成！", protocol_json

        except Exception as e:
            error_msg = f"❌ 解析失敗: {str(e)}\n\n{traceback.format_exc()}"
            return error_msg, ""

    def update_protocol_info(self, json_str: str) -> str:
        """
        更新Protocol資訊

        Args:
            json_str: Protocol資訊JSON字串

        Returns:
            狀態訊息
        """
        if not json_str or json_str.strip() == "":
            return "❌ Protocol資訊為空"

        try:
            # 解析JSON
            data = json.loads(json_str)

            # 更新Protocol資訊
            self.protocol_info = ProtocolInfo(**{
                k: v for k, v in data.items()
                if k in ProtocolInfo.__dataclass_fields__
            })

            return "✅ Protocol資訊已更新！"

        except json.JSONDecodeError as e:
            return f"❌ JSON格式錯誤: {str(e)}"
        except Exception as e:
            return f"❌ 更新失敗: {str(e)}"

    def generate_documents(
        self,
        doc_types: List[str],
        progress=gr.Progress()
    ) -> Tuple[str, List[str]]:
        """
        生成選定的文件

        Args:
            doc_types: 要生成的文件類型列表
            progress: Gradio進度條

        Returns:
            (狀態訊息, 生成的檔案路徑列表)
        """
        if not self.protocol_info:
            return "❌ 請先解析Protocol", []

        if not doc_types or len(doc_types) == 0:
            return "❌ 請至少選擇一種文件類型", []

        try:
            generated_files = []
            total_steps = len(doc_types)

            for idx, doc_type in enumerate(doc_types):
                progress((idx / total_steps), desc=f"生成 {doc_type}...")

                if doc_type == "CRF":
                    file_path = self._generate_crf()
                    if file_path:
                        generated_files.append(file_path)

                elif doc_type == "DVP":
                    file_path = self._generate_dvp()
                    if file_path:
                        generated_files.append(file_path)

                elif doc_type == "User Guide":
                    file_path = self._generate_user_guide()
                    if file_path:
                        generated_files.append(file_path)

                elif doc_type == "DMP":
                    file_path = self._generate_dmp()
                    if file_path:
                        generated_files.append(file_path)

            progress(1.0, desc="完成！")

            if generated_files:
                return f"✅ 成功生成 {len(generated_files)} 個文件！", generated_files
            else:
                return "⚠️ 沒有生成任何文件", []

        except Exception as e:
            error_msg = f"❌ 生成失敗: {str(e)}\n\n{traceback.format_exc()}"
            return error_msg, []

    # def _generate_crf(self) -> Optional[str]:
    #     """生成CRF文件"""
    #     try:
    #         generator = CRFGenerator(
    #             api_key=self.api_key,
    #             model_name="gemini-2.5-pro"
    #         )

    #         output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'CRF'}_CRF.docx"

    #         # 使用protocol_info生成CRF
    #         generator.generate_crf(
    #             protocol_info=self.protocol_info,
    #             output_path=str(output_path),
    #             logo_path=self.logo_path
    #         )

    #         return str(output_path)

    #     except Exception as e:
    #         print(f"CRF生成錯誤: {e}")
    #         traceback.print_exc()
    #         return None
    def _generate_crf(self) -> Optional[str]:
        """生成CRF文件"""
        try:
            # 修正：CRFGenerator 不需要 api_key，只需要 protocol_info 字典
            protocol_data = self.protocol_info.to_dict() if self.protocol_info else {}
            
            generator = CRFGenerator(protocol_info=protocol_data)

            output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'CRF'}_CRF.docx"

            # 修正：generate_crf 不需要 logo_path
            generator.generate_crf(
                output_path=str(output_path)
            )

            return str(output_path)

        except Exception as e:
            print(f"CRF生成錯誤: {e}")
            traceback.print_exc()
            return None

    # def _generate_dvp(self) -> Optional[str]:
    #     """生成DVP文件"""
    #     try:
    #         generator = DVPGenerator(
    #             api_key=self.api_key,
    #             model_name="gemini-2.5-pro"
    #         )

    #         output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'DVP'}_DVP.docx"

    #         # 使用protocol_info生成DVP
    #         generator.generate_dvp(
    #             protocol_info=self.protocol_info,
    #             output_path=str(output_path),
    #             logo_path=self.logo_path
    #         )

    #         return str(output_path)

    #     except Exception as e:
    #         print(f"DVP生成錯誤: {e}")
    #         traceback.print_exc()
    #         return None

    def _generate_dvp(self) -> Optional[str]:
        """生成DVP文件"""
        try:
            # 修正：需要導入 DVP 專用的類別，並建立正確的物件
            from modules.dvp_generator import DVPGenerator, ProtocolInfo as DVPProtocolInfo, CRFField
            from modules.crf_generator import CRFGenerator as CRFGenSource

            # 1. 轉換 Protocol 資訊為 DVP 模組需要的格式
            dvp_protocol_info = DVPProtocolInfo(
                protocol_number=self.protocol_info.protocol_number or "N/A",
                protocol_title=self.protocol_info.study_title or "N/A",
                sponsor=self.protocol_info.sponsor or "N/A",
                indication="N/A",
                phase=self.protocol_info.phase or "N/A"
            )
            
            # 2. 初始化生成器 (不需要 api_key)
            generator = DVPGenerator(protocol_info=dvp_protocol_info)
            
            # 3. 從 CRF 標準模板中提取欄位資訊 (因為 DVP 需要知道有哪些欄位)
            standard_domains = CRFGenSource.STANDARD_DOMAINS
            dvp_fields = []
            
            for domain_key, domain_data in standard_domains.items():
                for field in domain_data['fields']:
                    dvp_fields.append(CRFField(
                        field_name=field['name'],
                        field_label=field['label'],
                        form_name=domain_data['name'],
                        data_type=field['type'],
                        required=field.get('required', False)
                    ))
            
            generator.add_crf_fields(dvp_fields)
            generator.generate_all_rules()

            output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'DVP'}_DVP.docx"

            generator.generate_dvp_document(output_path=str(output_path))

            return str(output_path)

        except Exception as e:
            print(f"DVP生成錯誤: {e}")
            traceback.print_exc()
            return None

    # def _generate_user_guide(self) -> Optional[str]:
    #     """生成User Guide文件"""
    #     try:
    #         generator = UserGuideGenerator(
    #             api_key=self.api_key,
    #             model_name="gemini-2.5-pro"
    #         )

    #         output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'UserGuide'}_UserGuide.docx"

    #         # 使用protocol_info生成User Guide
    #         generator.generate_user_guide(
    #             protocol_info=self.protocol_info,
    #             output_path=str(output_path),
    #             logo_path=self.logo_path
    #         )

    #         return str(output_path)

    #     except Exception as e:
    #         print(f"User Guide生成錯誤: {e}")
    #         traceback.print_exc()
    #         return None

    def _generate_user_guide(self) -> Optional[str]:
        """生成User Guide文件"""
        try:
            from datetime import datetime
            from modules.crf_generator import CRFGenerator as CRFGenSource

            # 1. 準備 Protocol 資料
            protocol_data = {
                'protocol_id': self.protocol_info.protocol_number or "N/A",
                'protocol_title': self.protocol_info.study_title or "N/A",
                'sponsor': self.protocol_info.sponsor or "N/A",
                'version': "1.0",
                'date': datetime.now().strftime('%Y-%m-%d')
            }

            # 2. 準備 CRF 設計資料 (模擬)
            standard_domains = CRFGenSource.STANDARD_DOMAINS
            forms = []
            for domain_key, domain_data in standard_domains.items():
                fields = []
                for field in domain_data['fields']:
                    fields.append({
                        'field_name': field['name'],
                        'field_label': field['label'],
                        'field_type': field['type'],
                        'required': field.get('required', False),
                        'validation': field.get('coding_instruction', '')
                    })
                forms.append({
                    'form_name': domain_data['name'],
                    'form_title': domain_data['name'],
                    'visit': 'All Visits',
                    'fields': fields
                })
            
            crf_design = {'forms': forms}

            # 3. 初始化生成器 (不需要 api_key)
            generator = UserGuideGenerator(
                protocol_info=protocol_data,
                crf_design=crf_design,
                system_name="EDC System"
            )

            output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'UserGuide'}_UserGuide.docx"

            generator.generate(output_path=str(output_path))

            return str(output_path)

        except Exception as e:
            print(f"User Guide生成錯誤: {e}")
            traceback.print_exc()
            return None

    # def _generate_dmp(self) -> Optional[str]:
    #     """生成DMP文件（資料管理計劃）"""
    #     try:
    #         # DMP通常是DVP的延伸，這裡使用類似的生成器
    #         # 可以根據需要調整
    #         generator = DVPGenerator(
    #             api_key=self.api_key,
    #             model_name="gemini-2.5-pro"
    #         )

    #         output_path = self.output_dir / f"{self.protocol_info.protocol_number or 'DMP'}_DMP.docx"

    #         # 生成DMP（可以自訂模板）
    #         generator.generate_dvp(
    #             protocol_info=self.protocol_info,
    #             output_path=str(output_path),
    #             logo_path=self.logo_path
    #         )

    #         return str(output_path)

    #     except Exception as e:
    #         print(f"DMP生成錯誤: {e}")
    #         traceback.print_exc()
    #         return None


    def _generate_dmp(self) -> Optional[str]:
        """生成DMP文件"""
        # 目前暫時使用 DVP 生成邏輯，或是您可以略過此功能
        # 這裡簡單回傳 None 或實作類似 DVP 的邏輯
        print("DMP 生成功能目前使用 DVP 邏輯暫代")
        return self._generate_dvp()


    def create_interface(self):
        """創建Gradio介面"""

        # 自定義CSS
        custom_css = """
        .main-title {
            text-align: center;
            color: #2563eb;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 0.5em;
        }
        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 1.2em;
            margin-bottom: 2em;
        }
        .step-title {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            margin: 20px 0 10px 0;
        }
        .success-box {
            background-color: #dcfce7;
            border-left: 4px solid #22c55e;
            padding: 15px;
            border-radius: 4px;
        }
        .error-box {
            background-color: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 4px;
        }
        """

        with gr.Blocks(
            title="臨床試驗文件自動化系統",
            theme=gr.themes.Soft(),
            css=custom_css
        ) as interface:

            # 標題
            gr.HTML("""
                <div class="main-title">
                    🏥 臨床試驗文件自動化系統
                </div>
                <div class="subtitle">
                    Clinical Trial Document Automation System
                </div>
            """)

            # 步驟1: 設定API Key
            gr.HTML('<div class="step-title">📝 步驟 1: 設定 Gemini API Key</div>')

            with gr.Row():
                with gr.Column(scale=3):
                    api_key_input = gr.Textbox(
                        label="Gemini API Key",
                        placeholder="請輸入您的 Gemini API Key",
                        type="password",
                        info="如何取得API Key: https://makersuite.google.com/app/apikey"
                    )
                with gr.Column(scale=1):
                    api_key_btn = gr.Button("設定 API Key", variant="primary")

            api_key_status = gr.Textbox(label="狀態", interactive=False)

            # 步驟2: 上傳檔案
            gr.HTML('<div class="step-title">📁 步驟 2: 上傳檔案</div>')

            with gr.Row():
                with gr.Column():
                    pdf_file = gr.File(
                        label="Protocol PDF (必填)",
                        file_types=[".pdf"],
                        type="filepath"
                    )
                    pdf_status = gr.Textbox(label="上傳狀態", interactive=False)

                with gr.Column():
                    logo_file = gr.File(
                        label="公司 Logo (選填)",
                        file_types=[".png", ".jpg", ".jpeg"],
                        type="filepath"
                    )
                    logo_status = gr.Textbox(label="上傳狀態", interactive=False)

            # 步驟3: 解析Protocol
            gr.HTML('<div class="step-title">🔍 步驟 3: 解析 Protocol</div>')

            parse_btn = gr.Button("開始解析 Protocol", variant="primary", size="lg")
            parse_status = gr.Textbox(label="解析狀態", interactive=False)

            # Protocol資訊編輯區
            gr.HTML('<div class="step-title">✏️ 步驟 4: 編輯 Protocol 資訊（可選）</div>')

            protocol_json = gr.Code(
                label="Protocol 資訊 (JSON格式)",
                language="json",
                lines=20,
                interactive=True
            )

            with gr.Row():
                update_info_btn = gr.Button("更新資訊", variant="secondary")
                update_status = gr.Textbox(label="更新狀態", interactive=False, scale=2)

            # 步驟4: 選擇文件類型
            gr.HTML('<div class="step-title">📋 步驟 5: 選擇要生成的文件類型</div>')

            doc_type_checkboxes = gr.CheckboxGroup(
                choices=list(self.doc_types.keys()),
                label="文件類型",
                info="可多選",
                value=["CRF"]  # 預設選擇CRF
            )

            # 步驟5: 生成文件
            gr.HTML('<div class="step-title">🚀 步驟 6: 生成文件</div>')

            generate_btn = gr.Button("一鍵生成文件", variant="primary", size="lg")
            generate_status = gr.Textbox(label="生成狀態", interactive=False)

            output_files = gr.File(
                label="下載生成的文件",
                file_count="multiple",
                interactive=False
            )

            # 使用說明
            with gr.Accordion("📖 使用說明", open=False):
                gr.Markdown("""
                ## 使用步驟

                1. **設定 API Key**: 輸入您的 Gemini API Key 並點擊「設定 API Key」
                2. **上傳檔案**:
                   - 上傳 Protocol PDF（必填）
                   - 上傳公司 Logo（選填，會出現在生成的文件中）
                3. **解析 Protocol**: 點擊「開始解析 Protocol」，系統會自動提取 Protocol 中的關鍵資訊
                4. **編輯資訊**: 您可以在 JSON 編輯器中查看和修改提取的資訊
                5. **選擇文件類型**: 選擇您想要生成的文件類型
                6. **生成文件**: 點擊「一鍵生成文件」，系統會生成選定的文件
                7. **下載**: 生成完成後，點擊「下載」按鈕即可下載文件

                ## 支援的文件類型

                - **CRF (病例報告表)**: 用於收集臨床試驗資料的表單
                - **DVP (資料驗證計劃)**: 定義資料驗證規則和流程
                - **User Guide (使用者指南)**: EDC 系統使用手冊
                - **DMP (資料管理計劃)**: 資料管理策略和流程

                ## 注意事項

                - 解析 Protocol 可能需要 30-60 秒，請耐心等待
                - 生成文件的時間取決於選擇的文件數量和複雜度
                - 建議使用 Chrome 或 Edge 瀏覽器以獲得最佳體驗
                - API Key 僅用於本次會話，不會被儲存

                ## 獲取 Gemini API Key

                1. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. 使用 Google 帳號登入
                3. 點擊 "Create API Key"
                4. 複製 API Key 並貼到上方輸入框

                ## 範例 Protocol

                您可以使用自己的 Protocol PDF，或從以下來源取得範例：
                - [ClinicalTrials.gov](https://clinicaltrials.gov/)
                - [WHO ICTRP](https://www.who.int/clinical-trials-registry-platform)
                """)

            # 關於
            with gr.Accordion("ℹ️ 關於", open=False):
                gr.Markdown("""
                ## 臨床試驗文件自動化系統

                **版本**: 1.0.0
                **作者**: Clinical Data Automation Team
                **日期**: 2025-11-18

                ### 技術棧

                - **Web UI**: Gradio
                - **AI 引擎**: Google Gemini 1.5 Flash
                - **PDF 處理**: PDFPlumber
                - **文件生成**: python-docx

                ### 功能特點

                - ✅ 自動提取 Protocol 關鍵資訊
                - ✅ AI 智能分析和結構化
                - ✅ 支援多種文件類型生成
                - ✅ 可自訂 Protocol 資訊
                - ✅ 支援中英文
                - ✅ 進度實時顯示
                - ✅ 一鍵下載

                ### 授權

                此系統僅供教育和研究目的使用。

                ### 聯絡我們

                如有問題或建議，請聯繫開發團隊。
                """)

            # 綁定事件
            api_key_btn.click(
                fn=self.set_api_key,
                inputs=[api_key_input],
                outputs=[api_key_status]
            )

            pdf_file.upload(
                fn=self.upload_pdf,
                inputs=[pdf_file],
                outputs=[pdf_status, gr.State()]
            )

            logo_file.upload(
                fn=self.upload_logo,
                inputs=[logo_file],
                outputs=[logo_status]
            )

            parse_btn.click(
                fn=self.parse_protocol,
                inputs=[],
                outputs=[parse_status, protocol_json]
            )

            update_info_btn.click(
                fn=self.update_protocol_info,
                inputs=[protocol_json],
                outputs=[update_status]
            )

            generate_btn.click(
                fn=self.generate_documents,
                inputs=[doc_type_checkboxes],
                outputs=[generate_status, output_files]
            )

        return interface

    def launch(self, share=False, server_port=7860):
        """
        啟動Web介面

        Args:
            share: 是否創建公開分享連結
            server_port: 伺服器端口
        """
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_port=server_port,
            server_name="0.0.0.0",
            show_error=True
        )


def main():
    """主函數"""
    print("=" * 80)
    print("臨床試驗文件自動化系統 - Web UI")
    print("Clinical Trial Document Automation System - Web UI")
    print("=" * 80)
    print()

    # 創建並啟動Web UI
    web_ui = ClinicalDocWebUI()

    print("正在啟動 Web 介面...")
    print("啟動後請在瀏覽器中開啟顯示的網址")
    print()

    # 在Colab中自動使用share=True
    is_colab = 'google.colab' in sys.modules

    web_ui.launch(
        share=is_colab,  # Colab中自動分享
        server_port=7860
    )


if __name__ == "__main__":
    main()
