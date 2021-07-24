import vl from "vega-lite-api";
export const viz = vl
  .markPoint({
    fill: true,
    stroke: false,
    size: 900,
    opacity: 0.1,
  })
  .encode(
    vl.x().fieldQ("Time").scale({ zero: false }),
    vl.y().fieldQ("BG").scale({ zero: false }),
    vl.tooltip().fieldN("BG")
  );
