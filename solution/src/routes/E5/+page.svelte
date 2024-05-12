<script>
  import Nav from "../../components/nav.svelte";
  import Title from "../../components/title.svelte";

  const plotWidth = 1200;
  const plotHeight = 600;

  const leftMargin = 100;
  const rightMargin = 0;

  const prodPlantsY = 50;
  const distrPlantsY = 250;
  const regionsY = 450;

  const legendY = 10;
  const legendX = 850;

  const prodPlants = ["ANT1", "WRO1", "LYO1"];
  const distrPlants = ["ANT2", "BIR2", "WRO2", "GOT2", "LYO2"];

  const customerRegions = [
    ["Belgium", "Germany", "Netherlands"],
    ["United Kingdom"],
    ["Czech Republic", "Greece", "Hungary", "Poland"],
    [
      "Denmark",
      "Estonia",
      "Finland",
      "Latvia",
      "Lithuania",
      "Norway",
      "Sweden",
    ],
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

  const purchaseVarOptions = [
    "PurchaseOrderCreationDate",
    "PlannedGoodsReceiptDate",
    "ActualGoodsReceiptDate",
    "PlannedArrivalDateYard",
    "ActualArrivalDateYard",
    "PlannedVendorShipmentDate",
    "ActualVendorShipmentDate",
  ];

  let purchaseVar1 = "PurchaseOrderCreationDate";
  let purchaseVar2 = "ActualGoodsReceiptDate";

  const saleVarOptions = [
    "SalesOrderCreationDate",
    "RequestedDeliveryDate",
    "DeliveryDate",
  ];

  let salesVar1 = "SalesOrderCreationDate";
  let salesVar2 = "DeliveryDate";

  const salesAvgs = {};
  const purchaseAvgs = {};

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
    "Denmark, Estonia, Finland, Latvia, Lithuania, Norway, Sweden": {},
  };

  const workSpaceWidth = plotWidth - rightMargin;
  let delta = workSpaceWidth / distrPlants.length;
  distrPlants.forEach((plant, i) => {
    const x = leftMargin + i * delta;
    const y = distrPlantsY;
    cordMap[plant].x = x;
    cordMap[plant].y = y;

    const region = customerRegions[i].join(", ");
    cordMap[region].x = x;
    cordMap[region].y = regionsY;
  });

  cordMap["ANT1"].x = (cordMap["ANT2"].x + cordMap["BIR2"].x) / 2;
  cordMap["ANT1"].y = prodPlantsY;
  cordMap["WRO1"].x = (cordMap["WRO2"].x + cordMap["GOT2"].x) / 2;
  cordMap["WRO1"].y = prodPlantsY;
  cordMap["LYO1"].x = cordMap["LYO2"].x;
  cordMap["LYO1"].y = prodPlantsY;

  function log(e) {
    console.log(e);
    return e;
  }

  function avgBetween2Vars(data, var1, var2) {
    let total = 0;

    data.forEach((dp) => {
      const a = dp[var1];
      const b = dp[var2];
      total += b - a;
    });
    const avg = total / data.length;
    return avg;
  }

  export let data
  console.log(data);

  const salesDataInDays = data.sales_data_in_days;
  const purchaseDataInDays = data.purchases_data_in_days;

  function calcPurchaseAvg(data) {
    const newAvgs = {};
    let maxAvg = 0;
    let minAvg = 999999999999;
    Object.keys(data).forEach((route) => {
      const avg = avgBetween2Vars(data[route], purchaseVar1, purchaseVar2);
      if (avg > maxAvg) {
        maxAvg = avg;
      }
      if (avg < minAvg) {
        minAvg = avg;
      }
      newAvgs[route] = {
        avg: avg,
        VendorKey: data[route][0]["VendorKey"],
        PlantKey: data[route][0]["PlantKey"],
      };
    });

    Object.keys(newAvgs).forEach((route) => {
      newAvgs[route]["width"] = newAvgs[route]["avg"]
    });
    console.log(newAvgs);
    return newAvgs;
  }

  let purchaseDataInDaysAvgs = calcPurchaseAvg(purchaseDataInDays);
</script>

<Nav />
<Title title="Difference between dates of supply chain"/>

<svg id="plot" width={plotWidth} height={plotHeight}>
  <defs>
    <marker
      id="green-head"
      orient="auto"
      markerWidth="2"
      markerHeight="4"
      refX="1"
      refY="2"
    >
      <path d="M0,0 V4 L2,2 Z" fill="#3d8752" />
    </marker>
    <marker
      id="blue-head"
      orient="auto"
      markerWidth="2"
      markerHeight="4"
      refX="1"
      refY="2"
    >
      <path d="M0,0 V4 L2,2 Z" fill="#70b8ff" />
    </marker>
  </defs>

  {#each prodPlants as plant, i}
    <text x={cordMap[plant].x} y={cordMap[plant].y} class="small">
      {plant}
    </text>
  {/each}

  {#each distrPlants as plant, i}
    <text x={cordMap[plant].x} y={cordMap[plant].y} class="small">
      {plant}
    </text>
    {#each customerRegions[i] as country, j}
      <text
        x={cordMap[plant].x}
        y={cordMap[customerRegions[i].join(", ")].y + 20 * j}
        class="small"
      >
        {country}
      </text>
    {/each}
  {/each}

  {#each Object.keys(purchaseDataInDaysAvgs) as route, i}
    <line
      x1={cordMap[purchaseDataInDaysAvgs[route]["VendorKey"]].x + 15}
      y1={cordMap[purchaseDataInDaysAvgs[route]["VendorKey"]].y + 20}
      x2={cordMap[purchaseDataInDaysAvgs[route]["PlantKey"]].x + 15}
      y2={cordMap[purchaseDataInDaysAvgs[route]["PlantKey"]].y - 40}
      stroke-linecap="round"
      style="stroke:#70b8ff; stroke-width:{1 +
        purchaseDataInDaysAvgs[route]['width']}"
      marker-end="url(#blue-head)"
    />
    {#if cordMap[purchaseDataInDaysAvgs[route]["VendorKey"]].x != cordMap[purchaseDataInDaysAvgs[route]["PlantKey"]].x}
      <text
        x={cordMap[purchaseDataInDaysAvgs[route]["PlantKey"]].x}
        y={cordMap[purchaseDataInDaysAvgs[route]["VendorKey"]].y + 100}
        class="small"
      >
        {Math.round(purchaseDataInDaysAvgs[route]["avg"] * 100) / 100}
      </text>
    {:else}
      <text
        x={cordMap[purchaseDataInDaysAvgs[route]["PlantKey"]].x + 30}
        y={cordMap[purchaseDataInDaysAvgs[route]["VendorKey"]].y + 100}
        class="small"
      >
        {Math.round(purchaseDataInDaysAvgs[route]["avg"] * 100) / 100}
      </text>
    {/if}
  {/each}

  {#each Object.keys(salesDataInDays) as startPlant, i}
    <line
      x1={cordMap[startPlant].x + 20}
      y1={cordMap[startPlant].y + 40}
      x2={cordMap[
        salesDataInDays[startPlant]["metadata"]["CustomerRegion"].join(", ")
      ].x + 20}
      y2={cordMap[
        salesDataInDays[startPlant]["metadata"]["CustomerRegion"].join(", ")
      ].y - 40}
      stroke-linecap="round"
      style="stroke:#3d8752;stroke-width:{1 +
        Math.abs(
          avgBetween2Vars(
            salesDataInDays[startPlant]['data'],
            salesVar1,
            salesVar2
          ) * 0.6
        )}"
      marker-end="url(#green-head)"
    />
    <text
      x={cordMap[startPlant].x + 50}
      y={cordMap[startPlant].y + 100}
      class="small"
    >
      {Math.round(
        avgBetween2Vars(
          salesDataInDays[startPlant]["data"],
          salesVar1,
          salesVar2
        ) * 100
      ) / 100}
    </text>
  {/each}
</svg>

<!-- var selection -->
<div id="controls">
  <div id="purchaseDataVarOptions">
    <div class="containers">
      <select
        bind:value={purchaseVar2}
        on:change={() => {
          purchaseDataInDaysAvgs = calcPurchaseAvg(purchaseDataInDays);
        }}
      >
        {#each purchaseVarOptions as option, i}
          <option value={option}>{option}</option>
        {/each}
      </select>
    </div>
    <p style="margin-left: 15px; margin-right: 15px; text-align:center;">-</p>
    <div class="containers">
      <select
        bind:value={purchaseVar1}
        on:change={() => {
          purchaseDataInDaysAvgs = calcPurchaseAvg(purchaseDataInDays);
        }}
      >
        {#each purchaseVarOptions as option, i}
          <option value={option}>{option}</option>
        {/each}
      </select>
    </div>
  </div>

  <div id="saleDataVarOptions">
    <div>
      <select bind:value={salesVar2}>
        {#each saleVarOptions as option, i}
          <option value={option}>{option}</option>
        {/each}
      </select>
    </div>
    <p style="margin-left: 15px; margin-right: 15px;">-</p>
    <div>
      <select bind:value={salesVar1}>
        {#each saleVarOptions as option, i}
          <option value={option}>{option}</option>
        {/each}
      </select>
    </div>
  </div>
</div>

<style>
  #plot {
    background-color: aliceblue;
    margin: auto;
    display: flex;
  }

  #controls {
    display: flex;
    flex-direction: column;
    margin: auto;
    width: fit-content;
    align-items: center;
  }

  #saleDataVarOptions {
    display: flex;
    align-items: center;
    background-color: #eaeaea;
    width: fit-content;
    padding: 10px;
  }

  #purchaseDataVarOptions {
    display: flex;
    align-items: center;
    background-color: #eaeaea;
    width: fit-content;
    padding: 10px;
    margin-bottom: 10px;
    margin-top: 10px;
  }
</style>
