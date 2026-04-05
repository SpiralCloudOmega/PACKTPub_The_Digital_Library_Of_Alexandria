#!/usr/bin/env python3
"""
Packt Index Statistics & Topic Generator
==========================================
Parses PACKT_INDEX.md and generates:
  1. Console statistics (top repos, language breakdown, topic analysis)
  2. PACKT_TOPICS.md — repos organized by technology area

Usage:
    python scripts/packt_stats.py                    # Print stats to console
    python scripts/packt_stats.py --topics           # Also generate PACKT_TOPICS.md
    python scripts/packt_stats.py --topics --json     # Also output stats as JSON
"""

import argparse
import datetime
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

INDEX_FILE = "PACKT_INDEX.md"
TOPICS_FILE = "PACKT_TOPICS.md"

# ─── Topic classification rules ──────────────────────────────────────────────
# Each topic maps to a list of keyword patterns (matched against repo name + description)
TOPIC_RULES = {
    "🤖 Artificial Intelligence & Machine Learning": [
        r"machine.?learning", r"\bml\b", r"deep.?learning", r"\bdl\b",
        r"neural.?network", r"reinforcement.?learning", r"\bai\b",
        r"artificial.?intelligence", r"tensorflow", r"pytorch", r"keras",
        r"scikit", r"nlp", r"natural.?language", r"computer.?vision",
        r"opencv", r"yolo", r"object.?detection", r"image.?classif",
        r"gpt", r"\bllm\b", r"large.?language", r"generative.?ai",
        r"chatbot", r"transformer", r"bert", r"langchain", r"rag\b",
        r"hugging.?face", r"diffusion", r"stable.?diffusion",
        r"prompt.?engineer", r"copilot", r"openai",
    ],
    "📊 Data Science & Analytics": [
        r"data.?science", r"data.?analy", r"pandas", r"numpy",
        r"jupyter", r"kaggle", r"statistics", r"visualization",
        r"matplotlib", r"seaborn", r"plotly", r"tableau", r"power.?bi",
        r"\beda\b", r"exploratory", r"data.?engineer", r"data.?pipeline",
        r"etl\b", r"data.?warehouse", r"big.?data", r"spark", r"hadoop",
        r"pyspark", r"databricks", r"snowflake", r"airflow",
        r"data.?mining", r"data.?model",
    ],
    "☁️ Cloud & DevOps": [
        r"\baws\b", r"amazon.?web", r"\bazure\b", r"\bgcp\b",
        r"google.?cloud", r"cloud.?native", r"cloud.?computing",
        r"devops", r"docker", r"kubernetes", r"\bk8s\b", r"terraform",
        r"ansible", r"jenkins", r"ci.?cd", r"infrastructure.?as.?code",
        r"\biac\b", r"helm", r"serverless", r"lambda", r"ecs\b",
        r"microservice", r"service.?mesh", r"istio", r"prometheus",
        r"grafana", r"monitoring", r"gitops", r"argocd",
    ],
    "🔒 Cybersecurity": [
        r"security", r"penetration.?test", r"pentest", r"hacking",
        r"ethical.?hack", r"cybersecurity", r"cyber.?security",
        r"malware", r"forensic", r"incident.?response",
        r"vulnerability", r"exploit", r"\bsoc\b", r"threat",
        r"encryption", r"cryptograph", r"kali", r"metasploit",
        r"wireshark", r"burp", r"owasp", r"firewall", r"\bids\b",
        r"intrusion", r"comptia.?security", r"\bceh\b", r"\bcissp\b",
    ],
    "🌐 Web Development": [
        r"\breact\b", r"\bangular\b", r"\bvue\b", r"next\.?js",
        r"node\.?js", r"express", r"django", r"flask", r"fastapi",
        r"web.?develop", r"html", r"css", r"javascript",
        r"typescript", r"frontend", r"front.?end", r"backend",
        r"back.?end", r"full.?stack", r"responsive", r"bootstrap",
        r"tailwind", r"svelte", r"\bapi\b", r"rest\b", r"graphql",
        r"websocket", r"\bphp\b", r"laravel", r"wordpress",
        r"asp\.?net", r"blazor", r"web.?app",
    ],
    "📱 Mobile Development": [
        r"\bios\b", r"android", r"flutter", r"react.?native",
        r"swift(?:ui)?", r"kotlin", r"mobile", r"xamarin",
        r"\bmaui\b", r"ionic", r"cordova", r"app.?develop",
        r"iphone", r"ipad",
    ],
    "🎮 Game Development": [
        r"unity", r"unreal", r"game.?develop", r"game.?design",
        r"godot", r"blender", r"3d.?model", r"3d.?game",
        r"2d.?game", r"opengl", r"vulkan", r"shader",
        r"animation", r"mecanim", r"game.?engine",
    ],
    "🐍 Python": [
        r"\bpython\b", r"django", r"flask", r"fastapi",
        r"asyncio", r"pytest", r"pip\b", r"pep\b",
    ],
    "☕ Java & JVM": [
        r"\bjava\b(?!script)", r"spring", r"\bjvm\b", r"kotlin",
        r"scala", r"groovy", r"gradle", r"maven",
        r"hibernate", r"quarkus", r"micronaut",
    ],
    "🔷 .NET & C#": [
        r"\.net\b", r"\bc#\b", r"c.?sharp", r"asp\.?net",
        r"\bmaui\b", r"blazor", r"entity.?framework",
        r"wpf\b", r"xamarin", r"dotnet",
    ],
    "🏗️ Software Architecture & Design Patterns": [
        r"design.?pattern", r"architecture", r"microservice",
        r"clean.?code", r"solid\b", r"refactor", r"ddd\b",
        r"domain.?driven", r"event.?driven", r"cqrs",
        r"hexagonal", r"modulith",
    ],
    "🔧 Systems & Low-Level Programming": [
        r"\bc\+\+", r"\bcpp\b", r"\bc\b(?!#)", r"\brust\b",
        r"\bgo\b(?!ogle)", r"golang", r"linux", r"kernel",
        r"embedded", r"\bcuda\b", r"assembly", r"system.?program",
        r"operating.?system", r"memory.?management",
    ],
    "🗄️ Databases": [
        r"\bsql\b", r"mysql", r"postgres", r"mongodb",
        r"redis", r"cassandra", r"dynamodb", r"database",
        r"nosql", r"graph.?database", r"neo4j", r"elasticsearch",
        r"sqlite",
    ],
    "🧪 Testing & QA": [
        r"testing", r"\btdd\b", r"\bbdd\b", r"test.?driven",
        r"selenium", r"cypress", r"jest\b", r"pytest",
        r"junit", r"qa\b", r"quality.?assurance",
        r"automation.?test", r"performance.?test", r"load.?test",
    ],
    "🔗 Blockchain & Web3": [
        r"blockchain", r"ethereum", r"solidity", r"web3",
        r"smart.?contract", r"defi", r"\bnft\b", r"crypto",
        r"bitcoin", r"hyperledger",
    ],
    "🌐 Networking & Infrastructure": [
        r"network", r"\btcp\b", r"\bdns\b", r"cisco",
        r"comptia.?network", r"\bccna\b", r"\bccnp\b",
        r"routing", r"switching", r"wireless", r"\b5g\b",
        r"load.?balanc", r"proxy", r"nginx",
    ],
    "📖 Certifications & Exams": [
        r"certifi", r"\bexam\b", r"comptia", r"\baws.?certified",
        r"\bazure.?certified", r"\bcka\b", r"\bckad\b",
        r"\bcissp\b", r"\bceh\b", r"\bpmp\b", r"\bmos\b",
        r"practice.?test",
    ],
    "🤖 Robotics & IoT": [
        r"robot", r"\biot\b", r"internet.?of.?things",
        r"raspberry.?pi", r"arduino", r"sensor",
        r"embedded", r"\bro[s2]\b", r"drone",
    ],
}


def parse_index(path: str) -> list:
    """Parse PACKT_INDEX.md into a list of repo dicts."""
    repos = []
    pattern = re.compile(
        r"\| \[(.+?)\]\((.+?)\) \| (.*?) \| (.*?) \| (.*?) \|"
    )
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                name, url, desc, lang, stars_raw = m.groups()
                stars = 0
                sm = re.search(r"(\d+)", stars_raw)
                if sm:
                    stars = int(sm.group(1))
                repos.append({
                    "name": name.strip(),
                    "url": url.strip(),
                    "description": desc.strip().replace("\\|", "|"),
                    "language": lang.strip(),
                    "stars": stars,
                })
    return repos


def classify_repo(repo: dict) -> list:
    """Return list of topic names that match this repo."""
    text = f"{repo['name']} {repo['description']}".lower()
    # Normalize hyphens to spaces for better matching
    text_normalized = text.replace("-", " ").replace("_", " ")
    topics = []
    for topic, patterns in TOPIC_RULES.items():
        for pat in patterns:
            if re.search(pat, text_normalized, re.IGNORECASE):
                topics.append(topic)
                break
    return topics


def print_stats(repos: list) -> dict:
    """Print comprehensive statistics and return the data dict."""
    total = len(repos)
    starred = [r for r in repos if r["stars"] > 0]
    total_stars = sum(r["stars"] for r in repos)
    langs = Counter(r["language"] for r in repos if r["language"])
    topics = defaultdict(list)
    uncategorized = []

    for r in repos:
        matched = classify_repo(r)
        if matched:
            for t in matched:
                topics[t].append(r)
        else:
            uncategorized.append(r)

    print("=" * 60)
    print("📚 PacktPublishing Index Statistics")
    print("=" * 60)
    print(f"\n📦 Total Repositories:  {total:,}")
    print(f"⭐ Repos with Stars:    {len(starred):,}")
    print(f"⭐ Total Stars:         {total_stars:,}")
    print(f"💻 Unique Languages:    {len(langs)}")
    print(f"🏷️  Topic Categories:    {len(topics)}")
    print(f"❓ Uncategorized:       {len(uncategorized):,}")

    print(f"\n{'─' * 60}")
    print("🏆 Top 25 Most Starred Repositories")
    print(f"{'─' * 60}")
    for i, r in enumerate(sorted(repos, key=lambda x: x["stars"], reverse=True)[:25], 1):
        print(f"  {i:>2}. ⭐ {r['stars']:>5}  {r['name']}")

    print(f"\n{'─' * 60}")
    print("💻 Top 15 Programming Languages")
    print(f"{'─' * 60}")
    max_count = langs.most_common(1)[0][1] if langs else 1
    for lang, count in langs.most_common(15):
        bar = "█" * int(30 * count / max_count)
        pct = 100 * count / total
        print(f"  {lang:<20} {count:>5} ({pct:>4.1f}%) {bar}")

    print(f"\n{'─' * 60}")
    print("🏷️  Topic Distribution")
    print(f"{'─' * 60}")
    for topic in sorted(topics.keys(), key=lambda t: len(topics[t]), reverse=True):
        count = len(topics[topic])
        top_repo = max(topics[topic], key=lambda r: r["stars"])
        print(f"  {topic}")
        print(f"    {count:>5} repos  |  Top: ⭐{top_repo['stars']} {top_repo['name']}")

    stats = {
        "total_repos": total,
        "total_stars": total_stars,
        "repos_with_stars": len(starred),
        "unique_languages": len(langs),
        "top_languages": {lang: count for lang, count in langs.most_common(15)},
        "top_repos": [
            {"name": r["name"], "stars": r["stars"], "language": r["language"]}
            for r in sorted(repos, key=lambda x: x["stars"], reverse=True)[:25]
        ],
        "topics": {
            topic: {
                "count": len(rlist),
                "top_repo": max(rlist, key=lambda r: r["stars"])["name"],
            }
            for topic, rlist in topics.items()
        },
        "uncategorized_count": len(uncategorized),
    }
    return stats


def generate_topics_md(repos: list) -> str:
    """Generate PACKT_TOPICS.md — repos organized by technology topic."""
    topics = defaultdict(list)
    uncategorized = []

    for r in repos:
        matched = classify_repo(r)
        if matched:
            for t in matched:
                topics[t].append(r)
        else:
            uncategorized.append(r)

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(repos)
    total_stars = sum(r["stars"] for r in repos)
    langs = Counter(r["language"] for r in repos if r["language"])

    lines = []
    lines.append("# 🏷️ PacktPublishing — Topics & Categories")
    lines.append("")
    lines.append(f"> Auto-generated **{now}** from [{total:,} repositories](PACKT_INDEX.md)")
    lines.append(f"> ⭐ {total_stars:,} total stars across {len(langs)} programming languages")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Quick stats dashboard
    lines.append("## 📊 Quick Stats")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Repositories | **{total:,}** |")
    lines.append(f"| Total Stars | **⭐ {total_stars:,}** |")
    lines.append(f"| Unique Languages | **{len(langs)}** |")
    lines.append(f"| Topic Categories | **{len(topics)}** |")
    lines.append("")

    # Language chart
    lines.append("### 💻 Top Languages")
    lines.append("")
    lines.append("| Language | Repos | Share |")
    lines.append("|----------|------:|------:|")
    for lang, count in langs.most_common(15):
        pct = 100 * count / total
        bar = "█" * max(1, int(20 * count / langs.most_common(1)[0][1]))
        lines.append(f"| {lang} | {count:,} | {pct:.1f}% {bar} |")
    lines.append("")

    # Top 25 overall
    lines.append("### 🏆 Top 25 Most Starred")
    lines.append("")
    lines.append("| # | Repository | Language | ⭐ |")
    lines.append("|--:|------------|----------|----|")
    for i, r in enumerate(sorted(repos, key=lambda x: x["stars"], reverse=True)[:25], 1):
        lines.append(
            f"| {i} | [{r['name']}]({r['url']}) | {r['language']} | ⭐ {r['stars']:,} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Topic navigation
    lines.append("## 🔍 Topic Navigation")
    lines.append("")
    sorted_topics = sorted(topics.keys(), key=lambda t: len(topics[t]), reverse=True)
    for topic in sorted_topics:
        slug = re.sub(r"[^\w\s-]", "", topic).strip().lower().replace(" ", "-")
        slug = re.sub(r"-+", "-", slug)
        lines.append(f"- [{topic}](#{slug}) ({len(topics[topic]):,} repos)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Each topic section
    for topic in sorted_topics:
        topic_repos = topics[topic]
        sorted_repos = sorted(topic_repos, key=lambda x: x["stars"], reverse=True)

        lines.append(f"## {topic}")
        lines.append("")
        lines.append(f"> **{len(topic_repos):,}** repositories")
        lines.append("")

        # Show top 10 with description, then compact list for the rest
        lines.append("### ⭐ Highlights")
        lines.append("")
        lines.append("| Repository | Description | Language | ⭐ |")
        lines.append("|------------|-------------|----------|----|")
        for r in sorted_repos[:10]:
            desc = r["description"][:80] + "..." if len(r["description"]) > 80 else r["description"]
            stars_str = f"⭐ {r['stars']:,}" if r["stars"] > 0 else ""
            lines.append(f"| [{r['name']}]({r['url']}) | {desc} | {r['language']} | {stars_str} |")
        lines.append("")

        if len(sorted_repos) > 10:
            lines.append(f"<details><summary>📂 View all {len(sorted_repos):,} repos in this category</summary>")
            lines.append("")
            lines.append("| Repository | Language | ⭐ |")
            lines.append("|------------|----------|----|")
            for r in sorted_repos[10:]:
                stars_str = f"⭐ {r['stars']}" if r["stars"] > 0 else ""
                lines.append(f"| [{r['name']}]({r['url']}) | {r['language']} | {stars_str} |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Uncategorized
    if uncategorized:
        lines.append("## ❓ Uncategorized")
        lines.append("")
        lines.append(f"> **{len(uncategorized):,}** repositories not yet classified")
        lines.append("")
        lines.append("<details><summary>📂 View all</summary>")
        lines.append("")
        lines.append("| Repository | Description | Language | ⭐ |")
        lines.append("|------------|-------------|----------|----|")
        for r in sorted(uncategorized, key=lambda x: x["stars"], reverse=True):
            desc = r["description"][:80] + "..." if len(r["description"]) > 80 else r["description"]
            stars_str = f"⭐ {r['stars']}" if r["stars"] > 0 else ""
            lines.append(f"| [{r['name']}]({r['url']}) | {desc} | {r['language']} | {stars_str} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze the PacktPublishing index and generate topic categories"
    )
    parser.add_argument(
        "--index", default=INDEX_FILE, help=f"Path to index file (default: {INDEX_FILE})"
    )
    parser.add_argument(
        "--topics", action="store_true", help="Generate PACKT_TOPICS.md"
    )
    parser.add_argument(
        "--topics-output", default=TOPICS_FILE, help=f"Topics output file (default: {TOPICS_FILE})"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output stats as JSON to stdout"
    )
    args = parser.parse_args()

    if not Path(args.index).exists():
        print(f"❌ Index file not found: {args.index}")
        print("   Run: python scripts/generate_packt_index.py")
        sys.exit(1)

    repos = parse_index(args.index)
    if not repos:
        print(f"❌ No repos parsed from {args.index}")
        sys.exit(1)

    stats = print_stats(repos)

    if args.json:
        print(f"\n{'─' * 60}")
        print("📋 JSON Output")
        print(f"{'─' * 60}")
        print(json.dumps(stats, indent=2))

    if args.topics:
        content = generate_topics_md(repos)
        with open(args.topics_output, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = len(content) / 1024
        print(f"\n📄 Generated {args.topics_output} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
