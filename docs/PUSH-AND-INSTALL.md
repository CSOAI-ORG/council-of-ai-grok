# Push + install (owner machine)

The Grok session that generated this pack could **read** `CSOAI-ORG` but could not create repositories or commits (GitHub 403). Do this locally.

## 1. Dedicated plugin repo (recommended)

```bash
cd council-of-ai-grok
git init
git add .
git commit -m "v0.1.0 Grok Build plugin — measurement, never certification"
gh repo create CSOAI-ORG/council-of-ai-grok --public --source=. --remote=origin --push
git ls-remote origin HEAD
```

Paste the SHA into `docs/MARKETPLACE-PR.md`.

## 2. Also land doctrine on the monorepo

```bash
git clone -b master https://github.com/CSOAI-ORG/councilof-ai.git
cp GROK.md /path/to/councilof-ai/GROK.md
cp docs/ALIGNMENT-GROK-ADDENDUM.md /path/to/councilof-ai/docs/
# append addendum into ALIGNMENT.md
```

## 3. Flip default branch

```bash
gh repo edit CSOAI-ORG/councilof-ai --default-branch master
```

## 4. Local Grok TUI

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
mkdir -p ~/.grok/plugins
cp -R council-of-ai-grok ~/.grok/plugins/council-of-ai
grok inspect
grok
# then /council
```
