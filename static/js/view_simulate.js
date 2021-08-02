// setup API options
const options = {
  config: {
    // Vega-Lite default configuration
  },
  init: (view) => {
    // initialize tooltip handler
    view.tooltip(new vegaTooltip.Handler().call);
  },
  view: {
    // view constructor options
    // remove the loader if you don't want to default to vega-datasets!
    loader: vega.loader({
      baseURL:
        "https://unpkg.com/vega-datasets@2.2.0/build/vega-datasets.min.js",
    }),
    renderer: "svg",
  },
};
// const getData = async () => {
//     const url = "http://127.0.0.1:5000/results";
//     const res = await fetch(url);
//     return res.text();
//     // .then(result => result)
// }

const url = "http://127.0.0.1:5004/results/try1";
let config = {
  view: {
    stroke: null,
  },
  axis: {
    domain: false,
    tickColor: "lightGray",
  },
  style: {
    "guide-label": {
      fontSize: 20,
      fill: "#3e3c38",
    },
    "guide-title": {
      fontSize: 30,
      fill: "#3e3c38",
    },
  },
};
const res = async () => {
  const result = await fetch(url);
  return await result.json();
};
const upper_figures = async () => {
  const result = await res();
  // register vega and vega-lite with the API
  vl.register(vega, vegaLite, options);
  // now you can use the API!
  // const base = vl.markLine().encode(
  //     vl.x().fieldT("time").title(null),
  // )
  const data = result.filter((d) => d.patient_id === "adolescent#001");
  const bg_cgm = vl
    .markLine({
      strokeWidth: 1,
      // stroke: "red",
    })
    // .data(data)
    .encode(
      vl.x().fieldT("time").title(null),
      vl.y().fieldQ(vl.repeat("layer")).scale({ zero: false }),
      vl.color().datum(vl.repeat("layer")),
      vl.tooltip([vl.fieldQ("bg"), vl.hours("time")])
    )
    .width(300)
    .height(100)
    .repeat({ layer: ["bg", "cgm"] });
  //
  //   .config(config)

  // const bg = vl
  //   .markLine({
  //     strokeWidth: 1,
  //     stroke: "red",
  //   })
  //   .data(result.filter((d) => d.patient_id === "adolescent#001"))
  //   .width(300)
  //   .height(100)
  //   // .autosize({ type: "fit", contains: "padding" })
  //   //   .config(config)
  //   .encode(
  //     vl.x().fieldT("time").title(null),
  //     vl.y().fieldQ("bg").scale({ zero: false }),
  //     // vl.color().fieldQ("cgm"),
  //     vl.tooltip([vl.fieldQ("bg"), vl.hours("time")])
  //   );
  const cho = vl
    .markLine({ strokeWidth: 1 })
    //   .data(data)
    .encode(
      vl.x().fieldT("time").title(null),
      vl.y().fieldQ("cho").scale({ zero: false }),
      vl.tooltip([vl.fieldQ("cho"), vl.hours("time")])
    )
    .width(300)
    .height(100);

  const insulin = cho.encode(
    vl.y().fieldQ("insulin").scale({ zero: false }),
    vl.tooltip([vl.fieldQ("insulin"), vl.hours("time")])
  );
  const risk_index = vl
    .markLine({
      strokeWidth: 1,
      // stroke: "red",
    })
    .encode(
      vl.x().fieldT("time").title(null),
      vl.y().fieldQ(vl.repeat("layer")).scale({ zero: false }),
      vl.color().datum(vl.repeat("layer")),
      vl.tooltip([
        vl.fieldQ("lbgi"),
        vl.fieldQ("hbgi"),
        vl.fieldQ("risk"),
        vl.hours("time"),
      ])
    )
    .width(300)
    .height(100)
    .repeat({ layer: ["lbgi", "hbgi", "risk"] });
  //   const hbgi = risk_index.encode(vl.y().fieldQ("hbgi").scale({ zero: false }));

  vl.vconcat(bg_cgm, cho, insulin, risk_index)
    // .data(data)
    // .autosize({ type: "fit", contains: "padding" })
    .render()
    .then((viewElement) => {
      // render returns a promise to a DOM element containing the chart
      // viewElement.value contains the Vega View object instance
      document.getElementById("view").appendChild(viewElement);
    });
};
// const lower_figures = async () => {
//   const result = await res();
//   vl.register(vega, vegaLite, options);
//   const data = result.filter((d) => d.patient_id === "adolescent#001");
//   const risk_index = vl
//     .markLine({
//       strokeWidth: 1,
//       // stroke: "red",
//     })
//     .encode(
//       vl.x().fieldT("time").title(null),
//       vl.y().fieldQ(vl.repeat("layer")).scale({ zero: false }),
//       vl.color().datum(vl.repeat("layer")),
//       vl.tooltip([vl.fieldQ("lbgi"), vl.fieldQ("hbgi"), vl.hours("time")])
//     )
//     .width(300)
//     .height(100)
//     .repeat({ layer: ["lbgi", "hbgi", "risk"] })
//     .data(data)
//     // .autosize({ contains: "padding" })
//     .render()
//     .then((viewElement) => {
//       // render returns a promise to a DOM element containing the chart
//       // viewElement.value contains the Vega View object instance
//       document.getElementById("view").appendChild(viewElement);
//     });
// };
upper_figures();
// lower_figures();
