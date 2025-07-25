```
cuGraphでKGを実装していく、必要な機能を洗い出そう。
最初の目標は法令（最初は消防法 建築基準法）をナレッジグラフとして表現する。有向グラフで実装すべきと考えてる。
・データローダーと永続化
・ノード・エッジ設計
・クエリー
```

承知しました。タスク管理を **GitHub Projects** で行う前提で、先ほど洗い出した機能群をプロジェクトボードに落とし込む具体的な設定案をまとめます。

---

## 1. プロジェクトボードの基本構成

| カラム               | 目的              | 自動移動ルール（Projects v2 の Automation） |
| ----------------- | --------------- | --------------------------------- |
| **Backlog**       | 仕様検討・実装待ちタスクを蓄積 | Issue 追加時に自動で here                |
| **Ready for Dev** | 実装要件が確定し、着手可能   | `status: ready` ラベルを付与            |
| **In Progress**   | 実装中             | Draft PR／PR が open になると自動移動       |
| **Review**        | コードレビュー & テスト   | PR に `needs review` ラベル           |
| **Done**          | マージ & ドキュメント完了  | PR が `merged` で自動クローズ             |

> Projects v2 では **カスタムフィールド** が使えます。
>
> * **Phase**: `P0 PoC / P1 MultiLaw / ...`
> * **Component**: `Loader / Schema / Build / Query`
> * **Priority**: `High / Normal / Low`

---

## 2. イシュー & プルリクの粒度例

| Phase | Component | Issue タイトル例                                     |
| ----- | --------- | ----------------------------------------------- |
| P0    | Loader    | `firelaw-loader: e-Gov API から JSON 取得`          |
| P0    | Schema    | `node schema v0: Article ノード属性定義`               |
| P0    | Build     | `DiGraph build: nodes_df / edges_df から cuGraph` |
| P0    | Query     | `basic query: 条番号→参照先リスト API`                   |
| P1    | Loader    | `buildinglaw-loader: 条文パーサ実装`                   |
| …     | …         | …                                               |

* **Issue テンプレート**に *目的 / 定義済み条件 (DoD) / 参照資料* を記載
* **PR テンプレート**に *close する Issue, 動作確認方法, スクリーンショット* を記載
* **ラベル**: `bug`, `enhancement`, `documentation`, `performance`, ほか

---

## 3. マイルストーン設定

| マイルストーン          | 期日（例）      | 完了基準                       |
| ---------------- | ---------- | -------------------------- |
| **P0 PoC**       | 2025-08-15 | 消防法だけで最短経路・PageRankが走る     |
| **P1 MultiLaw**  | 2025-09-15 | 建基法を結合し横断参照クエリー通過          |
| **P2 Query API** | 2025-10-01 | `kg_query.py` ユニットテスト 80%+ |
| **P3 Viz**       | 2025-10-20 | PyVista で 3D 可視化デモ         |
| **P4 GNN**       | 2025-11-30 | GraphSAGE 埋め込み＆類似条文推薦      |

Projects v2 は **Iterations** 機能もあるため、2週間スプリントを設定し、「Iteration」フィールドでガントチャート風に進捗を追うことも可能です。

---

## 4. 権限・ブランチ運用の一例

* **main** : 保護ブランチ、PR レビュー 1 名必須
* **dev/** : 機能別トピックブランチ（例：`dev/loader-firelaw`）
* **bot** : Dependabot／自動フォーマッタ (ruff, black) 用

---

### Tips

1. **Issue → Project カード**は GitHub の「*Projects → +Add to project*」から簡単に紐づけできます。
2. **PR を Draft** にすると、自動で *In Progress* カラムへ移動できます。
3. **GitHub Actions** でテスト／Lint を回し、ステータスを Projects カラムと連動させると可視性が上がります。
4. ドキュメントは `docs/` 配下に置き、**GitHub Pages** を有効化すると外部共有が楽です。

---

これで GitHub Projects 上にタスクを整理しやすくなるはずです。
カラム名やフィールド、マイルストーン期日はチーム運用に合わせて調整ください。追加の設定や自動化ワークフローについてご相談があればお知らせください。


```
https://github.com/keisukehonda/f1/projects?query=is%3Aopen
これがこの建築PJ全体のリポジトリ
RL、KG、Ominiverseの3サブプロジェクトがぶら下がる。それぞれプロジェクトとして切るかんじか
```

以下では、GitHub Projects（v2）を用いて **「f1」リポジトリ配下に RL・KG・Omniverse の３つのワークストリームを管理する最適な切り方** を整理します。要点だけ先にまとめると **①サブプロジェクト単位で“独立ボード”を作りつつ、②横串の管理は共通フィールドで１クリック絞り込み、③Automation とテンプレートで重複設定を最小化** する方法が最も運用コストと可視性のバランスが取れます。

---

## 1. 現状確認

* f1 リポジトリの Projects はまだ 0 件で空状態です ([GitHub][1])。
  → これから構成を自由に設計できます。

---

## 2. ボード設計の２パターン

| 方式                                                               | メリット                                                                          | デメリット                                     |                                                                     |                                                |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------- |
| **A. 3 つの専用ボード**<br>`RL Roadmap` / `KG Roadmap` / `Omni Roadmap` | \* 各チームが自分の列だけを見れば良いので集中しやすい<br>\* カスタムビューやチャートを目的別に最適化できる ([GitHub Docs][2]) | \* Issue が横断すると重複カードが増える<br>\* ボード設定が３倍必要 |                                                                     |                                                |
| **B. 単一ボード＋Component フィールド**<br>`Architecture AI Master`         | \* フィールド \`Component = RL                                                     | KG                                        | Omni\` でワンクリック切替が可能 ([GitHub Docs][3])<br>\* ガント／バーンダウンを全体視点で俯瞰しやすい | \* 列やビューフィルタを誤ると混在して見にくい<br>\* チームごとの権限分離がしにくい |

> GitHub の Best Practices では **「複数リポまたぎ or 複数チームを束ねる時はサブボード推奨」** と明言しています ([GitHub Docs][4])。今回も RL・KG・Omniverse でメンバーが大きく異なる想定なので **方式 A** が無難です。

---

## 3. 推奨：方式 A（３ボード）＋横串フィールド

### 3.1 ボードの共通テンプレート

1. **Backlog → Ready → In Progress → Review → Done** の５カラム
   *Automation* で PR open ＝ In Progress, merged ＝ Done ([The GitHub Blog][5])
2. 共通カスタムフィールド

   * `Component` : 固定値 `RL/KG/Omni`（後述の横串に利用）
   * `Phase` : `P0 PoC / P1 Alpha / P2 Beta / Release`
   * `Priority` : `High/Med/Low`

### 3.2 テンプレート化で重複設定を削減

Projects v2 はボードをテンプレート保存 → コピー可能です ([The GitHub Blog][6])。
1️⃣ Master テンプレを作成 → 2️⃣ `Make copy` で RL/KG/Omni の３ボード生成 → 3️⃣ それぞれの既定フィルタに `Component==RL` などを設定。

### 3.3 横串ダッシュボード（任意）

* 追加で “**All Streams**” ボードを 1 枚用意し、`Component` 無指定で全 Issue を統合表示。
* チャート（累積フロー図・バーンダウン）が全体進捗モニタに役立ちます ([The GitHub Blog][7])。

---

## 4. 実装ステップ

| 手順 | 操作                                                                                | 参考ドキュメント |
| -- | --------------------------------------------------------------------------------- | -------- |
| 1  | `f1` リポジトリ → **Projects → New project** ([GitHub Docs][8])                        |          |
| 2  | Layout = **Table** を選択し、上記５カラムを追加                                                 | ―        |
| 3  | **Fields → +New field** で `Component/Phase/Priority` を作成                          | ―        |
| 4  | **Automation → Item open → Backlog** などを設定                                        |          |
| 5  | Settings → **Make template** → 名前 `Std Board Template` で保存 ([The GitHub Blog][6]) |          |
| 6  | `Use as template` から<br>`RL Roadmap / KG Roadmap / Omni Roadmap` を複製              |          |
| 7  | 各ボードで `Default filter` を<br>`Component == RL` などに設定                               | ―        |
| 8  | README にプロジェクトボードの URL を追記し周知                                                     | ―        |

---

## 5. クロスリポ対応 & 追加Tips

* Projects v2 は **クロスリポの Issue/PR** を単一ボードで扱えます ([GitHub][9])。
  → RL 用コードが別リポに分かれても、同じ RL Roadmap にカード追加可能。
* **GitHub CLI `gh project`** でスクリプト更新や一括移動ができます ([The GitHub Blog][6])。
* **Sub-issues** で大型機能をタスク分割し、親 Issue を Epic 代わりに ([GitHub Docs][10])。
* **Iterations** フィールドを 2 週間スプリントで切り、ボードに `Iteration = @current` ビューを置くと現行作業が常に浮き上がります ([The GitHub Blog][5])。

---

## 6. まとめ

* **RL / KG / Omniverse** を **独立ボード** とし、共通テンプレートで統一感を確保。
* **Component フィールド** により全体ダッシュボードで横串管理も可能。
* Automation・CLI・Iterations を組み合わせれば、低運用コストでスプリント管理＋進捗可視化が実現します。

この構成で進めて問題なければ、ボード初期化用の CLI スクリプト例や Issue/PR テンプレート案もご用意できますので、必要に応じてお知らせください。

[1]: https://github.com/keisukehonda/f1/projects?query=is%3Aopen "Projects · f1 · GitHub"
[2]: https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects?utm_source=chatgpt.com "About Projects - GitHub Docs"
[3]: https://docs.github.com/en/issues/planning-and-tracking-with-projects?utm_source=chatgpt.com "Planning and tracking with Projects - GitHub Docs"
[4]: https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/planning-and-tracking-work-for-your-team-or-project?utm_source=chatgpt.com "Planning and tracking work for your team or project - GitHub Docs"
[5]: https://github.blog/developer-skills/github/getting-started-with-project-planning-on-github/?utm_source=chatgpt.com "Getting started with project planning on GitHub"
[6]: https://github.blog/developer-skills/github/10-things-you-didnt-know-you-could-do-with-github-projects/?utm_source=chatgpt.com "10 things you didn't know you could do with GitHub Projects"
[7]: https://github.blog/news-insights/product-news/planning-next-to-your-code-github-projects-is-now-generally-available/?utm_source=chatgpt.com "Planning next to your code - GitHub Projects is now generally ..."
[8]: https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/adding-your-project-to-a-repository?utm_source=chatgpt.com "Adding your project to a repository - GitHub Docs"
[9]: https://github.com/orgs/community/discussions/6296?utm_source=chatgpt.com "[Projects Beta] Milestones Across Repositories #6296 - GitHub"
[10]: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues?utm_source=chatgpt.com "Adding sub-issues - GitHub Docs"


```
NVIDA AI-Q Brueprintに準拠することが重要で、このサンプルやドキュメントのポータルとして
https://build.nvidia.com/
がある。
```

NVIDIA AI-Q Blueprint は、NIM API・NeMo Retriever マイクロサービス・NeMo Agent Toolkit をひとまとめにした公式リファレンス実装群で、エンタープライズ向け AI エージェントの開発・最適化を体系化する枠組みです。AI-Q に準拠しておくと、後段の RL 強化学習や Omniverse 連携を含むマルチエージェント基盤を **NVIDIA 公認のベストプラクティス** で一貫管理できるため、当プロジェクト（RL・KG・Omni の 3 ストリーム）でも採用メリットは大きいです。サンプルとドキュメントの母港が **build.nvidia.com** で、Blueprint テンプレ・モデル・マイクロサービスをワンクリックで試せるポータルとして機能します。([build.nvidia.com][1])

## 1. AI-Q Blueprint のコア構成

| コンポーネント                           | 役割                                         | 主なリソース                                                        |
| --------------------------------- | ------------------------------------------ | ------------------------------------------------------------- |
| **NVIDIA NIM**                    | 推論マイクロサービス。LLM から視覚モデルまで CUDA 最適化済みで即デプロイ可 | build.nvidia.com の *Models* カタログに多数掲載 ([build.nvidia.com][2]) |
| **NeMo Retriever**                | RAG 用のスケーラブル検索基盤。ファイル／ベクトル DB 両対応          | 開発者ブログで実装例公開 ([NVIDIA Developer][3])                          |
| **NeMo Agent Toolkit (AI-Q SDK)** | マルチエージェント協調・ツール実行・評価プロファイルを司る              | GitHub `aiq-research-assistant` 参照 ([GitHub][4])              |

Blueprint には **エンタープライズ研究アシスタント**、**バイオメディカル RAG** など用途別のサンプルが複数あり、Docker Compose／k8s マニフェスト付きで即起動できます。([build.nvidia.com][5], [build.nvidia.com][6])

## 2. build.nvidia.com ポータルの使い方

### 2.1 ブループリント一覧

* トップページ → **“Blueprints”** タブで全テンプレにアクセス。フィルタで *Developer Example / Industry* を選択可能。([build.nvidia.com][7])

### 2.2 ワークフロー&モデル

* **Models** カタログで NIM 化された LLM・GNN・視覚モデルを確認し、そのまま API キーで呼び出し可。([build.nvidia.com][2])
* **Search** から “AI-Q” を打つと関連 Blueprint がまとめて表示される。([build.nvidia.com][8])

### 2.3 学習リソース

* ブログ記事・YouTube 解説・フォーラム Q\&A が相互リンクされており、AI-Q の設計思想とパブリッシュ手順を解説。([NVIDIA Developer][3], [YouTube][9], [NVIDIA Developer Forums][10])

## 3. 当プロジェクト（RL / KG / Omniverse）とのマッピング

| ストリーム         | AI-Q 参照ポイント                                    | 実装イメージ                                                      |
| ------------- | ---------------------------------------------- | ----------------------------------------------------------- |
| **KG**        | NeMo Retriever の **データフライホイール** パターン           | 法令 KG を索引化 → Retriever で RAG クエリ → Agent へ供給 ([NVIDIA][11]) |
| **RL**        | AI-Q **Agent Toolkit** のマルチツール連携 API           | NeMo Agent から RL ポリシー（NVIDIA NeMo-RL）を呼び出し、設計図チェック自動化       |
| **Omniverse** | 3D-guided Generative AI Blueprint でシーン⇔AI 連携基盤 | Omniverse 内図面を Agent が解析し、修正提案を生成 ([The Verge][12])         |

> **ポイント**: AI-Q Blueprint を「インフラ層の標準」とみなし、GitHub Projects の各サブボード（RL/KG/Omni）に *Phase 0* タスクとして「AI-Q コンテナ起動」「NIM 呼び出しサンプル実行」を追加すると、安全に技術検証を進められます。

## 4. 今後の具体的アクション

1. **ポータル登録**
   build.nvidia.com の **NIM API キー** を取得し、社内 GitHub Secrets に `NVIDIA_API_KEY` として保存。([build.nvidia.com][1])
2. **Blueprint のフォーク**
   `NVIDIA-AI-Blueprints/aiq-research-assistant` を `f1` のサブディレクトリへ取り込み、Docker Compose で起動テスト。([GitHub][4])
3. **GitHub Projects にタスク追加**

   * `KG/Phase0` : NeMo Retriever で法令 PDF→ベクトル化
   * `RL/Phase0` : Agent Toolkit で RL ポリシー呼び出し PoC
   * `Omni/Phase0` : 3D-guided Blueprint 動作確認
4. **標準化ガイド**
   AI-Q Blueprint の貢献ガイドに合わせて、Dockerfile・README 体裁を統一 ([NVIDIA Developer Forums][10])
5. **Docs ポータル**
   build.nvidia.com のリンク集を `docs/aiq_portal.md` としてリポジトリにコミットし、更新フローを明確化。

---

### まとめ

AI-Q Blueprint を土台に据えることで、GPU 推論（NIM）・マルチモーダル検索（Retriever）・エージェント協調（Toolkit）の３機能をワンセットで利用でき、RL・KG・Omniverse のサブプロジェクトへスムーズに横展開できます。まずは **portal で公開されているサンプルをフォークし、GitHub Projects に Phase0 タスクを設定**――この流れで着手すると、ユーザーが意識することなく AI-Q 標準に沿った開発フローを確立できます。

[1]: https://build.nvidia.com/?utm_source=chatgpt.com "Try NVIDIA NIM APIs"
[2]: https://build.nvidia.com/models?utm_source=chatgpt.com "Models - NVIDIA NIM APIs"
[3]: https://developer.nvidia.com/blog/chat-with-your-enterprise-data-through-open-source-ai-q-nvidia-blueprint/?utm_source=chatgpt.com "Chat With Your Enterprise Data Through Open-Source AI-Q NVIDIA ..."
[4]: https://github.com/NVIDIA-AI-Blueprints/aiq-research-assistant?utm_source=chatgpt.com "NVIDIA-AI-Blueprints/aiq-research-assistant - GitHub"
[5]: https://build.nvidia.com/nvidia/aiq?utm_source=chatgpt.com "Build an AI Agent for Enterprise Research Blueprint by NVIDIA"
[6]: https://build.nvidia.com/nvidia/biomedical-aiq-research-agent?utm_source=chatgpt.com "Biomedical AI-Q Research Agent Blueprint - NVIDIA NIM APIs"
[7]: https://build.nvidia.com/blueprints?utm_source=chatgpt.com "Build Your AI Application with Blueprints - NVIDIA NIM APIs"
[8]: https://build.nvidia.com/search?utm_source=chatgpt.com "Try NVIDIA NIM APIs"
[9]: https://www.youtube.com/watch?pp=0gcJCfwAo7VqN5tD&v=1auHkFYrDO4&utm_source=chatgpt.com "Unlock the Power of AI Agents with the AI-Q NVIDIA Blueprint"
[10]: https://forums.developer.nvidia.com/t/guidance-on-creating-and-publishing-nvidia-ai-agent-blueprints-and-nims/335402?utm_source=chatgpt.com "Guidance on Creating and Publishing NVIDIA AI Agent Blueprints ..."
[11]: https://www.nvidia.com/en-us/data-center/ai-data-platform/?utm_source=chatgpt.com "AI Data Platform for Enterprise Agentic AI - NVIDIA"
[12]: https://www.theverge.com/news/658613/nvidia-ai-blueprint-blender-3d-image-references?utm_source=chatgpt.com "Nvidia's new tool can turn 3D scenes into AI images"


```
RL / KG / Omniverseのうち、RLとKGは早い段階でエージェント化されてることが必要。
NeMoエージェントtool kitを使うべきだろう。RLとKGが組み合わさったエージェントなのか別個にたてるのかはまだよくわからないが。
```

まず結論をまとめます。**NeMo Agent Toolkit を用いて「RL 専用エージェント」と「KG 専用エージェント」を早期に別個で立ち上げ、後段で Agent-of-Agents アーキテクチャに統合する**のが最も安全で拡張しやすい設計です。Toolkit はマルチエージェント連携を前提に設計されており、RL モジュール（NeMo-RL）と KG モジュール（NeMo Retriever＋NIM API）を疎結合マイクロサービスとして登録するだけで、後から一体化・分業のいずれにも対応できます。以下で根拠と具体的ロードマップを解説します。

---

## NeMo Agent Toolkit と AI-Q Blueprint の位置づけ

### Toolkit が提供する三つの柱

* **プロファイリングと最適化** – ボトルネックやコストを可視化し、大規模エージェント運用を効率化 ([NVIDIA Developer][1])
* **フレームワーク非依存の拡張性** – 追加ツールや外部サービスを YAML 1 行でプラグイン可能 ([NVIDIA Developer][2])
* **NIM・Retriever との統合** – AI-Q Blueprint が示す標準構成（NIM ↔ Retriever ↔ Agent）に準拠 ([NVIDIA Developer][3], [NVIDIA NIM][4])

### build.nvidia.com ポータルの役割

Blueprint の Docker Compose／k8s マニフェスト、NIM API キー発行、サンプルコードが一元化されており、最小手順で「動く PoC」を用意できます ([NVIDIA NIM][5], [GitHub][6])。

---

## 単一エージェント vs 分割エージェントの比較

| 観点                | **統合（RL＋KG 一体）**     | **分割（RL エージェント＋KG エージェント）**         |
| ----------------- | -------------------- | ----------------------------------- |
| **初期実装コスト**       | コンテナ数が少なく簡潔          | モジュール 2 つを並行開発                      |
| **拡張性 / 責務分離**    | ロジック肥大化の懸念           | 役割が明確、再利用しやすい                       |
| **スケール戦略**        | 同時スケールで GPU 資源を浪費しがち | 負荷に応じ個別にオートスケール可 ([NVIDIA Docs][7]) |
| **障害耐性**          | モノリシックで影響範囲大         | 片方ダウンでも残りが機能                        |
| **マルチエージェントパターン** | 不要（単一）               | Agent-of-Agents で協調処理 ([NVIDIA][8]) |

> **推奨**: まずは **分割配置** → 早期に RL と KG を独立デプロイして疎結合 API で連携し、後でニーズに応じて「統合ビュー」を作る。

---

## 初期ロードマップ（Phase 0〜1）

### Phase 0: PoC 起動

1. **KG エージェント**

   * NeMo Retriever で消防法・建築基準法の条文 Embedding をインデックス化 ([NVIDIA Blog][9])
   * Toolkit の `kg_agent.yaml` に NIM Embedding & Search エンドポイントを登録
2. **RL エージェント**

   * NeMo-RL サンプル（DPO or PPO）を NIM 化し `rl_agent.yaml` として登録 ([NVIDIA Docs][10])
   * タスク: 法令チェック → 報酬は「違反数の減少」で設計
3. **Orchestrator（薄いメディエータ）**

   * Toolkit のテンプレ `agent_manager.yaml` を流用し、KG→RL→結果返却のパイプラインを定義 ([NVIDIA Developer][2])

### Phase 1: Agent-of-Agents 統合

* **Skill Router** – 入力を解析し KG or RL へ振り分け、複合要求時は両者を並列呼び出し
* **Memory/Data Flywheel** – 推論ログを build.nvidia.com 推奨のデータフライホイールにバッチ投入し継続学習 ([NVIDIA][11])
* **Guardrails** – NeMo Guardrails でポリシー制御、マルチ NIM を統合監視 ([NVIDIA Docs][7])

---

## GitHub Projects へのタスク反映（抜粋）

| Component        | Issue                     | Done when                            |
| ---------------- | ------------------------- | ------------------------------------ |
| **KG-agent**     | `setup_retriever_firelaw` | 条文 PDF → index → `/kg/search` API 返却 |
| **RL-agent**     | `nemo_rl_policy_poc`      | `POST /rl/check` が JSON で指摘リストを出力    |
| **Orchestrator** | `agent_manager_phase0`    | `POST /agent/validate` で一連の流れが動作     |
| **CI/CD**        | `nim_deploy_pipeline`     | main ブランチ push → NGC に自動 push        |

---

## まとめと次アクション

1. **分割エージェント**（RL, KG）を NeMo Agent Toolkit で早期に稼働させる。
2. build.nvidia.com から AI-Q Blueprint サンプルをフォークし、Docker Compose で PoC を 1 週間以内に立ち上げる。
3. GitHub Projects の *Phase0* に上表の Issue を追加し、担当を割当。
4. Phase 1 で Agent-of-Agents 統合・データフライホイール・Guardrails を段階的に適用。

これで「RL と KG がエージェント化されていること」を満たしつつ、後々 Omniverse 連携や追加ツール統合にも柔軟に対応できる土台が整います。

[1]: https://developer.nvidia.com/nemo-agent-toolkit?utm_source=chatgpt.com "NVIDIA NeMo Agent Toolkit"
[2]: https://developer.nvidia.com/blog/extending-the-nvidia-nemo-agent-toolkit-to-support-new-agentic-frameworks/?utm_source=chatgpt.com "Extending the NVIDIA NeMo Agent Toolkit to Support New Agentic ..."
[3]: https://developer.nvidia.com/blog/chat-with-your-enterprise-data-through-open-source-ai-q-nvidia-blueprint/?utm_source=chatgpt.com "Chat With Your Enterprise Data Through Open-Source AI-Q NVIDIA ..."
[4]: https://build.nvidia.com/?utm_source=chatgpt.com "Try NVIDIA NIM APIs"
[5]: https://build.nvidia.com/nvidia/aiq?utm_source=chatgpt.com "Build an AI Agent for Enterprise Research Blueprint by NVIDIA"
[6]: https://github.com/NVIDIA/NeMo-Agent-Toolkit?utm_source=chatgpt.com "NVIDIA/NeMo-Agent-Toolkit - GitHub"
[7]: https://docs.nvidia.com/nemo/microservices/latest/guardrails/tutorials/multiple-nim-microservices.html?utm_source=chatgpt.com "Working with Multiple NIM for LLMs — NVIDIA NeMo Microservices"
[8]: https://www.nvidia.com/en-us/glossary/multi-agent-systems/?utm_source=chatgpt.com "What are Multi-Agent Systems? | NVIDIA Glossary"
[9]: https://blogs.nvidia.com/blog/nemo-guardrails-nim-microservices/?utm_source=chatgpt.com "NVIDIA Releases NIM Microservices to Safeguard Applications for ..."
[10]: https://docs.nvidia.com/nemo/rl/latest/index.html?utm_source=chatgpt.com "Nemo RL: A Scalable and Efficient Post-Training Library"
[11]: https://www.nvidia.com/en-us/ai-data-science/products/nemo/?utm_source=chatgpt.com "Build Custom Generative AI | NVIDIA NeMo"


```
 NeMo Agent Toolkit
aiqっていうCLIいれるみたいだな。
```

NVIDIA NeMo Agent Toolkit（旧名 NVIDIA Agent Intelligence Toolkit＝AIQ）は、複数エージェントを統合管理するための OSS ライブラリで、付属 CLI **`aiq`** がワークフロー作成・実行の中枢に位置づけられます。`aiq` を早期に導入しておくと、KG 専用エージェントと RL 専用エージェントの両方を同じ開発パイプラインで管理でき、後から Omniverse 連携エージェントを追加しても最小限の変更で済みます。([NVIDIA Developer][1], [GitHub][2])

## 1. `aiq` CLI の位置づけ

* **役割**

  * ワークフロー雛形の生成 (`aiq workflow create …`) ([NVIDIA Developer][3])
  * 実行ログ・プロファイルの収集 (`aiq run … --profile`)([NVIDIA Developer][4])
  * インストール確認 (`aiq --version`)([GitHub][2])
* **名称変更に注意**
  2025 年 6 月に「Agent Intelligence Toolkit（AIQ）」から **「NeMo Agent Toolkit」** へ改称されましたが、CLI コマンド名は引き続き `aiq` のまま維持されています。([NVIDIA Developer Forums][5])

## 2. インストール手順（Linux 環境での例）

```bash
# 1. CUDA 12.4 対応 PyTorch 環境を準備
conda create -n nemo_agent python=3.10
conda activate nemo_agent

# 2. NeMo Agent Toolkit を取得
pip install nemo-agent-toolkit

# 3. 動作確認
aiq --version
```

* 公式ドキュメントの Quick-Start 手順では、NVIDIA NGC 版コンテナ（`nvcr.io/nvidia/aiq:latest`）も提供されています。([NVIDIA Docs][6])
* Windows は現在一部機能が未対応との報告があります。([NVIDIA Developer Forums][7])

## 3. 典型的な初期コマンド

| 目的         | コマンド例                                | 補足                                        |
| ---------- | ------------------------------------ | ----------------------------------------- |
| プロジェクト雛形作成 | `aiq project scaffold my_agent_proj` | デフォルト設定一式を生成([NVIDIA Developer][3])       |
| ワークフロー生成   | `aiq workflow create kg_example`     | `workflow.yaml` と `config.yml` を自動生成      |
| 実行         | `aiq run workflow.yaml`              | NIM／OpenAI など LLM プロバイダを自動判別              |
| プロファイル表示   | `aiq profile view latest`            | 各ツールのレイテンシ・コストを可視化([NVIDIA Developer][4]) |

## 4. RL・KG エージェント開発フローへの組み込み

1. **KG エージェント**

   * `LawRetriever` ツール→NeMo Retriever を REST 経由で呼び出し。
   * `aiq workflow create kg_workflow` で雛形を生成し、`tools/law_retriever.py` を追加。
2. **RL エージェント**

   * `PolicyExecutor` ツール→NeMo-RL（GRPO）を gRPC 呼び出し。
   * `aiq workflow create rl_workflow` 後、`tools/policy_executor.py` を実装。
3. **統合オーケストレーション**

   * `workflows/design_checker.yaml` で KG→RL→応答の順にステップを定義。
   * `aiq run workflows/design_checker.yaml` で両エージェント連携を検証。

Toolkit の YAML ワークフローは、後から **Omniverse SceneInspector** ツールなどを追加してもステップを追記するだけで拡張できます。([GitHub][8], [NVIDIA Developer][9])

## 5. 参考リソース

* GitHub: `NVIDIA/NeMo-Agent-Toolkit`（README にインストール手順と `aiq` 基本コマンド）([GitHub][2])
* 公式 Docs: “Installing NVIDIA Agent Intelligence Toolkit” 章（依存バージョン一覧）([NVIDIA Docs][6])
* 開発者ブログ: “Improve AI Code Generation Using NVIDIA NeMo Agent Toolkit” （`aiq workflow create` 事例）([NVIDIA Developer][3])
* YouTube: “Build Custom AI Agents with NeMo Agent Toolkit” （GUI ↔ CLI 連携デモ）([YouTube][10])

---

### 結論

`aiq` CLI は NeMo Agent Toolkit の **心臓部** です。早い段階で `aiq` を導入し、KG エージェントと RL エージェントのワークフロー雛形を用意しておくことで、後続の Omniverse 連携や CI/CD 自動化まで NVIDIA AI-Q Blueprint のベストプラクティスと整合した開発体制を構築できます。

[1]: https://developer.nvidia.com/nemo-agent-toolkit?utm_source=chatgpt.com "NVIDIA NeMo Agent Toolkit"
[2]: https://github.com/NVIDIA/NeMo-Agent-Toolkit?utm_source=chatgpt.com "NVIDIA/NeMo-Agent-Toolkit - GitHub"
[3]: https://developer.nvidia.com/blog/improve-ai-code-generation-using-nvidia-nemo-agent-toolkit/?utm_source=chatgpt.com "Improve AI Code Generation Using NVIDIA NeMo Agent Toolkit"
[4]: https://developer.nvidia.com/blog/extending-the-nvidia-nemo-agent-toolkit-to-support-new-agentic-frameworks/?utm_source=chatgpt.com "Extending the NVIDIA NeMo Agent Toolkit to Support New Agentic ..."
[5]: https://forums.developer.nvidia.com/t/nvidia-agent-intelligence-toolkit-is-now-the-nvidia-nemo-agent-toolkit/335881?utm_source=chatgpt.com "NVIDIA Agent Intelligence toolkit is now the NVIDIA NeMo Agent toolkit"
[6]: https://docs.nvidia.com/aiqtoolkit/latest/quick-start/installing.html?utm_source=chatgpt.com "Installing NVIDIA Agent Intelligence Toolkit - aiq"
[7]: https://forums.developer.nvidia.com/t/does-nemo-agent-toolkit-support-running-on-windows/338742?utm_source=chatgpt.com "Does NeMo Agent Toolkit support running on Windows?"
[8]: https://github.com/NVIDIA/NeMo-Agent-Toolkit-UI?utm_source=chatgpt.com "NVIDIA/NeMo-Agent-Toolkit-UI - GitHub"
[9]: https://developer.nvidia.com/blog/how-to-build-custom-ai-agents-with-nvidia-nemo-agent-toolkit-open-source-library/?utm_source=chatgpt.com "How to Build Custom AI Agents with NVIDIA NeMo Agent Toolkit ..."
[10]: https://www.youtube.com/watch?v=NsogD7UhZ4Q&utm_source=chatgpt.com "How to Build Custom AI Agents with NVIDIA NeMo Agent ... - YouTube"
