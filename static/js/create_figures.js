create_figures = () => {
  // register vega and vega-lite with the API
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

  vl.register(vega, vegaLite, options);
  const bg_cgm = vl
    .markLine({
      strokeWidth: 1,
      // stroke: "red",
    })
    //   .data(data)
    .encode(
      vl.x().fieldT("time").title(null),
      vl.y().fieldQ(vl.repeat("layer")).scale({ zero: false }),
      vl.color().datum(vl.repeat("layer")),
      vl.tooltip([vl.fieldQ("bg"), vl.hours("time")])
    )
    .width(300)
    .height(100)
    .repeat({ layer: ["bg", "cgm"] })
    .config(config);

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

  fig = vl.vconcat(bg_cgm, cho, insulin, risk_index);

  // .data(data)
  // .autosize({ type: "fit", contains: "padding" })
  fig.render().then((viewElement) => {
    // render returns a promise to a DOM element containing the chart
    // viewElement.value contains the Vega View object instance
    document.getElementById("view").appendChild(viewElement);
  });
  return fig;
};

module.exports = create_figures;
