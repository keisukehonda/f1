#!/usr/bin/env bash
# 2-space indent に合わせています

OWNER="keisukehonda"
REPO="f1"
TITLE="KG Roadmap"

echo "▶︎ Creating project \"$TITLE\"..."
PROJECT_JSON=$(gh project create --title "$TITLE" --owner "$OWNER" --format json) || exit 1
NUMBER=$(echo "$PROJECT_JSON" | jq -r '.number')
echo "✅  Project $NUMBER created"

echo "▶︎ Adding custom fields..."
create_field () {
  gh project field-create "$NUMBER" \
      --owner "$OWNER" \
      --name "$1" \
      --data-type "SINGLE_SELECT" \
      --single-select-options "$2"
}
create_field "Phase"     "P0 PoC,P1 MultiLaw,P2 Query API,P3 Viz,P4 GNN"
create_field "Component" "Loader,Schema,Build,Query"
create_field "Priority"  "High,Normal,Low"

echo "▶︎ (既定 Status フィールドは変更せず利用します)"

# ボード URL を出力して終了（ブラウザは開かない）
BOARD_URL=$(gh project view "$NUMBER" \
               --owner "$OWNER" \
               --format json \
               --template "{{.url}}")

echo "🎉  Initialization complete. Board URL:"
echo "$BOARD_URL"