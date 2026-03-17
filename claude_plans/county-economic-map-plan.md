# County Economic Health Map — Implementation Handoff Plan
**For: SeattleWren.com | Target path: `/data/economic-health`**

---

## Objective

Build a national county-level interactive choropleth map with a metric toggle covering:
- Unemployment rate
- Median household income
- Income after housing (disposable income proxy)
- Per capita income

Single React component, one Census API call, localStorage caching, canvas rendering for performance.

---

## Single API Call — Fetch Everything at Once

```
GET https://api.census.gov/data/2023/acs/acs5
  ?get=NAME,
       B23025_001E,
       B23025_005E,
       B19013_001E,
       B19301_001E,
       B25105_001E
  &for=county:*
  &in=state:*
  &key=YOUR_CENSUS_KEY
```

### Variable Reference

| Variable | Table | Description |
|---|---|---|
| `B23025_001E` | B23025 | Total civilian population 16+ |
| `B23025_005E` | B23025 | Civilian unemployed |
| `B19013_001E` | B19013 | Median household income (12 months) |
| `B19301_001E` | B19301 | Per capita income (12 months) |
| `B25105_001E` | B25105 | Median monthly housing costs |

### Computed Fields (client-side)

```js
const unemploymentRate  = B23025_005E / B23025_001E * 100;
const annualHousingCost = B25105_001E * 12;
const incomeAfterHousing = B19013_001E - annualHousingCost;  // disposable proxy
const perCapitaIncome   = B19301_001E;
const medianIncome      = B19013_001E;
```

### Null Handling Rules

```js
// Census returns -666666666 for suppressed/missing data
const clean = v => (v === null || v == -666666666 || v < 0) ? null : +v;
```

Any county where the computed metric is `null` renders as `#D3D1C7` (neutral gray) with tooltip text "Data not available."

---

## Topology Source

```
https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json
```

- ~100KB gzipped
- Feature `.id` values are numeric 5-digit FIPS (e.g. `53033` for King County WA)
- Match to Census API response by concatenating `state + county` columns: `state.padStart(2,'0') + county.padStart(3,'0')`

---

## Caching Strategy

```js
// useCountyData.js
const CACHE_KEY = 'seattlewren_county_econ_v1';
const CACHE_TTL = 7 * 24 * 60 * 60 * 1000; // 7 days in ms

async function fetchWithCache() {
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      const { timestamp, data } = JSON.parse(cached);
      if (Date.now() - timestamp < CACHE_TTL) return data;
    }
  } catch(e) {}

  const [topoRes, censusRes] = await Promise.all([
    fetch('https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json'),
    fetch(`https://api.census.gov/data/2023/acs/acs5?get=NAME,B23025_001E,B23025_005E,B19013_001E,B19301_001E,B25105_001E&for=county:*&in=state:*&key=${import.meta.env.VITE_CENSUS_KEY}`)
  ]);

  const [topo, censusRaw] = await Promise.all([topoRes.json(), censusRes.json()]);

  // Build lookup: fips -> computed metrics
  const [header, ...rows] = censusRaw;
  const lookup = {};
  rows.forEach(row => {
    const obj = Object.fromEntries(header.map((k,i) => [k, row[i]]));
    const fips = obj.state.padStart(2,'0') + obj.county.padStart(3,'0');
    const clean = v => (v === null || +v < -1) ? null : +v;
    const totalPop  = clean(obj.B23025_001E);
    const unemp     = clean(obj.B23025_005E);
    const medIncome = clean(obj.B19013_001E);
    const pcIncome  = clean(obj.B19301_001E);
    const housing   = clean(obj.B25105_001E);
    lookup[fips] = {
      name: obj.NAME,
      fips,
      totalPop,
      unemp,
      unemploymentRate: totalPop ? unemp / totalPop * 100 : null,
      medianIncome: medIncome,
      perCapitaIncome: pcIncome,
      monthlyHousing: housing,
      annualHousing: housing ? housing * 12 : null,
      incomeAfterHousing: (medIncome && housing) ? medIncome - (housing * 12) : null,
    };
  });

  const data = { topo, lookup };

  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ timestamp: Date.now(), data }));
  } catch(e) {}

  return data;
}
```

---

## Component File Structure

```
src/
  components/
    EconomicMap/
      index.jsx           ← page wrapper, data fetch, metric state
      MapCanvas.jsx       ← D3 canvas choropleth + hit detection
      HitCanvas.jsx       ← invisible canvas for mousemove county lookup
      Tooltip.jsx         ← hover card
      Legend.jsx          ← quantile color scale bar + labels
      MetricToggle.jsx    ← 4-button toggle strip
      StateFilter.jsx     ← dropdown, triggers fitExtent zoom
      SummaryStats.jsx    ← top 3 metric cards (state avg, highest, lowest)
      RankingTable.jsx    ← top 10 / bottom 10 for active metric
      useCountyData.js    ← fetch + cache hook (see above)
      constants.js        ← color scales, metric config, formatters
  pages/
    economic-health.jsx   ← route wrapper, imports EconomicMap
```

---

## Metric Configuration (constants.js)

```js
export const METRICS = {
  unemploymentRate: {
    label: 'Unemployment Rate',
    description: 'Civilian unemployed as % of population 16+',
    source: 'ACS B23025',
    format: v => v == null ? 'N/A' : `${v.toFixed(1)}%`,
    // For unemployment: low is GOOD, so reverse the color scale
    colorStops: ['#1D9E75','#9FE1CB','#E1F5EE','#EF9F27','#BA7517','#E24B4A','#A32D2D'],
    direction: 'lower-is-better',
  },
  medianIncome: {
    label: 'Median Household Income',
    description: 'Median household income, past 12 months',
    source: 'ACS B19013',
    format: v => v == null ? 'N/A' : `$${Math.round(v).toLocaleString()}`,
    colorStops: ['#A32D2D','#E24B4A','#BA7517','#EF9F27','#E1F5EE','#9FE1CB','#1D9E75'],
    direction: 'higher-is-better',
  },
  incomeAfterHousing: {
    label: 'Income After Housing',
    description: 'Median household income minus annual housing costs',
    source: 'ACS B19013 + B25105',
    format: v => v == null ? 'N/A' : `$${Math.round(v).toLocaleString()}`,
    colorStops: ['#A32D2D','#E24B4A','#BA7517','#EF9F27','#E1F5EE','#9FE1CB','#1D9E75'],
    direction: 'higher-is-better',
    nullNote: 'Housing cost data unavailable for some rural counties',
  },
  perCapitaIncome: {
    label: 'Per Capita Income',
    description: 'Total income divided by total population',
    source: 'ACS B19301',
    format: v => v == null ? 'N/A' : `$${Math.round(v).toLocaleString()}`,
    colorStops: ['#A32D2D','#E24B4A','#BA7517','#EF9F27','#E1F5EE','#9FE1CB','#1D9E75'],
    direction: 'higher-is-better',
  },
};
```

---

## Canvas Rendering Pattern

Use TWO canvas elements stacked — one visible, one hidden for hit detection:

```jsx
// MapCanvas.jsx — simplified
import * as d3 from 'd3';
import * as topojson from 'topojson-client';

export function MapCanvas({ topo, lookup, metric, onHover }) {
  const visRef = useRef();
  const hitRef = useRef();
  // hitColors[i] = fips string, so we can reverse-lookup on mousemove
  const hitIndex = useRef([]);

  useEffect(() => {
    const features = topojson.feature(topo, topo.objects.counties).features
      .filter(f => f.id); // skip features without FIPS

    const w = visRef.current.offsetWidth;
    const h = Math.round(w * 0.6);
    [visRef, hitRef].forEach(r => {
      r.current.width = w;
      r.current.height = h;
    });

    const projection = d3.geoAlbersUsa().fitSize([w, h], {
      type: 'FeatureCollection', features
    });
    const path = d3.geoPath(projection);

    const visCtx = visRef.current.getContext('2d');
    const hitCtx = hitRef.current.getContext('2d');

    const metricConfig = METRICS[metric];
    const values = features
      .map(f => lookup[String(f.id).padStart(5,'0')]?.[metric])
      .filter(v => v != null);

    const colorScale = d3.scaleQuantile()
      .domain(values)
      .range(metricConfig.colorStops);

    hitIndex.current = [];

    features.forEach((f, i) => {
      const fips = String(f.id).padStart(5,'0');
      const county = lookup[fips];
      const value = county?.[metric];

      // Visible canvas
      visCtx.beginPath();
      path.context(visCtx)(f);
      visCtx.fillStyle = value != null ? colorScale(value) : '#D3D1C7';
      visCtx.fill();
      visCtx.strokeStyle = 'rgba(255,255,255,0.5)';
      visCtx.lineWidth = 0.3;
      visCtx.stroke();

      // Hit canvas: unique color per county (index encoded as RGB)
      const r = (i >> 16) & 0xff;
      const g = (i >> 8) & 0xff;
      const b = i & 0xff;
      hitCtx.beginPath();
      path.context(hitCtx)(f);
      hitCtx.fillStyle = `rgb(${r},${g},${b})`;
      hitCtx.fill();

      hitIndex.current[i] = fips;
    });
  }, [topo, lookup, metric]);

  function handleMouseMove(e) {
    const rect = hitRef.current.getBoundingClientRect();
    const x = Math.round((e.clientX - rect.left) * (hitRef.current.width / rect.width));
    const y = Math.round((e.clientY - rect.top) * (hitRef.current.height / rect.height));
    const [r,g,b] = hitRef.current.getContext('2d').getImageData(x, y, 1, 1).data;
    const idx = (r << 16) | (g << 8) | b;
    const fips = hitIndex.current[idx];
    onHover(fips ? { fips, county: lookup[fips], x: e.clientX, y: e.clientY } : null);
  }

  return (
    <div style={{ position: 'relative' }}>
      <canvas ref={visRef} style={{ width: '100%', display: 'block' }} />
      <canvas ref={hitRef}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', opacity: 0, pointerEvents: 'none' }}
        onMouseMove={handleMouseMove}
        onMouseLeave={() => onHover(null)}
      />
    </div>
  );
}
```

---

## Tooltip Content Per Metric

```jsx
// Tooltip.jsx
function Tooltip({ county, metric }) {
  if (!county) return null;
  const cfg = METRICS[metric];
  return (
    <div className="tooltip">
      <div className="tt-name">{county.name}</div>
      <div className="tt-primary">{cfg.label}: <strong>{cfg.format(county[metric])}</strong></div>
      {metric === 'incomeAfterHousing' && (
        <>
          <div className="tt-detail">Median income: {METRICS.medianIncome.format(county.medianIncome)}</div>
          <div className="tt-detail">Annual housing: {county.annualHousing ? `$${Math.round(county.annualHousing).toLocaleString()}` : 'N/A'}</div>
        </>
      )}
      {metric === 'unemploymentRate' && (
        <div className="tt-detail">
          {county.unemp?.toLocaleString()} unemployed / {county.totalPop?.toLocaleString()} total
        </div>
      )}
    </div>
  );
}
```

---

## State Filter + Zoom

```js
// StateFilter.jsx — zoom map to selected state
function zoomToState(stateFips, features, projection, canvas) {
  const stateFeatures = features.filter(f =>
    String(f.id).padStart(5,'0').startsWith(stateFips)
  );
  const collection = { type: 'FeatureCollection', features: stateFeatures };
  const w = canvas.width;
  const h = canvas.height;
  projection.fitExtent([[20, 20], [w-20, h-20]], collection);
  // then re-render
}
```

State FIPS reference: build a `STATE_FIPS` lookup from the Census response — each row already has `state` and `NAME` columns, so extract unique states dynamically rather than hardcoding.

---

## Page Layout (economic-health.jsx)

```jsx
export default function EconomicHealth() {
  return (
    <div className="page-container">
      <h2>County Economic Health</h2>
      <p className="subtitle">
        National county-level data from the U.S. Census ACS 5-year estimates (2023).
        Income after housing subtracts annual housing costs from median household income
        as a proxy for disposable income.
      </p>

      <MetricToggle />          {/* 4 buttons */}
      <StateFilter />           {/* dropdown + reset */}
      <SummaryStats />          {/* 3 metric cards */}
      <MapCanvas />             {/* main map */}
      <Legend />                {/* color scale */}
      <RankingTable />          {/* top 10 / bottom 10 */}

      <p className="data-note">
        Source: U.S. Census Bureau, American Community Survey 5-Year Estimates, 2023.
        Tables B23025, B19013, B19301, B25105. "Income after housing" is a calculated
        field (median household income minus annualized median monthly housing costs)
        and is not an official Census measure.
      </p>
    </div>
  );
}
```

---

## Dependencies

```bash
npm install d3 topojson-client
```

If `d3` is already installed from the unemployment map build, only `topojson-client` may be needed.

---

## Environment Variable

Add to `.env` (and `.env.example` with a placeholder):

```
VITE_CENSUS_KEY=your_key_here
```

Get a free key at: https://api.census.gov/data/key_signup.html

---

## Prompt for Claude Desktop

> In the SeattleWren repo, build the County Economic Health map component described in the attached plan. Key requirements:
>
> 1. Create `src/components/EconomicMap/` with the file structure in the plan
> 2. Single Census ACS5 API call fetching B23025 (unemployment), B19013 (median income), B19301 (per capita income), B25105 (housing costs) for all counties in all states
> 3. Cache both the Census response and the us-atlas topology in localStorage with a 7-day TTL under key `seattlewren_county_econ_v1`
> 4. Render using TWO stacked canvas elements — visible canvas for display, invisible hit canvas for mousemove county detection (index-encoded RGB pattern)
> 5. Color scale: `d3.scaleQuantile()` with 7 stops, direction-aware (unemployment reverses the ramp)
> 6. Metric toggle: Unemployment Rate / Median Income / Income After Housing / Per Capita Income
> 7. State filter dropdown that calls `projection.fitExtent()` to zoom to selected state
> 8. Tooltip showing metric value + supporting detail fields per metric config
> 9. Ranking table (top 10 / bottom 10) that updates when metric changes
> 10. Route the page to `/data/economic-health`
> 11. Census API key from `import.meta.env.VITE_CENSUS_KEY`
> 12. Null/suppressed Census values (-666666666) render as neutral gray `#D3D1C7`
>
> All metric configs, color scales, and formatters should live in `constants.js` so future metrics can be added by editing one file.

---

## Post-Launch Content Ideas

Once the map is live, each of these is a standalone Musing post:

- **"The Housing Trap"** — map of income after housing, highlighting counties where housing consumes >40% of median income
- **"Where Jobs Are Disappearing"** — unemployment rate map filtered to post-2019 change (requires pulling 2019 vintage for comparison)
- **"The Wage Illusion"** — side-by-side of median income vs per capita income, showing where household size skews the story
- **"Woodinville in Context"** — zoom to King/Snohomish, annotate local counties, personalize for your audience

---

*Plan version 1.0 — generated for SeattleWren.com*
