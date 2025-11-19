# 快速開始 - 3分鐘上手 🚀

恭喜！您已成功獲得完整的臨床試驗文件自動化系統。

## 🎯 選擇您的使用方式

### 方式一：Web UI（最簡單，推薦） 🌐

**適合**: 所有人，無需編程知識

```bash
# 進入專案目錄
cd clinical-doc-automation

# Windows用戶：雙擊
launch_web_ui.bat

# Mac/Linux用戶：執行
./launch_web_ui.sh

# 或手動執行
python web_interface.py
```

瀏覽器會自動開啟 http://localhost:7860

**3個步驟完成**:
1. 設定Gemini API Key（免費取得：https://makersuite.google.com/app/apikey）
2. 上傳Protocol PDF
3. 點擊「一鍵生成所有文件」

⏱️ **時間**: 約5分鐘

📖 **詳細教學**: `WEB_UI_QUICKSTART.md`

---

### 方式二：Google Colab（雲端運行） ☁️

**適合**: 想在雲端運行，不想安裝軟體

1. 訪問 https://colab.research.google.com/
2. 上傳 `Clinical_Trial_Document_Automation_System.ipynb`
3. 上傳 `modules/` 資料夾
4. 執行Section 1-2（安裝）
5. 執行Section 8（一鍵生成）

⏱️ **時間**: 約5分鐘

📖 **詳細教學**: `NOTEBOOK_QUICK_START.md`

---

### 方式三：命令列（自動化） 💻

**適合**: 開發者，需要批次處理

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定API Key
export GEMINI_API_KEY="your-api-key-here"

# 3. 執行
python automation_workflow.py --protocol your_protocol.pdf

# 批次處理
python automation_workflow.py --batch p1.pdf p2.pdf p3.pdf
```

⏱️ **時間**: 每個Protocol約3-5分鐘

📖 **詳細教學**: `QUICKSTART_AUTOMATION.md`

---

## 📚 完整文檔導航

| 需求 | 文檔 |
|------|------|
| 🚀 快速開始（3分鐘） | `WEB_UI_QUICKSTART.md` |
| 📖 完整功能說明 | `README.md` |
| 💻 安裝指南 | `INSTALLATION_GUIDE.md` |
| 📊 專案總結 | `PROJECT_SUMMARY.md` |
| ✅ 交付清單 | `FINAL_DELIVERY_CHECKLIST.md` |

---

## 💡 第一次使用建議

1. **先閱讀** `WEB_UI_QUICKSTART.md`（5分鐘）
2. **取得API Key**: https://makersuite.google.com/app/apikey（免費）
3. **準備Protocol PDF**（確保是文字版，非掃描版）
4. **啟動Web UI**，跟著介面指示操作
5. **生成第一份文件**，查看效果
6. **閱讀完整文檔**，了解更多功能

---

## 🆘 遇到問題？

1. **執行測試**: `python test_installation.py`
2. **查看FAQ**: `README.md` 的「常見問題」章節
3. **查看日誌**: `automation.log`
4. **參考範例**: `examples/` 資料夾

---

## 🎉 開始您的文件自動化之旅！

**現在就開始**:
```bash
python web_interface.py
```

**祝您使用順利！** 🚀
