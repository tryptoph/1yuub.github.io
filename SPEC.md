# CyberVulnDB — Cybersecurity Intelligence Dashboard

## Project Overview

**Project Name:** CyberVulnDB  
**Version:** 2.0.0  
**Type:** Real-time Cybersecurity Intelligence Dashboard (Browser-only Web Application)  
**Stack:** Vanilla JavaScript, Leaflet.js, CSS3  
**Core Functionality:** Multi-source CVE tracking, ransomware/malware monitoring, APT group intelligence, security news aggregation, and global threat map visualization  
**Target Users:** Security analysts, vulnerability researchers, SOC teams, CTI analysts, threat intelligence researchers  
**Design:** Terminal-inspired cyber aesthetic with dark theme

---

## Architecture

### Tech Stack
- **Frontend:** Vanilla JavaScript (ES6+ IIFE modules, no framework)
- **Styling:** Custom CSS with CSS custom properties (dark theme)
- **Maps:** Leaflet.js with CartoDB dark tiles
- **Fonts:** IBM Plex Mono (mono) + Space Grotesk (display)
- **Data:** 100% client-side — all APIs called directly from browser
- **CORS Strategy:** Direct calls where possible, 3-tier proxy fallback chain (rss2json → allorigins → corsproxy)

### Project Structure
```
cybervulndb/
├── index.html              # App shell — panels, map, modals, dropdowns
├── css/
│   └── style.css           # All styles (~1500 lines, terminal cyber theme)
├── js/
│   ├── app.js              # Main logic — render, events, filters, refresh loops
│   ├── api.js              # All API fetchers, data mapping, caching
│   ├── map.js              # Leaflet map management, markers, popups
│   ├── ui.js               # Toast, loading, export, modal helpers
│   └── utils.js            # Storage, formatting utilities
├── lib/
│   ├── leaflet.js          # Map library (vendored)
│   └── leaflet.css         # Map styles (vendored)
├── data/
│   └── countries.json      # Country geometry for map
├── test_app.py             # Playwright automated tests (6 checks)
└── SPEC.md                 # This specification
```

---

## Current State (v1.x — What's Working)

### ✅ Implemented & Verified
- **CVE Panel:** 3 sources (cvelistV5 real-time, GitHub Advisory, NVD) with source selector dropdown, severity filter, auto-refresh every 2 min, NEW badges, precise time-ago display
- **Ransomware Panel:** Live data from ransomware.live (50 recent victims), group/country/industry display
- **APT Panel:** 15 enriched groups with MITRE ATT&CK data (static, hardcoded)
- **News Panel:** 60+ articles from 10 RSS feeds via proxy chain + HackerNews Algolia API, auto-refresh every 3 min, category filter
- **Threat Map:** Leaflet with markers for all threat types, popups, reset view
- **Search:** Cross-panel full-text search
- **Export:** JSON export of all loaded data
- **UI:** Terminal aesthetic, scanline overlay, severity colors, toast notifications, loading states, responsive layout

### 🟡 Current Limitations
- CVE is the only panel with a data source selector dropdown
- Ransomware panel has only 1 source (ransomware.live)
- APT panel is hardcoded (no live API)
- News panel has no source selector (fetches all feeds)
- No severity categorization per CVE source
- No statistics dashboard or summary cards
- No EPSS exploit prediction enrichment
- No IOC/malware indicator feeds

---

## v2.0 Enhancement Specification

### Goals
1. **10 data sources per category** — CVE, Malware/Ransomware, APT, News
2. **Source selector dropdown on every panel** with "All Sources" as default
3. **Severity filtering per CVE data source**
4. **Auto-fetch from all sources** — parallel loading, newest-first ordering
5. **Enhanced design** — statistics bar, improved cards, source badges, better animations

---

## Data Sources — 10 Per Category

### 1. CVE / Vulnerability Sources

| # | Source | API Endpoint | CORS | Auth | Freshness | Severity Data |
|---|--------|-------------|------|------|-----------|---------------|
| 1 | **CVEProject (cvelistV5)** | `api.github.com/repos/CVEProject/cvelistV5/commits` → `raw.githubusercontent.com` individual JSON | ✅ | None | **Real-time** (0 lag) | CVSSv4 + CVSSv3.1 |
| 2 | **GitHub Advisory DB** | `api.github.com/advisories?type=reviewed&sort=published` | ✅ | None | ~1 day | CVSS from advisory |
| 3 | **NVD (NIST)** | `services.nvd.nist.gov/rest/json/cves/2.0` | ✅ | None (rate-limited) | ~5-7 days | CVSSv3.1 + CVSSv2 |
| 4 | **CVE.org (MITRE)** | `cveawg.mitre.org/api/cve?state=PUBLISHED&time_modified.gt={date}` | ✅ | None | **Real-time** | CVSSv4 + CVSSv3.1 |
| 5 | **OSV.dev (Google)** | `api.osv.dev/v1/query` (POST, query by ecosystem) | ❌ proxy | None | Real-time | CVSS from DB |
| 6 | **CISA KEV** | `cisa.gov/.../known_exploited_vulnerabilities.json` | ❌ proxy | None | Daily | N/A (all are exploited) |
| 7 | **EPSS (FIRST.org)** | `api.first.org/data/v1/epss?cve={id}` | ✅ | None | Daily | Exploit probability score |
| 8 | **Exploit-DB** | `gitlab.com/api/v4/projects/exploit-database%2Fexploitdb/repository/commits` | ✅ | None | Daily | N/A (has exploit code) |
| 9 | **Packet Storm** | RSS: `packetstormsecurity.com/feeds/` | ❌ proxy | None | Daily | N/A |
| 10 | **VulnCheck (Community)** | RSS/JSON feed from vulncheck.com community | ❌ proxy | Free key | Daily | CVSS provided |

**Implementation Notes:**
- **Default:** "All Sources (Merged)" — fetches from sources 1-4 in parallel (fastest, most reliable), deduplicates by CVE ID, sorts newest first, shows 30 results
- **EPSS enrichment:** After loading CVEs from any source, batch-query EPSS scores and overlay as exploit probability badges
- **CISA KEV enrichment:** Cross-reference loaded CVEs against KEV catalog, add "🔥 Exploited" badge
- **Severity per source:** Each source returns its own CVSS data; when merging "All Sources", prefer CVSSv4 > CVSSv3.1 > CVSSv2, take highest score if conflict
- **Rate limiting:** GitHub API = 60 req/hr unauthenticated; NVD = 6 req/sec; CVE.org = generous but undocumented

### 2. Malware / Ransomware Sources

| # | Source | API Endpoint | CORS | Auth | Data Type |
|---|--------|-------------|------|------|-----------|
| 1 | **ransomware.live (Victims)** | `api.ransomware.live/v1/recentvictims` | ❌ proxy | None | Recent ransomware victims (org, group, country) |
| 2 | **ransomware.live (Groups)** | `api.ransomware.live/v1/groups` | ❌ proxy | None | 324 ransomware group profiles |
| 3 | **URLhaus (Abuse.ch)** | `urlhaus.abuse.ch/downloads/json_recent/` | ❌ proxy | None | Malicious URLs (malware distribution) |
| 4 | **ThreatFox (Abuse.ch)** | `threatfox.abuse.ch/export/json/recent/` | ❌ proxy | None | IOCs — domains, IPs, hashes linked to malware |
| 5 | **Feodo Tracker (Abuse.ch)** | `feodotracker.abuse.ch/downloads/ipblocklist.json` | ❌ proxy | None | Botnet C2 server IPs (Dridex, Emotet, TrickBot) |
| 6 | **MalwareBazaar (Abuse.ch)** | `bazaar.abuse.ch/export/csv/recent/` | ❌ proxy | None | Recent malware samples (hashes, family, tags) |
| 7 | **InQuest Labs** | `labs.inquest.net/api/iocdb/list?limit=50` | ✅ | None | IOC database (hashes, YARA rules, references) |
| 8 | **Have I Been Pwned** | `haveibeenpwned.com/api/v3/breaches` | ✅ | None | 600+ data breaches (org, date, count, data types) |
| 9 | **Malware Traffic Analysis** | RSS: `malware-traffic-analysis.net/blog-entries.rss` | ❌ proxy | None | Malware traffic analysis blog posts with IOCs |
| 10 | **ANY.RUN (Public)** | RSS: `any.run/malware-trends/` or public task feed | ❌ proxy | None | Public malware sandbox submissions & trends |

**Implementation Notes:**
- **Default:** "All Sources (Merged)" — fetches sources 1, 3, 4, 7 in parallel (fastest), merges by type
- **Card design:** Unified malware card showing: threat name, type (ransomware/trojan/phishing/botnet/IOC), source badge, time-ago, severity indicator
- **Deduplication:** By IOC value (URL/hash/IP) across sources
- **Country mapping:** ransomware.live provides country codes; URLhaus provides ASN/country; ThreatFox provides reporter country

### 3. APT / Threat Actor Sources

| # | Source | API Endpoint | CORS | Auth | Data Type |
|---|--------|-------------|------|------|-----------|
| 1 | **MISP Galaxy** | `raw.githubusercontent.com/MISP/misp-galaxy/main/clusters/threat-actor.json` | ✅ | None | **953 threat actors** with aliases, country, refs, description |
| 2 | **MITRE ATT&CK (STIX)** | `raw.githubusercontent.com/mitre/cti/master/enterprise-attack/intrusion-set/` or STIX bundle | ✅ | None | Intrusion sets with techniques, software, campaigns |
| 3 | **AlienVault OTX** | `otx.alienvault.com/api/v1/pulses/activity` | ❌ proxy | Free key | Threat pulses, IOCs, targeted countries |
| 4 | **Malpedia** | `malpedia.caad.fkie.fraunhofer.de/api/list/actors` | ❌ proxy | Free key | APT actor profiles with malware families |
| 5 | **MISP Galaxy (Countries)** | `raw.githubusercontent.com/MISP/misp-galaxy/main/clusters/country.json` | ✅ | None | Country-to-actor mapping |
| 6 | **ETDA/ThaiCERT** | `apt.etda.or.th/cgi-bin/listgroups.cgi` | ❌ proxy | None | APT group encyclopedia |
| 7 | **APTnotes** | `raw.githubusercontent.com/aptnotes/data/master/APTnotes.json` | ✅ | None | APT research papers & reports archive |
| 8 | **Mandiant Blog** | RSS: `mandiant.com/resources/blog/rss.xml` | ❌ proxy | None | APT campaign reports |
| 9 | **CrowdStrike Blog** | RSS: `crowdstrike.com/blog/feed/` | ❌ proxy | None | Adversary reports (FANCY BEAR, etc.) |
| 10 | **Kaspersky Securelist** | RSS: `securelist.com/feed/` | ❌ proxy | None | APT campaign analysis |

**Implementation Notes:**
- **Default:** "All Sources (Merged)" — loads MISP Galaxy (953 actors) as primary comprehensive database, enriches with MITRE ATT&CK techniques
- **MISP Galaxy is the star:** 953 actors with countries, aliases, references — replaces the hardcoded 15 actors entirely
- **Sorting:** By last-modified date (if available) or alphabetically; highlight actors with recent campaign activity from RSS sources
- **Actor cards:** Name, aliases, country flag, known malware, target sectors, number of references, last active date
- **Search:** Full-text search across all actor names, aliases, descriptions

### 4. Security News Sources

| # | Source | API / Feed URL | CORS | Auth | Focus |
|---|--------|---------------|------|------|-------|
| 1 | **The Hacker News** | RSS: `feeds.feedburner.com/TheHackersNews` | ❌ proxy | None | Breaking cybersecurity news |
| 2 | **BleepingComputer** | RSS: `bleepingcomputer.com/feed/` | ❌ proxy | None | Malware, vulnerabilities, tech news |
| 3 | **Krebs on Security** | RSS: `krebsonsecurity.com/feed/` | ❌ proxy | None | Investigative cybersecurity journalism |
| 4 | **Dark Reading** | RSS: `darkreading.com/rss.xml` | ❌ proxy | None | Enterprise security news |
| 5 | **SecurityWeek** | RSS: `securityweek.com/feed/` | ❌ proxy | None | Security industry news |
| 6 | **SANS ISC** | RSS: `isc.sans.edu/rssfeed.xml` | ❌ proxy | None | Internet Storm Center diaries |
| 7 | **Schneier on Security** | RSS: `schneier.com/feed/atom/` | ❌ proxy | None | Security analysis & opinion |
| 8 | **Malwarebytes Blog** | RSS: `blog.malwarebytes.com/feed/` | ❌ proxy | None | Malware research |
| 9 | **Threatpost** | RSS: `threatpost.com/feed/` | ❌ proxy | None | Threat intelligence news |
| 10 | **HackerNews (Algolia)** | API: `hn.algolia.com/api/v1/search_by_date?query=security+vulnerability&tags=story` | ✅ | None | Community-curated tech/security stories |

**Implementation Notes:**
- **Default:** "All Sources" — fetches from all 10 in parallel via proxy chain, deduplicates by normalized URL
- **Already working:** All 10 sources are currently implemented and verified
- **Proxy chain:** rss2json.com → allorigins.win → corsproxy.io (3-tier fallback per feed)
- **Category auto-detection:** Classify articles by keyword matching (vulnerabilities, breaches, malware, ransomware, APT, policy)
- **Source badge:** Each news card shows which outlet it came from

---

## Source Selector Dropdowns — All Panels

### Dropdown Specification

Every panel gets a `<select>` source selector in its panel header:

```html
<!-- CVE Panel Header -->
<select id="cve-source-filter" title="CVE data source">
  <option value="all" selected>All Sources (Merged)</option>
  <option value="cvelist">CVEProject (Real-time)</option>
  <option value="github">GitHub Advisory</option>
  <option value="nvd">NVD (NIST)</option>
  <option value="cveorg">CVE.org (MITRE)</option>
  <option value="osv">OSV.dev (Google)</option>
  <option value="kev">CISA KEV (Exploited)</option>
  <option value="exploitdb">Exploit-DB</option>
  <option value="packetstorm">Packet Storm</option>
  <option value="vulncheck">VulnCheck</option>
</select>

<!-- Malware Panel Header -->
<select id="malware-source-filter" title="Malware data source">
  <option value="all" selected>All Sources (Merged)</option>
  <option value="ransomware-victims">Ransomware Victims</option>
  <option value="ransomware-groups">Ransomware Groups</option>
  <option value="urlhaus">URLhaus (Malicious URLs)</option>
  <option value="threatfox">ThreatFox (IOCs)</option>
  <option value="feodo">Feodo Tracker (Botnets)</option>
  <option value="bazaar">MalwareBazaar (Samples)</option>
  <option value="inquest">InQuest Labs (IOCs)</option>
  <option value="phishtank">PhishTank (Phishing)</option>
  <option value="maltraffic">Malware Traffic Analysis</option>
  <option value="anyrun">ANY.RUN (Sandboxes)</option>
</select>

<!-- APT Panel Header -->
<select id="apt-source-filter" title="APT data source">
  <option value="all" selected>All Sources (Merged)</option>
  <option value="misp">MISP Galaxy (953 actors)</option>
  <option value="mitre">MITRE ATT&CK</option>
  <option value="otx">AlienVault OTX</option>
  <option value="malpedia">Malpedia</option>
  <option value="misp-country">MISP (By Country)</option>
  <option value="etda">ThaiCERT/ETDA</option>
  <option value="aptnotes">APTnotes (Papers)</option>
  <option value="mandiant">Mandiant Blog</option>
  <option value="crowdstrike">CrowdStrike Blog</option>
  <option value="securelist">Kaspersky Securelist</option>
</select>

<!-- News Panel Header -->
<select id="news-source-filter" title="News source">
  <option value="all" selected>All Sources</option>
  <option value="hackernews-rss">The Hacker News</option>
  <option value="bleeping">BleepingComputer</option>
  <option value="krebs">Krebs on Security</option>
  <option value="darkreading">Dark Reading</option>
  <option value="securityweek">SecurityWeek</option>
  <option value="sans">SANS ISC</option>
  <option value="schneier">Schneier</option>
  <option value="malwarebytes">Malwarebytes</option>
  <option value="threatpost">Threatpost</option>
  <option value="hn-algolia">HackerNews (Community)</option>
</select>
```

### Dropdown Behavior
- **Default:** "All Sources (Merged)" is selected on every panel
- **On change:** Show loading spinner, fetch from selected source, render results sorted newest-first
- **Count badge:** Tab shows total item count (updates on source change)
- **Toast notification:** "Loaded {N} items from {source}" on each fetch
- **Memory:** Store last-selected source in `localStorage` per panel

---

## Severity Filtering Per CVE Source

### How Severity Works Across Sources

| Source | Severity Data Available | Mapping |
|--------|------------------------|---------|
| cvelistV5 | CVSSv4 baseScore + CVSSv3.1 | Map score → CRITICAL/HIGH/MEDIUM/LOW |
| GitHub Advisory | `severity` field (critical/high/moderate/low) | Direct mapping |
| NVD | CVSSv3.1 metrics in `impact` | Standard CVSS ranges |
| CVE.org | CVSSv4 + CVSSv3.1 in `containers.cna.metrics` | Same as cvelistV5 |
| OSV.dev | `severity` array with CVSS vectors | Parse CVSS vector string |
| CISA KEV | No CVSS (all are critical by nature) | Default to CRITICAL |
| EPSS | Probability score 0-1 | Overlay enrichment, not severity |
| Exploit-DB | No CVSS | Marked as "EXPLOIT" type |
| Packet Storm | No CVSS | Unscored |
| VulnCheck | CVSS provided | Standard mapping |

### CVSS Score → Severity Mapping
```
CRITICAL: score >= 9.0
HIGH:     score >= 7.0
MEDIUM:   score >= 4.0
LOW:      score >  0.0
NONE:     score == 0 or missing
```

### Merged Severity Resolution
When "All Sources" is selected and a CVE appears in multiple sources:
1. Prefer CVSSv4 score over CVSSv3.1 over CVSSv2
2. If same version, take the higher score
3. Add source indicator showing which sources have this CVE

---

## Auto-Fetch & Refresh Strategy

### Initial Load
```
Page load → Promise.all([
  fetchAllCVESources()     // 4 primary CVE APIs in parallel
  fetchAllMalware()        // ransomware.live + URLhaus + ThreatFox + InQuest
  fetchAllAPT()            // MISP Galaxy (primary) + enrichment
  fetchAllNews()           // 10 RSS feeds in parallel via proxy chain
])
→ Render all panels
→ Plot map markers
→ Start refresh timers
```

### Refresh Intervals
| Category | Refresh Interval | Strategy |
|----------|-----------------|----------|
| CVE | Every 2 minutes | Fetch from primary source (cvelistV5), check for new IDs, show NEW badge |
| Malware | Every 3 minutes | Fetch ransomware.live victims + URLhaus recent |
| APT | Every 30 minutes | MISP Galaxy rarely changes; RSS feeds for latest reports |
| News | Every 3 minutes | Fetch all RSS feeds, deduplicate, prepend new items |

### Caching
- **localStorage cache:** 15-minute TTL for full dataset, keyed by version (`cybervulndb_data_v{N}`)
- **Per-source cache:** Individual source results cached separately for faster source switching
- **Cache invalidation:** Bump version key when source list changes; clear on manual refresh

---

## Design Enhancements (v2.0)

### 1. Statistics Bar (New)
Add a horizontal stats bar between header and main content:
```
┌──────────────────────────────────────────────────────────────────┐
│  ⚡ 95 CVEs  │  ⚠ 50 Attacks  │  ◎ 953 APT Groups  │  ◉ 60 News  │
│  12 CRITICAL  │  8 Countries   │  15 Active          │  3 min ago   │
└──────────────────────────────────────────────────────────────────┘
```
- Animated counters on initial load
- Click a stat to switch to that panel
- Severity mini-bar under CVE count (colored segments for CRIT/HIGH/MED/LOW)

### 2. Source Badges on Cards
Every threat card shows a small source badge:
```
┌─────────────────────────────────────────┐
│ [CVE] [cvelistV5]              2h ago   │
│ CVE-2026-3741 — YiFang CMS 2.0.5...   │
│ ████ MEDIUM 5.1  │  EPSS: 23%          │
└─────────────────────────────────────────┘
```
- Source badge color-coded per provider
- EPSS probability shown as percentage when available
- "🔥 KEV" badge if in CISA Known Exploited list

### 3. Enhanced Card Design
- **Glassmorphism effect:** Subtle frosted glass on hover
- **Source color stripe:** Left border color matches source provider
- **Expandable preview:** Click to expand inline before opening modal
- **Severity gradient:** Background gradient intensity based on severity
- **Pulse animation:** Cards with CRITICAL severity pulse gently

### 4. Improved Panel Headers
```
┌─────────────────────────────────────────┐
│ // Latest CVEs              Updated 2m │
│ [Source: All ▾] [Severity ▾] [30 items]│
└─────────────────────────────────────────┘
```
- Source dropdown + severity filter + item count on one line
- Last-updated timestamp
- Loading indicator (spinning ⟳) during fetch

### 5. Map Enhancements
- **Marker clustering:** Group nearby markers with count badges
- **Heatmap layer:** Toggle between markers and heatmap
- **Source filter on map:** Show/hide markers by category or source
- **Animated markers:** New threats appear with pulse animation
- **Country highlight:** Click a country to filter all panels by that country

### 6. Dark/Light Theme Toggle (Optional)
- Toggle button in header
- Light theme with adjusted colors for readability
- Store preference in localStorage

### 7. Activity Timeline (Sidebar Bottom)
Scrolling real-time feed of latest events across all categories:
```
16:05  ⚡ CVE-2026-3741 published (MEDIUM 5.1)
16:03  ⚠ LockBit claimed victim in DE
16:01  ◉ New article: "Zero-day in..."
15:58  ⚡ CVE-2026-3740 published (MEDIUM 6.9)
```

### 8. Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `1-4` | Switch to panel (CVE/Ransom/News/APT) |
| `r` | Refresh all data |
| `s` | Focus search bar |
| `Esc` | Close modal |
| `?` | Show keyboard shortcuts |

---

## Data Models (v2.0)

### Unified Threat Item
```javascript
{
  id: "CVE-2026-3741",
  type: "cve" | "malware" | "ransomware" | "apt" | "news" | "ioc" | "phishing",
  source: "cvelist" | "github" | "nvd" | "cveorg" | "urlhaus" | ...,
  title: "YiFang CMS 2.0.5 SQL Injection",
  description: "A security vulnerability has been detected...",
  published: "2026-03-08T14:32:10.515Z",
  severity: { score: 5.1, level: "MEDIUM", vector: "CVSS:4.0/..." },
  epss: { score: 0.23, percentile: 0.84 },          // if enriched
  kev: true,                                          // if in CISA KEV
  country: "US",
  coords: [38.9, -77.0],
  url: "https://...",
  tags: ["sql-injection", "web", "cms"],
  meta: { /* source-specific fields */ }
}
```

### Source Health Status
```javascript
{
  id: "cvelist",
  name: "CVEProject (cvelistV5)",
  status: "ok" | "degraded" | "error",
  lastFetch: "2026-03-08T16:05:00Z",
  itemCount: 35,
  latency: 1200,  // ms
  error: null
}
```

---

## Implementation Phases

### Phase 1: Multi-Source CVE (Expand from 3 → 6 core sources)
- Add CVE.org (cveawg.mitre.org) fetcher
- Add EPSS enrichment (batch query after CVE load)
- Add CISA KEV badge enrichment
- Change default to "All Sources"
- Wire severity filter per source
- Update dropdown with all options

### Phase 2: Multi-Source Malware (Replace single source → 5+ sources)
- Add URLhaus fetcher (JSON download feed)
- Add ThreatFox fetcher (IOC export)
- Add InQuest Labs fetcher
- Add source dropdown to ransomware panel (rename to "Malware/Ransom")
- Unified malware card design
- Auto-refresh every 3 min

### Phase 3: Live APT Intelligence (Replace hardcoded → live APIs)
- Add MISP Galaxy fetcher (953 actors from GitHub raw)
- Parse and display actor cards with country, aliases, refs
- Add source dropdown to APT panel
- Add APT-related RSS feeds (Mandiant, CrowdStrike, Securelist)
- Search across all actor names and aliases

### Phase 4: News Source Selector
- Replace category filter with source filter dropdown
- Allow filtering by individual news outlet
- Keep "All Sources" as default
- Add item count to tab badge

### Phase 5: Design Enhancements
- Add statistics bar
- Add source badges on all cards
- EPSS probability display
- KEV badge display
- Enhanced card hover effects
- Loading spinners per panel
- Activity timeline
- Keyboard shortcuts

### Phase 6: Testing & Polish
- Update Playwright tests for new dropdowns
- Test all source combinations
- Performance optimization (lazy loading, virtual scrolling for large lists)
- Error handling for offline/degraded sources
- Bump version strings and cache keys

---

## API Rate Limits & Constraints

| API | Rate Limit | Strategy |
|-----|-----------|----------|
| GitHub API (cvelistV5, Advisory) | 60 req/hr unauthenticated | Cache aggressively, combine calls |
| NVD | 6 req/sec (5 without API key) | Single query per refresh |
| CVE.org | Undocumented (generous) | Reasonable polling |
| OSV.dev | Undocumented (generous) | Cache results |
| EPSS | Undocumented | Batch queries, cache 1hr |
| ransomware.live | Undocumented | Cache 5 min |
| Abuse.ch feeds | Public downloads, no limit | Cache 10 min |
| InQuest Labs | Undocumented | Cache 10 min |
| RSS feeds | N/A (static files) | Cache 3 min |
| MISP Galaxy (GitHub raw) | CDN-cached | Cache 30 min |

---

## Testing

### Automated Tests (test_app.py)
1. ✅ Page loads with all panels
2. ✅ CVE cards render (30+ items)
3. ✅ Status bar shows connected
4. ✅ Threat counter matches data
5. ✅ Modal opens on CVE click
6. ✅ Modal closes correctly
7. 🆕 Source dropdown changes CVE source
8. 🆕 Malware panel loads data
9. 🆕 APT panel shows actors
10. 🆕 All source selectors functional

### Manual Test Matrix
- [ ] Each CVE source individually
- [ ] Each malware source individually
- [ ] Each APT source individually
- [ ] Each news source individually
- [ ] "All Sources" for each panel
- [ ] Severity filter with each CVE source
- [ ] Search across all panels
- [ ] Export with multi-source data
- [ ] Map markers from all sources
- [ ] Auto-refresh with source selections preserved

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-07 | Initial vanilla JS implementation |
| 1.0.1 | 2026-03-08 | Terminal aesthetic, sorting, auto-refresh |
| 1.0.2 | 2026-03-08 | Live news feeds (60+ articles, 10 RSS sources) |
| 1.0.3 | 2026-03-08 | Real-time CVEs (cvelistV5), GitHub Advisory, precise time-ago |
| 1.0.4 | 2026-03-08 | Live ransomware (ransomware.live), enriched APT (15 groups) |
| 1.0.5 | 2026-03-08 | CVE source selector dropdown, severity per source |
| **2.0.0** | **TBD** | **Multi-source all panels, design refresh (this spec)** |

---

## References

### CVE / Vulnerability
- NVD API: https://services.nvd.nist.gov/rest/json/cves/2.0
- CVEProject: https://github.com/CVEProject/cvelistV5
- CVE.org API: https://cveawg.mitre.org/api-docs
- GitHub Advisory: https://docs.github.com/en/rest/security-advisories
- OSV.dev: https://osv.dev/docs/
- EPSS: https://www.first.org/epss/api
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### Malware / Ransomware
- ransomware.live: https://www.ransomware.live/
- Abuse.ch URLhaus: https://urlhaus.abuse.ch/api/
- Abuse.ch ThreatFox: https://threatfox.abuse.ch/api/
- Abuse.ch Feodo: https://feodotracker.abuse.ch/
- Abuse.ch MalwareBazaar: https://bazaar.abuse.ch/
- InQuest Labs: https://labs.inquest.net/

### APT / Threat Actors
- MISP Galaxy: https://github.com/MISP/misp-galaxy
- MITRE ATT&CK: https://attack.mitre.org/
- Malpedia: https://malpedia.caad.fkie.fraunhofer.de/

### News
- HackerNews Algolia: https://hn.algolia.com/api

### Tools
- Leaflet.js: https://leafletjs.com/
- Playwright: https://playwright.dev/
