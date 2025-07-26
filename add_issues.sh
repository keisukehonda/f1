# 事前変数
OWNER=keisukehonda
REPO=f1
PROJ=9           # KG Roadmap のプロジェクト番号
PRIO="Priority:High"

# ---------- P0 / Schema ----------
ISSUE_URL=$(gh issue create \
  --repo $OWNER/$REPO \
  --title "P0: node schema v0 – Article ノード属性定義" \
  --body  "cuDF nodes_df に保持する Article ノードの属性（id, law, article_no, title, text, effective_date）を決定し、テーブル定義として書き起こす" \
  --label Phase:P0,Component:Schema,$PRIO \
  --assignee @me | tail -n1)        # ← 出力の最後の行が URL

gh project item-add $PROJ --owner $OWNER --url "$ISSUE_URL"

# ---------- P0 / Build ----------
ISSUE_URL=$(gh issue create \
  --repo $OWNER/$REPO \
  --title "P0: DiGraph build – nodes_df / edges_df から cuGraph" \
  --body  "nodes_df・edges_df から cugraph.DiGraph を生成する最小 PoC。PageRank が動作することを確認する" \
  --label Phase:P0,Component:Build,$PRIO \
  --assignee @me | tail -n1)

gh project item-add $PROJ --owner $OWNER --url "$ISSUE_URL"

# ---------- P0 / Query ----------
ISSUE_URL=$(gh issue create \
  --repo $OWNER/$REPO \
  --title "P0: basic query – 条番号→参照先リスト API" \
  --body  "入力された条番号から参照先（引用・準用）条文 ID を返す Python 関数を実装し、ユニットテストを追加" \
  --label Phase:P0,Component:Query,$PRIO \
  --assignee @me | tail -n1)

gh project item-add $PROJ --owner $OWNER --url "$ISSUE_URL"

# ---------- P1 / Loader ----------
ISSUE_URL=$(gh issue create \
  --repo $OWNER/$REPO \
  --title "P1: buildinglaw-loader – 条文パーサ実装" \
  --body  "建築基準法の条文 XML をパースし、Article ノードと参照エッジを抽出するローダーを実装" \
  --label Phase:P1,Component:Loader,$PRIO \
  --assignee @me | tail -n1)

gh project item-add $PROJ --owner $OWNER --url "$ISSUE_URL"
