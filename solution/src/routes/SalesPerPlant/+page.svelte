<script>
  import Nav from "../../components/nav.svelte";
  import Title from "../../components/title.svelte";
  export let data;

  console.log(data);

  const dates = Object.keys(data[Object.keys(data)[0]]);
  console.log(dates);

  let plot;

  const plotWidth = 1000;
  const plotHeight = 1000;

  const marginLeft = 100;
  const marginBottom = 150;

  const marginTop = 20;

  const minSale = 174;
  const maxSale = 23261;

  let xLin = 0;
  let selectedXi = null;
  let mouseX = null;
  let mouseY = null;
  const x = Object.values(data[Object.keys(data)[0]]).map((_, i) => i);
  const xDelta = (plotWidth - marginLeft) / x.length;

  const colorMap = {
    "4": "red",
    "5": "blue",
    "6": "orange",
    "7": "purple",
    "8": "green",
  };

  function xCord(i) {
    return marginLeft + (i - 1) * xDelta;
  }

  function yCord(value) {
    const workableHeight = plotHeight - marginBottom - marginTop;
    return marginTop + workableHeight - workableHeight * (value / maxSale);
  }

  function gridYCord(i) {
    const v = 5000;
    return yCord(v * i);
  }

  function range(start, end, interval) {
    const result = [];
    for (let i = start; i <= end; i += interval) {
      result.push(i);
    }
    return Array.from(result);
  }

  const coords = {};
  Object.keys(data).forEach((plantKey) => {
    coords[plantKey] = [];
    Object.values(data[plantKey]).forEach((v, i) => {
      coords[plantKey].push({
        x: i,
        y: yCord(v),
      });
    });
  });
  console.log(coords);

  function log(v) {
    console.log(v);
    return v;
  }

  function translateX(x) {
    return x - plot.getBoundingClientRect().left;
  }
  function translateY(y) {
    return y - plot.getBoundingClientRect().top;
  }

  function moveMouse(e) {
    mouseX = translateX(e.clientX);
    mouseY = translateY(e.clientY);

    const relativeMouseX = e.clientX - plot.getBoundingClientRect().left;
    let minX = xCord(x[0]);
    let minD = Math.abs(xCord(x[0]) - relativeMouseX);
    for (let i = 0; i < x.length; i++) {
      const v = xCord(x[i]);
      const d = Math.abs(v - relativeMouseX);
      if (d < minD) {
        minX = v;
        minD = d;
        selectedXi = i;
      }
    }
    xLin = minX;
  }
</script>

<Nav />
<Title title="Sales per distribution plant through time" />

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<svg
  id="plot"
  width={plotWidth}
  height={plotHeight}
  on:mousemove={moveMouse}
  bind:this={plot}
>
  <!-- y axs -->
  <line
    x1={marginLeft}
    y1={0}
    x2={marginLeft}
    y2={plotHeight - marginBottom + marginTop}
    style="stroke:lightgrey;stroke-width:2"
  />
  <!-- x axs -->
  <line
    x1={marginLeft}
    y1={plotHeight - marginBottom + marginTop}
    x2={plotWidth}
    y2={plotHeight - marginBottom + marginTop}
    style="stroke:lightgrey;stroke-width:2"
  />

  {#each dates as date, i}
    <line
      x1={xCord(i + 1)}
      y1={plotHeight - marginBottom + marginTop}
      x2={xCord(i + 1)}
      y2={plotHeight - marginBottom + marginTop + 10}
      style="stroke:black;stroke-width:1"
    />
    <text
      x={xCord(i) - 10}
      y={plotHeight - marginBottom + 100}
      class="small"
      transform="rotate(315, {xCord(i) - 10}, {plotHeight -
        marginBottom +
        100})"
    >
      {date}
    </text>
  {/each}

  <text
    x={20}
    y={30}
    class="small"
    font-size="15"
  >
    Number
  </text>
  <text
    x={20}
    y={45}
    class="small"
    font-size="15"
  >
    of sales
  </text>
  <text
    x={40}
    y={plotHeight - marginBottom + marginTop}
    class="small"
    font-size="15"
  >
    Date
  </text>

  <!-- grid -->
  {#each range(1, 5, 1) as i}
    <line
      x1={marginLeft}
      y1={gridYCord(i)}
      x2={plotWidth}
      y2={gridYCord(i)}
      style="stroke:lightgrey;stroke-width:1"
    />
    <text x={marginLeft - 60} y={gridYCord(i)} class="small">
      {5000 * i}
    </text>
  {/each}

  {#each Object.keys(data) as plantKey}
    {#each range(1, x.length - 2, 1) as i}
      <circle cx={xCord(i)} cy={coords[plantKey][i]["y"]} r={3} fill="black" />
      <line
        x1={xCord(i)}
        y1={coords[plantKey][i]["y"]}
        x2={xCord(i + 1)}
        y2={coords[plantKey][i + 1]["y"]}
        style="stroke:{colorMap[plantKey]};stroke-width:2"
      />
    {/each}
  {/each}

  <!-- cursor -->
  <line
    x1={xLin}
    y1={0}
    x2={xLin}
    y2={plotHeight}
    style="stroke:lightgrey;stroke-width:2"
  />

  <!-- legend -->
  <rect
    width="80"
    height={120}
    fill="white"
    stroke="lightgrey"
    transform="translate({mouseX + 20}, {mouseY})"
  />

  <text x={mouseX + 30} y={mouseY + 20} class="small" style="fill:black}">
    {dates[selectedXi - 1]}
  </text>
  {#each Object.keys(data) as plantKey, i}
    <text
      x={mouseX + 30}
      y={mouseY + 40 + 15 * i}
      class="small"
      style="fill:{colorMap[plantKey]}"
    >
      {plantKey}:
    </text>
    <text
      x={mouseX + 50}
      y={mouseY + 40 + 15 * i}
      class="small"
      style="fill:{colorMap[plantKey]}"
    >
      {Object.values(data[plantKey])[selectedXi]}
    </text>
  {/each}
</svg>

<style>
  #plot {
    margin: auto;
    display: flex;
    background-color: aliceblue;
  }
</style>
