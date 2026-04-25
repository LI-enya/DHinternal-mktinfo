# DHinternal MktInfo — 维护手册

> 本文档记录仪表盘的核心结构、设计系统、常见维护场景。
> 改动 UI / 加 section / 改色之前先看一遍。

---

## 1. 文件结构

| 文件 | 用途 |
|---|---|
| `index.html` | 主仪表盘（HTML + CSS + JS 单文件） |
| `data.json` | 每日更新数据（按日期 entry）|
| `brands.json` | 永久参考的品牌列表（Primary + Reference + AI 拓展） |
| `WORKFLOW.md` | 数据更新工作流说明 |
| `MAINTAINING.md` | 本文件 |
| `scripts/export_brands.py` | brands.json → 品牌资料库 Excel 输出 |
| `_品牌资料库/IO-ISOLE/` / `_品牌资料库/LA-Laise/` | 各品牌竞品 Excel |

---

## 2. 设计系统

### 2.1 颜色（所有颜色集中在 `:root` ~line 12-50）

| CSS 变量 | 值 | 用途 |
|---|---|---|
| `--accent` | `#C9A77A` | 香槟金（主强调色，统一）|
| `--accent-deep` | `#A8895C` | 深香槟（hover / kicker 文字）|
| `--accent-soft` | `#E7C89C` | 浅香槟（装饰）|
| `--text` | `#1A1A1A` | 主文字（黑）|
| `--text-light` | `#6A6A6A` | 次要文字 |
| `--signal` | `#A88EA0` | 雾紫（HOT / NEW 信号）|
| `--decor` | `#A88EA0` | 装饰雾紫 |
| `--bg` | `#F4F4F4` | 浅背景 |
| `--card` | `#FFFFFF` | 卡片纯白 |
| `--zone-dark` | `#0A0A0A` | 暗区背景（SNS / Brand List）|

**改色** → 只改 `:root` 一处即可全局生效。

### 2.2 字号系统（雑誌風タイポ）

| Tier | px | Font | 用途 |
|---|---|---|---|
| **Display** | `clamp(64px, 11vw, 168px)` | Playfair italic UPPERCASE | section headline (Calendar / Topics / etc.) |
| **Stat number** | `clamp(56px, 6.8vw, 124px)` | Playfair italic | By the Numbers 数字 |
| **Lead** | 19-22 | Noto Sans JP 600 | topic-title / competitor-move |
| **Body** | 16-17 | Noto Sans JP 400 | 描述文 |
| **Caption** | 13 | Noto Sans JP 400 | 次要、source |
| **Kicker** | 11-12 | Noto Sans JP 700 + UPPERCASE +letter-spacing 0.22-0.32em | label |

### 2.3 字体（Google Fonts 头部 link）

- **Noto Sans JP** (400, 500, 600, 700) — 主文 JP / 中
- **Playfair Display** (400, 500, 600, italic) — display / italic 装饰

### 2.4 雑誌レイアウトパターン

每个 section 用统一模板：

```html
<div class="section" id="xxxSection">
    <div class="section-header-mag">
        <div class="kicker">No. XX · Section Label</div>
        <div class="section-title section-title--display">English Headline</div>
        <div class="section-headline-jp">日本語タイトル<span class="meta">— サブ説明</span></div>
    </div>
    <!-- 内容 -->
</div>
```

---

## 3. Icon 系统（重要：混合 emoji + SVG）

按场景严格区分：

| 场景 | 方式 | 例 | 理由 |
|---|---|---|---|
| **Filter / Tab / Nav**（功能性 UI）| SVG outline (currentColor) | `<svg class="icon"><use href="#i-bag"/></svg>` | 编辑统一感 |
| **Content**（card / stat / tag / 描述文）| Emoji | 👝 👠 🔥 ⭐ 🆕 | 视觉识别度 |

### 3.1 SVG 库（`index.html` body 顶部 `<svg style="display:none"><defs>...</defs></svg>`）

现有 16 个 symbol：

| ID | 用途 |
|---|---|
| `i-calendar` | 日历 |
| `i-social` | 聊天/SNS |
| `i-flame` (filled) | 火焰（信号色继承）|
| `i-search` | 搜索 |
| `i-bag` | 购物袋 |
| `i-shoe` | 高跟鞋 |
| `i-book` | 书 |
| `i-chart` | 柱状图 |
| `i-folder` | 文件夹 |
| `i-globe` | 地球 |
| `i-store` | 店铺 |
| `i-star` (filled) | 星 |
| `i-sparkle` | 闪光 |
| `i-warning` | 警告 |
| `i-x` | 关闭 |
| `i-arrow-up` | 上箭头 |

### 3.2 新增 SVG icon

1. 在 `<defs>` 内加：
   ```html
   <symbol id="i-newname" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
     <!-- path here -->
   </symbol>
   ```
2. 引用：HTML 内 `<svg class="icon"><use href="#i-newname"/></svg>`、JS 内 `${icon('i-newname')}`

### 3.3 JS 中的 icon helper

`<script>` 顶部已定义：

```js
function icon(name) { return `<svg class="icon"><use href="#${name}"/></svg>`; }
```

JS 模板内用 `${icon('i-bag')}`，比手写 `<svg class="icon"><use href="#i-bag"/></svg>` 简洁、不易写错。

---

## 4. 添加新 section 步骤

1. **HTML** 加 section 块（按 §2.4 模板）
2. **JS** `renderSectionIndex()` (~line 1235) 添加 nav 入口：
   ```js
   { id: 'newSection', icon: icon('i-newicon'), label: '日本語ラベル', count: someCount }
   ```
3. **CSS**（如需 dark zone）加：
   ```css
   #newSection { background: var(--zone-dark); color: #EFE7D3; }
   #snsSection, #brandListSection, #newSection { /* dark zone overrides */ }
   ```
4. **Mobile** breakpoint（~line 605, 617）如有自定义 styling 同步

---

## 5. 数据更新流程

### 自动（每 3 日）
`~/.claude/scheduled-tasks/daily-mktinfo-update/SKILL.md` 定义规则：
- WebSearch 获取最新 SNS 话题 / 竞品动向 / 活动信息
- 写入 `data.json` 顶部新日期 entry
- git commit + push → GitHub Pages 自动部署

### 手动
直接编辑 `data.json`，commit push 即可。

---

## 6. 部署

- GitHub Pages 自动部署（`.github/workflows/pages.yml`）
- main 分支 push 后 1-2 分钟生效
- URL: https://li-enya.github.io/DHinternal-mktinfo/

---

## 7. 常见维护场景

| 场景 | 操作 |
|---|---|
| 改 accent 色 | `:root` 内 `--accent` 改 1 处 |
| 改 section 标题 | HTML 内 `.kicker` / `.section-title--display` / `.section-headline-jp` |
| 加 emoji 图标 | 直接在 HTML / JS 写 emoji，无 CSS 工作 |
| 加 SVG 图标 | §3.2 步骤 |
| 调字号 | 找对应 CSS 类（`.section-title--display` 等），mobile 断点同步 |
| 加 section | §4 |
| 改 dark zone 色 | `#snsSection, #brandListSection { ... }` 块内 |

---

## 8. 注意事项

- **`!important` 慎用** — 现状只在 `.competitor-card.is-primary { border-left-color: var(--text) !important; }` 1 处。新加的话先尝试提升 specificity
- **emoji 在不同 OS 显示略有差异**（Win / Mac / iOS） — 已选用普及度高的 👝 👠 🔥 ⭐
- **章节番号 `No. 01` ~ `No. 07`** 在 HTML 直接写死。重排时手动改 7 处
- **clamp() 字号** — 大屏自动放大、小屏自动缩小，无需写多个 mobile 规则
