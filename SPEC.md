# CyberVulnDB - Cybersecurity Intelligence Dashboard

## Project Overview

**Project Name:** CyberVulnDB  
**Type:** Real-time Cybersecurity Intelligence Dashboard (Web Application)  
**Current Implementation:** Vanilla JavaScript (originally planned as Next.js)
**Core Functionality:** CVE tracking, ransomware monitoring, APT intelligence, security news aggregation, and threat visualization
**Target Users:** Security analysts, vulnerability researchers, SOC teams, CTI analysts

---

## Implementation History

### Original Plan (from SPEC.md v1)
- **Stack:** Next.js 14+ with TypeScript, React 18+
- **Styling:** CSS Modules with CSS Variables
- **State Management:** Zustand
- **Maps:** globe.gl + Three.js (3D), deck.gl + MapLibre (2D)
- **AI:** Ollama (local) / Groq (cloud) / Transformers.js fallback

### What Was Actually Built
- **Stack:** Vanilla JavaScript (no framework)
- **Styling:** Custom CSS with CSS Variables
- **Maps:** Leaflet.js with OpenStreetMap/CartoDB tiles
- **Data:** NVD API 2.0, fallback static data, mock ransomware/APT data

---

## Current Project Structure

```
cybervulndb/
├── index.html              # Main HTML entry point
├── css/
│   └── style.css          # All styles (terminal-inspired cyber aesthetic)
├── js/
│   ├── app.js             # Main application logic (render, events, init)
│   ├── api.js             # API clients (NVD, RSS, fallback data)
│   ├── map.js             # Leaflet map management
│   ├── ui.js              # UI interactions (toast, loading, export)
│   └── utils.js           # Utility functions (storage, formatting)
├── lib/
│   ├── leaflet.js         # Map library
│   └── leaflet.css        # Map styles
└── SPEC.md                # This specification
```

---

## Features Implemented

### ✅ Working Features

1. **CVE Tracking**
   - Fetches from NVD API 2.0
   - Fallback static data with recent CVEs
   - Severity filter dropdown (CRITICAL/HIGH/MEDIUM/LOW)
   - Sort by date (newest first)
   - Click to view CVE details in modal

2. **Ransomware Monitor**
   - Mock data for ransomware victims
   - Group, country, sector display
   - Click to view details in modal

3. **APT Intelligence**
   - Mock data for APT groups
   - Aliases, country, target sectors
   - Click to view details in modal

4. **Security News**
   - RSS feed fetching (with CORS proxy)
   - Category filtering
   - Opens in new tab

5. **Threat Map**
   - Leaflet.js map
   - Markers for CVEs, ransomware, APT
   - Popup details on click
   - Reset view button

6. **Auto-Refresh**
   - Data refreshes every 5 minutes
   - Manual refresh button

7. **Search**
   - Search across CVEs, ransomware, APT, news

8. **Export**
   - Export data as JSON

9. **UI/UX**
   - Terminal-inspired cyber aesthetic
   - IBM Plex Mono + Space Grotesk fonts
   - Scanline overlay effect
   - Dark theme with cyan accents
   - Severity color coding
   - Responsive design
   - Toast notifications

---

## Current Issues (Bugs to Fix)

### 🔴 Critical Issues

1. **CVEs Not Rendering in UI**
   - Status: NVD API returns data but render function not executing properly
   - Console shows: `[API] Fetched 20 CVEs from NVD` but `window.cyberData` is null
   - Issue: Async/await problem in `renderCVEs()` function - it's now async but the caller isn't awaiting properly

2. **Click Handlers Not Working**
   - CVE cards not clickable to open modal
   - Likely related to the async rendering issue

### 🟡 Known Limitations

1. **NVD API Reliability**
   - Sometimes returns old CVEs instead of latest
   - Fallback data is used as backup

2. **RSS Feeds**
   - Many feeds fail due to CORS
   - Limited to working feeds only

3. **Map Markers**
   - CVE coordinates are estimated from description text
   - Not all CVEs have location data

---

## Data Sources

### CVE Data
- **Primary:** NVD API 2.0 (`https://services.nvd.nist.gov/rest/json/cves/2.0`)
- **Fallback:** Static JSON with verified recent CVEs
- **KEV:** CISA KEV Catalog (planned)

### Ransomware Data
- **Current:** Mock data (static JSON)
- **Planned:** RansomDB API, ransomware group leak sites

### APT Data
- **Current:** Mock data (static JSON)
- **Planned:** MITRE ATT&CK API

### News Data
- **Current:** RSS feeds via CORS proxy
- **Planned:** Add more reliable feeds

---

## UI/UX Specification (Current)

### Color Palette (Terminal Cyber Theme)
```css
:root {
  /* Backgrounds */
  --bg-primary: #050508;
  --bg-secondary: #0a0c10;
  --bg-card: #0d1018;
  --bg-elevated: #12161f;
  
  /* Text */
  --text-primary: #e4e4e7;
  --text-secondary: #9ca3af;
  --text-muted: #52525b;
  
  /* Accents */
  --accent-cyan: #00ffd5;
  --accent-green: #39ff14;
  --accent-red: #ff2d55;
  
  /* Severity */
  --critical: #ff2d55;
  --high: #ff9500;
  --medium: #ffcc00;
  --low: #30d158;
  --info: #64d2ff;
  
  /* Threat Types */
  --ransomware: #ff375f;
  --apt: #bf5af2;
  --cve: #ffcc00;
}
```

### Typography
- **Primary Font:** IBM Plex Mono (monospace)
- **Display Font:** Space Grotesk (headings)

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Logo | Search Bar | Refresh | Export                    │
├────────────┬────────────────────────────────────────────────────┤
│            │                                                     │
│  SIDEBAR   │                   MAP                             │
│            │                                                     │
│ [CVE]      │         (Leaflet Interactive Map)                  │
│ [RANSOM]   │                                                     │
│ [NEWS]     │                                                     │
│ [APT]      │                                                     │
│            │                                                     │
├────────────┴────────────────────────────────────────────────────┤
│ FOOTER: Status | Last Updated | Threat Count                   │
└─────────────────────────────────────────────────────────────────┘
```

### Components
- Tab navigation for sidebar panels
- Threat cards with severity badges
- Modal dialogs for details
- Toast notifications
- Loading overlay
- Map legend

---

## What's Been Done (Detailed)

### Phase 1: Basic Setup
- ✅ Created vanilla JS project structure
- ✅ Set up HTML with semantic structure
- ✅ Created CSS with cyber theme
- ✅ Integrated Leaflet.js map

### Phase 2: API Integration
- ✅ NVD API client with caching
- ✅ Fallback data for CVEs
- ✅ Mock data for ransomware/APT
- ✅ RSS feed fetching with CORS proxy

### Phase 3: UI Features
- ✅ Tab navigation
- ✅ Severity filtering
- ✅ Search functionality
- ✅ Modal system
- ✅ Toast notifications
- ✅ Export feature

### Phase 4: Visual Design
- ✅ Terminal-inspired aesthetic
- ✅ Custom color palette
- ✅ Animations and transitions
- ✅ Responsive design

### Phase 5: Bug Fixes (In Progress)
- 🔄 Fixed async/await in renderCVEs
- 🔄 Added auto-refresh interval
- 🔄 Fixed modal close functionality
- 🔄 Added z-index fixes for clickable elements

---

## What Still Needs to Be Done

### Immediate Priorities
1. **Fix CVE rendering** - Ensure CVEs display in the sidebar
2. **Fix click handlers** - Make CVE cards open modal on click
3. **Verify auto-refresh** - Confirm data refreshes every 5 minutes

### Short-term Features
4. **CISA KEV Integration** - Add known exploited vulnerabilities indicator
5. **Better fallback data** - More comprehensive static CVE data
6. **Improved RSS feeds** - Find more reliable CORS-enabled feeds
7. **Map improvements** - Better marker clustering, heatmap layer

### Medium-term Features
8. **EPSS Scoring** - Add Exploit Prediction Scoring System data
9. **More ransomware data** - Real API integration
10. **APT technique matrix** - MITRE ATT&CK visualization

### Long-term Features (Original Spec)
11. **AI Summaries** - Ollama/Groq integration for threat briefs
12. **3D Globe** - Upgrade from Leaflet to globe.gl
13. **User preferences** - Theme toggle, custom feeds

---

## API Specifications

### NVD API 2.0
```
GET https://services.nvd.nist.gov/rest/json/cves/2.0
Parameters:
  - pubStartDate: ISO 8601
  - pubEndDate: ISO 8601
  - cvssV3Severity: CRITICAL|HIGH|MEDIUM|LOW
  - resultsPerPage: number (1-2000)
Rate Limit: 6 requests per second
```

### CISA KEV Catalog
```
GET https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
```

### RSS Feeds (Working)
- The Hacker News: `https://feeds.feedburner.com/TheHackersNews`
- Krebs on Security: `https://krebsonsecurity.com/feed/`

---

## Data Models

### CVE
```javascript
{
  id: "CVE-2026-30823",
  description: "Flowise before 3.0.13 IDOR vulnerability...",
  published: "2026-03-07T06:16:00.000Z",
  cvss: {
    score: 8.8,
    severity: "HIGH",
    vector: "CVSS:3.1"
  },
  type: "cve"
}
```

### RansomwareVictim
```javascript
{
  id: "r1",
  organization: "Tech Corp",
  group: "LockBit",
  country: "US",
  countryCode: "US",
  sector: "Technology",
  discovered: "2026-03-01",
  status: "published"
}
```

### APTGroup
```javascript
{
  id: "apt29",
  name: "Cozy Bear",
  aliases: ["APT29", "The Dukes", "CozyDuke"],
  country: "RU",
  targetSectors: ["Government", "Healthcare", "Energy"],
  description: "..."
}
```

---

## Dependencies

### Current (Vanilla JS)
```json
{
  "leaflet": "^1.9.4"
}
```

### Original Plan (Not Implemented)
```json
{
  "next": "^14.0.0",
  "react": "^18.2.0",
  "typescript": "^5.3.0",
  "zustand": "^4.4.0",
  "globe.gl": "^2.27.0",
  "rss-parser": "^3.13.0"
}
```

---

## Testing

### Current Testing Approach
- Playwright for automated testing
- Manual browser testing
- Console log debugging

### Test Coverage
- ✅ Page load
- ✅ API calls
- ✅ Data rendering
- 🔄 Click handlers (broken)
- 🔄 Modal functionality (broken)

---

## Future Considerations

### Migration Back to Next.js (Optional)
If the project grows, consider migrating back to Next.js:
- Better code organization
- Server-side rendering
- API routes for proxying
- TypeScript support

### Potential Enhancements
- PWA support for offline viewing
- User accounts for personalized feeds
- Email alerts for new CVEs
- Slack/Discord integrations
- Real-time WebSocket updates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-07 | Initial vanilla JS implementation |
| 1.0.1 | 2026-03-08 | Added terminal aesthetic, fixed sorting, added auto-refresh |
| 1.0.2 | 2026-03-08 | Fixed async issues in renderCVEs (in progress) |

---

## References

- NVD API: https://services.nvd.nist.gov/rest/json/cves/2.0
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Leaflet Docs: https://leafletjs.com/
- MITRE ATT&CK: https://attack.mitre.org/
