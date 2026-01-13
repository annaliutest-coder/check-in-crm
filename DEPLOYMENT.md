# Zeabur 部署指南

本文檔提供將 CRM 快速打卡系統部署到 Zeabur 平台的完整步驟。

## 📋 部署前準備

### 1. 確認 GitHub 倉庫

確保所有代碼已推送到 GitHub 倉庫：

```bash
git add .
git commit -m "準備 Zeabur 部署"
git push origin main
```

### 2. 準備環境變數

需要準備以下環境變數的值：

**必填**：
- `EVENT_NAME`：活動名稱（例如：`2026春季招生活動`）

**選填（郵件功能）**：
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`
- `GMAIL_USER`

> **提示**：如果暫時不需要郵件功能，可以先跳過 Gmail 相關變數，系統仍可正常運行（只是無法發送郵件）。

## 🚀 部署步驟

### 步驟 1：登入 Zeabur

1. 訪問 [Zeabur](https://zeabur.com)
2. 使用 GitHub 帳號登入

### 步驟 2：創建新專案

1. 點擊 **"Create Project"** 或 **"New Project"**
2. 選擇一個區域（建議選擇 **Asia (Tokyo)** 或 **Asia (Singapore)**）
3. 為專案命名（例如：`crm-checkin-system`）

### 步驟 3：添加 PostgreSQL 資料庫

1. 在專案頁面中，點擊 **"Add Service"**
2. 選擇 **"Database"** → **"PostgreSQL"**
3. Zeabur 會自動創建 PostgreSQL 實例並生成 `DATABASE_URL` 環境變數

### 步驟 4：部署應用

1. 點擊 **"Add Service"** → **"Git"**
2. 選擇你的 GitHub 倉庫（可能需要授權 Zeabur 訪問）
3. 選擇正確的分支（通常是 `main` 或 `master`）
4. Zeabur 會自動偵測這是一個 Python 專案

### 步驟 5：配置環境變數

1. 點擊應用服務卡片
2. 進入 **"Variables"** 或 **"Environment Variables"** 標籤
3. 添加以下環境變數：

```
EVENT_NAME=2026春季招生活動
```

如需啟用郵件功能，繼續添加：

```
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REFRESH_TOKEN=your-refresh-token
GMAIL_USER=your-email@gmail.com
```

4. 點擊 **"Save"** 或 **"Confirm"**

### 步驟 6：等待部署完成

1. Zeabur 會自動執行以下步驟：
   - 安裝依賴（`requirements.txt`）
   - 執行啟動腳本（`start.sh`）：
     - 生成 Prisma Client
     - 創建資料庫表結構
     - 啟動 FastAPI 應用
2. 部署過程約需 2-5 分鐘
3. 部署完成後，狀態會顯示為 **"Running"**

### 步驟 7：配置域名（選用）

1. 在應用服務卡片中，找到 **"Networking"** 或 **"Domain"** 設定
2. Zeabur 會自動生成一個域名（例如：`your-app.zeabur.app`）
3. 也可以綁定自訂域名

## ✅ 部署驗證

### 1. 訪問應用

打開 Zeabur 提供的域名，應該看到打卡介面。

### 2. 測試打卡功能

1. 在打卡頁面輸入 Email
2. 點擊「打卡」按鈕
3. 應該看到成功訊息

### 3. 檢查儀表板

訪問 `your-domain.zeabur.app/dashboard`，確認：
- 可以看到剛剛打卡的用戶
- 統計數據正確顯示

### 4. 測試排程系統

訪問 `your-domain.zeabur.app/scheduler`，確認頁面正常顯示。

## 🔧 常見問題

### Q1: 部署失敗，顯示 "Prisma generate failed"

**解決方法**：
- 確認 `requirements.txt` 包含 `prisma>=0.15.0`
- 檢查 `start.sh` 是否有執行權限（應該自動處理）
- 查看 Zeabur 的部署日誌，確認錯誤訊息

### Q2: 資料庫連線錯誤

**解決方法**：
- 確認 PostgreSQL 服務已正確添加
- 檢查應用是否能訪問 `DATABASE_URL` 環境變數
- 在 Zeabur 專案中，確保 PostgreSQL 和應用在同一個專案內

### Q3: 郵件發送失敗

**解決方法**：
- 如果不需要郵件功能，可以暫時在打卡時不勾選「寄送歡迎郵件」
- 檢查 Gmail API 憑證是否正確設定
- 確認 Refresh Token 是否過期

### Q4: 靜態文件（CSS/JS）無法載入

**解決方法**：
- 檢查 `main.py` 中的靜態文件掛載是否正確：
  ```python
  app.mount("/static", StaticFiles(directory="static"), name="static")
  ```
- 確認 `static` 和 `templates` 目錄已推送到 GitHub

### Q5: 部署後修改代碼如何更新？

**解決方法**：
1. 推送代碼到 GitHub：
   ```bash
   git add .
   git commit -m "更新功能"
   git push
   ```
2. Zeabur 會自動偵測並重新部署（如已啟用自動部署）
3. 或手動在 Zeabur 專案中點擊 **"Redeploy"**

## 📊 監控與日誌

### 查看應用日誌

1. 在 Zeabur 專案中，點擊應用服務卡片
2. 進入 **"Logs"** 標籤
3. 可以看到即時日誌輸出，包括：
   - Prisma 生成過程
   - 資料庫遷移日誌
   - FastAPI 啟動訊息
   - API 請求日誌

### 監控資料庫

1. 點擊 PostgreSQL 服務卡片
2. 可以查看：
   - 連線數
   - 儲存空間使用量
   - 資料庫效能指標

## 🔄 回滾部署

如果新版本有問題，可以回滾到之前的版本：

1. 在 Zeabur 應用服務中，找到 **"Deployments"** 或 **"History"**
2. 選擇之前成功的部署版本
3. 點擊 **"Rollback"** 或 **"Redeploy"**

## 📝 環境變數完整清單

```env
# 必填
DATABASE_URL=postgresql://user:pass@host:5432/db  # Zeabur 自動提供

# 應用配置
EVENT_NAME=2026春季招生活動

# 郵件功能（選填）
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REFRESH_TOKEN=your-refresh-token
GMAIL_USER=your-email@gmail.com
```

## 🎉 部署完成

恭喜！你的 CRM 快速打卡系統已成功部署到 Zeabur。

如有任何問題，請參考：
- [Zeabur 官方文檔](https://zeabur.com/docs)
- [Prisma 文檔](https://www.prisma.io/docs)
- [FastAPI 文檔](https://fastapi.tiangolo.com)
