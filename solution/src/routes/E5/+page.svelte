<script>
  import Nav from "../../components/nav.svelte";

  const plotWidth = 1200;
  const leftMargin = 100;
  const rightMargin = 50;
  const spacing = 10;

  const yStart = 100;
  const ySpacing = 150;

  const prodPlants = ["ANT1", "WRO1", "LYO1"];
  const distrPlants = ["ANT2", "BIR2", "WRO2", "GOT2", "LYO2"];

  const customerRegions = [
    ["Belgium", "Germany", "Netherlands"],
    ["United Kingdom"],
    ["Czech Republic", "Greece", "Hungary", "Poland"],
    ["Denmark", "Estonia", "Finland", "Latvia", "Lithuania", "Norway", "Sweden"],
    [
      "Croatia",
      "France",
      "Italy",
      "Portugal",
      "Slovenia",
      "Spain",
      "Switzerland",
    ],
  ];

  const cordMap = {
    ANT1: { x: null, y: null },
    WRO1: { x: null, y: null },
    LYO1: { x: null, y: null },
    ANT2: { x: null, y: null },
    BIR2: { x: null, y: null },
    WRO2: { x: null, y: null },
    GOT2: { x: null, y: null },
    LYO2: { x: null, y: null },
    "Belgium, Germany, Netherlands": { x: null, y: null },
    "Croatia, France, Italy, Portugal, Slovenia, Spain, Switzerland": {
      x: null,
      y: null,
    },
    "United Kingdom": { x: null, y: null },
    "Czech Republic, Greece, Hungary, Poland": { x: null, y: null },
    "Denmark, Estonia, Finland, Latvia, Lithuania, Norway, Sweden": {}
  };

  function registerCord(cordName, cord, name, returnValue) {
    /*
    cordName: x or y
    cord: value to set
    name: the variable in the cord map for which we want to register a cord
    returnValue: the value to return to svg element, is not always the same as registered cord
    */
    if (cordName == "x") {
      cordMap[name].x = cord;
    }
    if (cordName == "y") {
      cordMap[name].y = cord;
    }
    return returnValue;
  }

  function getSpacedOutX(i, elements) {
    const total = plotWidth - (leftMargin + rightMargin);
    const l = total / elements.length;
    return leftMargin + l * i;
  }

  function log(e){
    console.log("log", e)
    return e
  }

  export let data;

  console.log(data);
</script>

<h1>Figure: E5</h1>
<Nav />

<svg id="plot" width={plotWidth} height="600">
  {#each prodPlants as plant, i}
    <text
      x={registerCord(
        "x",
        getSpacedOutX(i, prodPlants),
        plant,
        getSpacedOutX(i, prodPlants)
      )}
      y={registerCord("y", yStart, plant, yStart)}
      class="small"
    >
      {plant}
    </text>
  {/each}
  {#each distrPlants as plant, i}
    <text
      x={registerCord(
        "x",
        getSpacedOutX(i, distrPlants),
        plant,
        getSpacedOutX(i, distrPlants)
      )}
      y={registerCord("y", yStart + ySpacing, plant, yStart + ySpacing)}
      class="small"
    >
      {plant}
    </text>
  {/each}
  {#each customerRegions as region, i}
    {#each region as country, j}
      <text
        x={registerCord(
          "x",
          getSpacedOutX(i, customerRegions),
          region.join(", "),
          getSpacedOutX(i, customerRegions)
        )}
        y={registerCord(
          "y",
          yStart + 2 * ySpacing,
          region.join(", "),
          yStart + 2 * ySpacing + 20 * j
        )}
        class="small"
      >
        {country}
      </text>
    {/each}
  {/each}
  {#each Object.values(data.purchases_per_production_plant) as route, i}
    <line
      x1={cordMap[route["production_plant"]].x}
      y1={cordMap[route["production_plant"]].y}
      x2={cordMap[route["distribution_center"]].x}
      y2={cordMap[route["distribution_center"]].y}
      style="stroke:2;stroke-width:{Math.abs(route['avg_goods_receipt_date_delta'] * 10)}"
    />
  {/each}
  {#each Object.values(data.purchases_per_distribution_center) as route, i}
    <line
      x1={cordMap[route["distribution_center"]].x}
      y1={cordMap[route["distribution_center"]].y}
      x2={cordMap[(route["customer_region"].join(", "))].x}
      y2={cordMap[route["customer_region"].join(", ")].y}
      style="stroke:red;stroke-width:2"
    />
  {/each}
</svg>

<style>
  #plot {
    background-color: aliceblue;
    margin: auto;
    display: flex;
  }
</style>
