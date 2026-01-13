# CRM 學生快速打卡系統

一個基於 FastAPI + Prisma 的快速活動打卡系統，專為華語文教學系國際與文化組設計，適合在 iPad 等平板設備上使用。

## 🚀 功能特色

- **快速打卡介面**：支援 Email 快速打卡，自動建立/更新用戶資料
- **用戶管理**：追蹤用戶參與的活動標籤
- **儀表板**：即時查看統計數據、用戶列表
- **CSV 匯出**：支援依標籤篩選並匯出用戶資料
- **郵件系統**：
  - 打卡時發送歡迎郵件（Gmail API）
  - 排程郵件：可針對特定標籤的用戶群發送定時郵件
- **QR Code 模擬**：支援模擬 QR Code 掃描功能

## 📋 系統需求

- Python 3.11+
- PostgreSQL（生產環境）或 SQLite（本地開發）
- Gmail API 憑證（選用，用於郵件功能）

## 🛠️ 本地開發

### 1. 克隆專案

```bash
git clone <your-repo-url>
cd check-in-crm
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

複製 `.env.example` 到 `.env` 並填入相關資訊：

```bash
cp .env.example .env
```

編輯 `.env`：

```env
# 本地開發可使用 SQLite
DATABASE_URL="file:./dev.db"

# 活動名稱
EVENT_NAME="2026春季招生活動"

# Gmail API（選用）
GMAIL_CLIENT_ID="your-client-id"
GMAIL_CLIENT_SECRET="your-client-secret"
GMAIL_REFRESH_TOKEN="your-refresh-token"
GMAIL_USER="your-email@gmail.com"
```

> **注意**：本地開發時需要暫時修改 `prisma/schema.prisma` 的 datasource 為 SQLite：
> ```prisma
> datasource db {
>   provider = "sqlite"
>   url      = "file:./dev.db"
> }
> ```

### 4. 初始化資料庫

```bash
prisma generate
prisma db push
```

### 5. 啟動開發服務器

```bash
uvicorn main:app --reload
```

訪問 http://localhost:8000

## 📦 部署到 Zeabur

詳細部署步驟請參閱 [DEPLOYMENT.md](./DEPLOYMENT.md)

### 快速步驟

1. **推送到 GitHub**
2. **在 Zeabur 創建專案並連接倉庫**
3. **添加 PostgreSQL 服務**
4. **設定環境變數**：
   - `EVENT_NAME`
   - （選用）Gmail API 相關變數
5. **部署完成**

Zeabur 會自動執行 `start.sh` 腳本，包含資料庫初始化和應用啟動。

## 📱 頁面說明

- **`/`** - 打卡介面（Kiosk 模式）
- **`/dashboard`** - 儀表板（用戶管理、統計、匯出）
- **`/scheduler`** - 排程郵件管理

## 🔧 技術架構

- **後端框架**：FastAPI
- **ORM**：Prisma (Python)
- **資料庫**：PostgreSQL (生產) / SQLite (開發)
- **郵件服務**：Gmail API
- **排程系統**：APScheduler
- **前端**：HTML + Tailwind CSS + Vanilla JavaScript

## 📝 環境變數說明

| 變數名稱 | 說明 | 必填 | 預設值 |
|---------|------|-----|-------|
| `DATABASE_URL` | PostgreSQL 連線字串 | 是（Zeabur 自動提供） | - |
| `EVENT_NAME` | 當前活動名稱 | 否 | `2026春季招生活動` |
| `GMAIL_CLIENT_ID` | Gmail OAuth Client ID | 否 | - |
| `GMAIL_CLIENT_SECRET` | Gmail OAuth Client Secret | 否 | - |
| `GMAIL_REFRESH_TOKEN` | Gmail OAuth Refresh Token | 否 | - |
| `GMAIL_USER` | 發送郵件的 Gmail 地址 | 否 | - |

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📄 授權

MIT License
