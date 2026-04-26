# DHinternal MktInfo 操作手册

> 「想改某个东西的时候我该干什么」的速查手册。
> 想看技术细节请看 `SKILL.md`（在 `~/.claude/scheduled-tasks/daily-mktinfo-update/`）。

---

## 📍 三个核心文件

| 文件 | 谁动它 | 用途 |
|---|---|---|
| `brands.json` | **CEO 自己改** | 竞品列表 + 品牌定位 |
| `data.json` | Claude 自动写 | 实际数据（每周日 / 周四 18:00 JST 更新）|
| `index.html` | Claude 改（让 Claude 改） | 页面骨架（极少改）|

> **原则**：你直接编辑 `brands.json` 即可，剩下的 Claude 都能搞定。

---

## 🎯 我想 ... 该怎么办

### ① 加一个新竞品

```
1. 打开 brands.json
2. 找正确的位置（参照下表）
3. 复制一个已有 entry，改成新品牌
4. 跑：cd 市场调研/DHinternal-mktinfo && python scripts/export_brands.py
5. 检查 Excel（_品牌资料库/{IO-ISOLE,LA-Laise}/竞争对手列表.xlsx）
6. git add brands.json 竞争对手列表.xlsx
7. git commit -m "brands: 加 XXX" && git push
```

**位置选择速查表**：

| 你的竞品是... | 放在哪里 | tier 字段填 |
|---|---|---|
| CEO 钦定，每次必爬 | `{bag/shoe}.primary` | `core` 或 `price-aligned` |
| CEO 提供的参考类（调性近的） | `{bag/shoe}.reference.seed` | `tone-aligned` |
| CEO 提供的参考类（市场动向） | `{bag/shoe}.reference.seed` | `trend-watch` |
| CEO 提供的参考类（看活动促销） | `{bag/shoe}.reference.seed` | `activity-watch` |
| Claude 推荐的（你接受了） | `{bag/shoe}.reference.aiSuggested` | 同上三选一 |

**最小可行 entry**：
```json
{
  "name": "ブランド名",
  "tier": "tone-aligned",
  "reason": "为什么加它，50字以内",
  "officialUrl": "https://..."
}
```

如果嫌麻烦，**直接告诉 Claude**："加 XXX 到 ISOLÉ 的调性对，URL 是 https://..."，Claude 会自动:
- 验证 URL 真实性
- 写进 brands.json 正确位置
- 跑 export 脚本
- commit + push

---

### ② 删除一个竞品

直接编辑 `brands.json`，删掉那条 entry，然后：
```bash
python scripts/export_brands.py
git add brands.json scripts/feishu_*.txt 竞争对手列表.xlsx 路径
git commit -m "brands: 移除 XXX" && git push
```

或直接告诉 Claude："从 brands.json 删掉 XXX"。

---

### ③ 改 ISOLÉ / l'aisé 的定位描述

编辑 `brands.json` 的 `ourBrands` 数组，改对应品牌的 `positioning` 字段。

需要修改的常见点：
- `tone`（调性关键词数组）
- `avoid`（避忌关键词）
- `coreProducts`（核心产品线）
- `categoryEmphasis.current`（**仅 l'aisé**：当前主打的类目，目前是 `"dress shoes"`）

**改完不需要重新跑脚本**，下次定时任务自动读新版。

---

### ④ 改 dress shoes 强化方向（l'aisé 专属）

如果某天想把 l'aisé 的强化重点从 `dress shoes` 换成比如 `loafer`：

```json
"categoryEmphasis": {
  "current": "loafer",
  "_note": "..."
}
```

下次 Claude 跑 WebSearch 时会自动用 `loafer` 关键词检索。

---

### ⑤ 改自动更新频率

当前是 **每周日 + 周四 18:00 JST**（cron `0 18 * * 0,4`），对应团队周一 + 周五早上 review 的前一晚。

**告诉 Claude**：「把 daily-mktinfo-update 改成每天/每周/每 N 天」，他会用 `mcp__scheduled-tasks__update_scheduled_task` 工具改。

---

### ⑥ 手动立刻更新一次（不等定时）

**告诉 Claude**：「手动跑一次 daily-mktinfo-update，按 SKILL.md 走完整流程」。

---

### ⑦ 重新生成 Excel + 飞书文本

任何时候改完 `brands.json` 后：

```bash
cd "C:/Users/blcu1/Desktop/AI/市场调研/DHinternal-mktinfo"
python scripts/export_brands.py
```

输出：
- `_品牌资料库/IO-ISOLE/竞争对手列表.xlsx`
- `_品牌资料库/LA-Laise/竞争对手列表.xlsx`
- `scripts/feishu_io.txt`（飞书文本，供复制）
- `scripts/feishu_la.txt`（同上）

直接控制台也会打印一份飞书文本，方便复制。

---

### ⑧ 把网页分享给别人

链接是固定的：**https://li-enya.github.io/DHinternal-mktinfo/**

只要 GitHub 仓库 `LI-enya/DHinternal-mktinfo` 不删，链接永远有效。无需登录。

---

## ⚠️ 出问题时

### 🔴 飞书收到「[Claude] DH-mktinfo 更新失敗」紫色日历提醒

意味着自动更新失败了。

**第一步**：把日历事件的 description 截屏发给 Claude，他会读出失败原因（哪个 ガードレール 触发的）。

**常见原因 → 怎么办**：

| 失败原因 | 应对 |
|---|---|
| G0: bag primary ヒット数 < 3 | 多半是某个 primary 品牌官网/新闻最近没新内容。可以等下次更新。如果连续2-3次都失败，检查 brands.json 里那几个品牌 URL 是否还活着 |
| G2: 重复度 > 70% | 信号是这几天市场太"安静"，Claude 找不到足够的新动向。可以等下次更新 |
| G3: URL 大量失效 | 某些品牌官网改版了。让 Claude 检查 brands.json 里的 URL 列表 |

**手动重试**：让 Claude 重跑一次 SKILL.md。

---

### 🟡 网页能开但数据看着不对（错误/缺失）

让 Claude 看一下：
1. `data.json` 第一条 entry 的内容
2. 浏览器 console 有没有 JS 报错

99% 的情况是 `data.json` 写坏了或 schema 不对。让 Claude 修。

---

### 🔴 网页打不开（404 / 空白页）

可能性：
1. **GitHub Pages 部署延迟**：push 后 1-2 分钟才生效，等等就好
2. **HTML 写坏了**：让 Claude `git revert` 最近一次 index.html 的改动

---

## 📦 完整文件清单

```
DHinternal-mktinfo/                          # GitHub 仓库
├── index.html                ← 页面骨架（极少改）
├── data.json                 ← 数据（每周日/周四 18:00 JST Claude 自动更新）
├── brands.json               ← 竞品列表 + 品牌定位（CEO 主要编辑这个）
├── WORKFLOW.md               ← 本文
├── .github/workflows/
│   └── pages.yml             ← GitHub Pages 自动部署（不用动）
├── .gitignore
└── scripts/
    ├── export_brands.py      ← 重新生成 Excel + 飞书文本
    ├── feishu_io.txt         ← 最新飞书文本（自动生成）
    └── feishu_la.txt         ← 同上

~/.claude/scheduled-tasks/daily-mktinfo-update/
└── SKILL.md                  ← Claude 自动更新时读的指令（一般不用动）

_品牌资料库/
├── IO-ISOLE/
│   └── 竞争对手列表.xlsx     ← export_brands.py 自动生成
└── LA-Laise/
    └── 竞争对手列表.xlsx     ← 同上
```

---

## 🤝 一句话总结

**95% 的场景**：

> 改 `brands.json` → 跑 `python scripts/export_brands.py` → `git commit && push`

或者更省事：

> 直接告诉 Claude 你要改什么。
