(function (vega, vegaLite, vl, vegaTooltip, d3) {
  'use strict';

  function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

  var vega__default = /*#__PURE__*/_interopDefaultLegacy(vega);
  var vegaLite__default = /*#__PURE__*/_interopDefaultLegacy(vegaLite);
  var vl__default = /*#__PURE__*/_interopDefaultLegacy(vl);

  // Appearance customization to improve readability.
  // See https://vega.github.io/vega-lite/docs/
  const dark = "#3e3c38";
  const config = {
    axis: {
      domain: false,
      tickColor: "lightGray",
    },
    style: {
      "guide-label": {
        fontSize: 20,
        fill: dark,
      },
      "guide-title": {
        fontSize: 30,
        fill: dark,
      },
    },
  };

  const csvUrl =
    "https://gist.githubusercontent.com/xiaoxiaomeng0/83a31edc87e3864dbba8a7ccd263af71/raw/simglucose_test.csv";

  const getData = async () => {
    const data = await d3.csv(csvUrl);

    // Have a look at the attributes available in the console!
    console.log(data[0]);

    return data;
  };

  const viz = vl__default['default']
    .markPoint({
      fill: true,
      stroke: false,
      size: 900,
      opacity: 0.1,
    })
    .encode(
      vl__default['default'].x().fieldQ("Time").scale({ zero: false }),
      vl__default['default'].y().fieldQ("BG").scale({ zero: false }),
      vl__default['default'].tooltip().fieldN("BG")
    );

  vl__default['default'].register(vega__default['default'], vegaLite__default['default'], {
    view: { renderer: "svg" },
    init: (view) => {
      view.tooltip(new vegaTooltip.Handler().call);
    },
  });

  const run = async () => {
    const marks = viz
      .data(await getData())
      .width(window.innerWidth)
      .height(window.innerHeight)
      .autosize({ type: "fit", contains: "padding" })
      .config(config);

    document.body.appendChild(await marks.render());
  };
  run();

}(vega, vegaLite, vl, vegaTooltip, d3));
