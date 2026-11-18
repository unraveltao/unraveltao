#!/usr/bin/env python3
"""Generate self-hosted GitHub profile SVGs from GitHub GraphQL data."""
import datetime as dt
import html
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

USER = os.environ.get("PROFILE_USER", "unraveltao")
TOKEN = os.environ["GH_TOKEN"]
OUT = Path("assets/activity")
OUT.mkdir(parents=True, exist_ok=True)
query = """query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    repositories(ownerAffiliations:OWNER, first:100, privacy:PUBLIC) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
    }
  }
}"""
req = Request("https://api.github.com/graphql", data=json.dumps({"query":query,"variables":{"login":USER}}).encode(), headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json","User-Agent":"profile-svg-generator"})
with urlopen(req, timeout=30) as response:
    payload = json.load(response)
if payload.get("errors") or not payload.get("data", {}).get("user"):
    raise RuntimeError(f"GitHub GraphQL query failed: {payload.get('errors', 'user not found')}")
u = payload["data"]["user"]
c = u["contributionsCollection"]
calendar = c["contributionCalendar"]
stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
def esc(value):
    return html.escape(str(value), quote=True)
def save(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
def stats(theme):
    dark = theme == "dark"
    bg, fg, sub, accent, border = ("none","#c9d1d9","#8b949e","#58a6ff","#30363d") if dark else ("none","#1f2328","#59636e","#0969da","#d1d9e0")
    values = [("Contributions (last year)",calendar["totalContributions"]),("Commits",c["totalCommitContributions"]),("Pull requests",c["totalPullRequestContributions"]),("Public repos",u["repositories"]["totalCount"]),("Stars (first 100 repos)",stars),("Followers",u["followers"]["totalCount"])]
    rows = "".join(f'<text x="28" y="{100+i*35}" fill="{sub}" font-size="15">{esc(label)}</text><text x="565" y="{100+i*35}" fill="{fg}" font-size="17" text-anchor="end" font-weight="bold">{esc(value)}</text>' for i,(label,value) in enumerate(values))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="310" viewBox="0 0 600 310" role="img" aria-label="GitHub activity statistics for {esc(USER)}"><rect x="1" y="1" width="598" height="308" rx="12" fill="none" stroke="{border}"/><text x="28" y="43" fill="{accent}" font-family="Arial,sans-serif" font-size="22" font-weight="bold">Developer Activity</text><g font-family="Arial,sans-serif">{rows}</g><text x="28" y="295" fill="{sub}" font-family="Arial,sans-serif" font-size="11">GitHub GraphQL · Updated {dt.date.today().isoformat()}</text></svg>'
def heatmap(theme):
    dark = theme == "dark"
    bg, fg, border = ("none","#c9d1d9","#30363d") if dark else ("none","#1f2328","#d1d9e0")
    palette = ["#161b22","#0e4429","#006d32","#26a641","#39d353"] if dark else ["#ebedf0","#9be9a8","#40c463","#30a14e","#216e39"]
    levels = {"NONE":0,"FIRST_QUARTILE":1,"SECOND_QUARTILE":2,"THIRD_QUARTILE":3,"FOURTH_QUARTILE":4}
    cells = []
    for wi, week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            weekday = dt.date.fromisoformat(day["date"]).weekday()
            sunday_first = (weekday+1)%7
            x,y = 45+wi*13,60+sunday_first*13
            color = palette[levels[day["contributionLevel"]]]
            cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color}"><title>{esc(day["date"])}: {day["contributionCount"]} contributions</title></rect>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="180" viewBox="0 0 780 180" role="img" aria-label="GitHub contribution calendar for {esc(USER)}"><rect x="1" y="1" width="778" height="178" rx="12" fill="{bg}" stroke="{border}"/><text x="26" y="35" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="{fg}">Contribution Calendar · {calendar["totalContributions"]} contributions</text><g>{"".join(cells)}</g></svg>'
for theme in ("light","dark"):
    save(f"stats-{theme}.svg", stats(theme))
    save(f"calendar-{theme}.svg", heatmap(theme))
print("Generated 4 SVGs from GitHub GraphQL.")
