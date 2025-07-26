"""
src/kg/loader/firelaw_loader.py

消防法（昭和23年法律第186号）を e-Gov PDF/XML から取り込み
nodes_df, edges_df (cudf) を返す PoC ローダー
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Tuple

import cudf
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text


class FireLawLoader:
  """消防法ローダー"""

  ARTICLE_RE = re.compile(r"^第(?P<num>[\d〇一二三四五六七八九十]+)条")  # 漢数字対応
  REF_RE = re.compile(r"第(?P<dst>[\d〇一二三四五六七八九十]+)条")

  def __init__(self, src_path: Path) -> None:
    self.src_path = src_path

  # ---------- public -------------------------------------------------
  def load(self) -> Tuple[cudf.DataFrame, cudf.DataFrame]:
    """nodes_df, edges_df を返す"""
    text = self._extract_text()
    articles = self._parse_articles(text)
    refs = self._parse_references(articles)

    nodes_df = cudf.DataFrame(articles)
    edges_df = cudf.DataFrame(refs)
    return nodes_df, edges_df

  # ---------- private ------------------------------------------------
  def _extract_text(self) -> str:
    """PDF なら pdfminer、XML なら BeautifulSoup で条文テキストを得る"""
    if self.src_path.suffix.lower() == ".pdf":
      return extract_text(self.src_path)
    if self.src_path.suffix.lower() in {".xml", ".html"}:
      soup = BeautifulSoup(self.src_path.read_text(encoding="utf-8"), "lxml")
      return soup.get_text("\n")
    raise ValueError(f"Unsupported extension: {self.src_path.suffix}")

  def _parse_articles(self, text: str) -> list[dict]:
    """条番号・条文テキストを抽出しリスト化"""
    articles: list[dict] = []
    current = None
    for line in text.splitlines():
      m = self.ARTICLE_RE.match(line.strip())
      if m:
        # 新しい条文開始
        if current:
          articles.append(current)
        current = {
          "id": len(articles),
          "law": "FireLaw",
          "article_no": self._kanji2int(m.group("num")),
          "title": line.strip(),
          "text": "",
        }
      elif current:
        current["text"] += line.strip() + "\n"
    if current:
      articles.append(current)
    return articles

  def _parse_references(self, articles: list[dict]) -> list[dict]:
    """条文内の参照を edges として抽出"""
    edges: list[dict] = []
    for art in articles:
      for m in self.REF_RE.finditer(art["text"]):
        dst_no = self._kanji2int(m.group("dst"))
        edges.append(
          {
            "src_id": art["id"],
            "dst_no": dst_no,
            "edge_type": "引用",
            "context": m.group(0),
          }
        )
    # dst_no → dst_id へ番号対応
    no2id = {a["article_no"]: a["id"] for a in articles}
    for e in edges:
      e["dst_id"] = no2id.get(e["dst_no"], -1)
    return edges

  # ---------- util ---------------------------------------------------
  @staticmethod
  def _kanji2int(kanji: str) -> int:
    """ごく簡易的な漢数字→整数変換（十進法のみ対応）"""
    table = {"〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if "十" not in kanji:
      return table.get(kanji, int(kanji))
    # 例) 十二 = 10+2, 二十三 = 2*10+3
    parts = kanji.split("十")
    left = table.get(parts[0], 1)  # 十三 → '' (1)
    right = table.get(parts[1], 0) if len(parts) > 1 else 0
    return left * 10 + right


# ------------------------------- CLI -------------------------------
if __name__ == "__main__":
  import argparse

  p = argparse.ArgumentParser(description="消防法ローダー PoC")
  p.add_argument("--src", required=True, help="消防法 PDF または XML のパス")
  p.add_argument("--outdir", default="data", help="Parquet 出力先ディレクトリ")
  args = p.parse_args()

  loader = FireLawLoader(Path(args.src))
  nodes, edges = loader.load()

  outdir = Path(args.outdir)
  outdir.mkdir(parents=True, exist_ok=True)
  nodes.to_parquet(outdir / "firelaw_nodes.pq")
  edges.to_parquet(outdir / "firelaw_edges.pq")

  # 簡易統計を JSON で出力
  stats = {"nodes": len(nodes), "edges": len(edges)}
  (outdir / "firelaw_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
  print(json.dumps(stats, indent=2, ensure_ascii=False))
