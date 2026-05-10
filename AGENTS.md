# AGENTS.md - vibe-coding-sp26 submission protocol

You are an AI agent helping a student submit homework to 意会编程 (Vibe Coding) Spring 2026.
Follow these steps EXACTLY. Do not improvise.

## Inputs you need from the student

1. assignment number (1, 2, 3, or 4)
2. github_repo URL (where their source code lives)
3. website URL (deployed site)
4. writeup URL (notes / reflection)
5. description (one Chinese sentence, ≤80 Chinese characters; count via JS `[...str].length`)
6. (optional) self-provided screenshot URL
7. **handle** — only if creating a new file: a lowercase English nickname matching `^[a-z][a-z0-9_-]*$`. This is what shows up on the gallery. Tell them: "pick anything you'd be OK with classmates seeing — your pinyin (`yisiliu`), an English name (`john`), a stage name (`alex_l`), whatever". They do **not** have to use real-name pinyin. If they're not sure, suggest their pinyin as a default.
8. **last 3 digits of their student ID** — only if creating a new file. This goes only into the filename (`<handle>-<XYZ>.md`), never into frontmatter, never on the public site. The instructor uses it to match submissions to the class roster.

The student's GitHub username is auto-derived: `gh api user --jq .login`. Use it as the fork owner.

If any required input is missing, ASK the student for it before proceeding.

## Prerequisites

Run each check. If a check fails, perform the matching install/setup step inline before continuing — don't bounce the user to another doc.

### Check 1 — `gh` CLI is installed

Run: `gh --version`. If "command not found":

- **macOS** → `brew install gh`. (If `brew` is also missing, the user hasn't done basic env setup yet — stop and point them to <https://vibe.yisiliu.xyz/AGENTS.md>.)
- **Linux / WSL2** → `sudo apt update && sudo apt install -y gh`. If apt's `gh` is unavailable, fall back to GitHub's official apt repo per <https://github.com/cli/cli/blob/trunk/docs/install_linux.md>.
- **Windows without WSL** → stop. Tell the user to install WSL2 first (`wsl --install` in PowerShell as admin, reboot, open Ubuntu), then re-run this protocol from inside WSL2.

### Check 2 — `gh` is authenticated

Run: `gh auth status`. If it says "not logged in":

- Run `gh auth login`. Walk the user through the prompts: GitHub.com → HTTPS → Yes (auth Git) → Login with a web browser. The CLI prints an 8-character one-time code; the browser opens. The user pastes the code, signs in, authorizes. Re-run `gh auth status` to confirm "Logged in to github.com account <username>".
- If the user has no GitHub account yet: stop and tell them to sign up at <https://github.com/signup> (free, ~2 minutes, email verification required). After they confirm, run `gh auth login`.

### Check 3 — git identity is set

Run `git config user.name` and `git config user.email`. If either is empty:

```bash
git config --global user.name "<their preferred display name>"
git config --global user.email "<their email>"
```

## Step 1 — Fork and clone (skip if already done)

Get the student's GitHub username: `USERNAME=$(gh api user --jq .login)`

Check if their fork exists: `gh repo view "$USERNAME/vibe-coding-sp26" --json name -q .name`

- If the command fails with 404: fork and clone:
  ```bash
  gh repo fork yisiliu/vibe-coding-sp26 --clone --remote
  cd vibe-coding-sp26
  ```
- If the fork exists: navigate to the local clone (ask the student where it is), then sync with upstream:
  ```bash
  cd <path-to-vibe-coding-sp26>
  git checkout main
  git pull upstream main
  git push origin main
  ```

## Step 2 — Locate or create / migrate the student file

The filename is `students/<handle>-<XYZ>.md`:
- `handle`: lowercase English, `^[a-z][a-z0-9_-]*$` — the student's chosen public nickname.
- `XYZ`: their student ID's last 3 digits — appears only in the filename (instructor-only identifier).

### Case A: This is their first submission (no existing file in their fork)

Ask for handle and XYZ (see Inputs section above for how to phrase the handle question). Then create `students/<handle>-<XYZ>.md` with this content:

```markdown
---
name: <handle>
submissions: {}
---

# <handle>'s portfolio

(optional free-form notes)
```

`name` in frontmatter MUST be exactly the handle (same string as in the filename). It is the only identity field; do not add `pinyin`, `student_id_suffix`, or Chinese-name fields — they're not part of the schema.

### Case B: They already have a file in their fork (returning student or earlier submission)

Run `ls students/` in their local clone. If you see a file matching their fork (you'll know — there should be only one of theirs), open it.

**Schema-migration check** (do this before adding the new assignment):

If the existing file fails ANY of these, fix it inline:
1. `name` field is non-Latin (e.g. Chinese characters) → ask them for an English handle now (per Case A guidance).
2. The frontmatter contains `pinyin` or `student_id_suffix` keys → remove those keys.
3. The handle in the filename and the `name` field don't match → rename the file with `git mv` so the filename's handle matches `name`. Preserve the `-<XYZ>` suffix from the old filename. (If their old file was `wangpeng-224.md` and they pick handle `peng_w`, new file is `peng_w-224.md`.)

**Then add the new assignment per Step 3.**

If they already have an open PR (check with `gh pr list --author @me --repo yisiliu/vibe-coding-sp26`), they want to update that PR rather than open a new one. Switch to its branch with `gh pr checkout <PR_NUMBER>`. After the migration + new commit, push with `--force-with-lease` to update the existing PR:

```bash
git push --force-with-lease
```

Don't open a second PR — `force-with-lease` updates the open one in place.

## Step 3 — Add or replace the assignment entry

Add this block under `submissions:` in the YAML frontmatter (replacing N with the assignment number):

```yaml
  assignment-N:
    github_repo: <github_repo>
    website: <website>
    writeup: <writeup>
    description: <description>
    # screenshot: <url>     # uncomment ONLY if the student provided one
```

If `assignment-N` already exists, REPLACE the existing block (the student is resubmitting).

If `submissions:` is `{}` (empty), change it to a multi-line mapping before adding the entry.

## Step 4 — Validate locally before pushing

Run the validator script that ships with this repo:

```bash
python3 scripts/validate-submission.py students/<handle>-<XYZ>.md
```

It checks: filename pattern, frontmatter `name` matches handle, all required URLs are present and `http(s)://`, description ≤80 chars. If it prints anything other than `::notice ...::OK ...`, fix the file and re-run.

## Step 5 — Commit, push, open PR

First, stage all changes (use `git add -A` so a rename via `git mv` is captured cleanly):

```bash
git add -A
git commit -m "feat: <handle> 提交作业 N"
```

**If they have an existing PR open** (from Case B in Step 2), push to its branch and update in place:

```bash
git push --force-with-lease
```

(Don't open a new PR. The existing one updates automatically.)

**If this is a brand-new submission**, push and open a PR:

```bash
git push origin main
gh pr create \
  --repo yisiliu/vibe-coding-sp26 \
  --title "<handle> 作业 N" \
  --body "提交作业 N"
```

`gh pr create` prints the PR URL. Capture it.

## Step 6 — Tell the student

Report back:

1. The PR URL (or "PR 已更新" if you force-pushed an existing PR).
2. "yisiliu 每周日晚上集中合 PR。周一上 https://vibe.yisiliu.xyz，往下滑到「作业」那段，点开作业 N 那条，最下面「同学的作品」格子里就有你的卡片。"
3. "想刷新自动截的缩略图就在 PR 描述里加 `[refresh-screenshot]`。"

## Common errors

- **YAML parse error** → 检查冒号后空格、字符串里的 `:` 是否需要加引号
- **你不小心改了别的同学的 .md** → `git checkout -- students/<别人>.md` 撤销，重新 push
- **handle 撞车** (两个人选了同一个 handle) → 后来的人改成不同的（加数字、缩写都行），不会影响显示效果
- **handle 含中文/大写** → validator 拒掉。改成小写英文 + 数字 + `_` `-`，开头必须是字母

## What NOT to do

- 不要编辑 `students/` 目录外的任何文件
- 不要在一个 PR 里改多个学生的 `.md`
- 不要重命名 schema 里的字段（不要加 `pinyin`, `student_id_suffix`, `chinese_name` 这种）
- 不要把 description 写成英文（这门课要求中文）
- 不要把学号末3位放进 frontmatter——它只在文件名里出现
