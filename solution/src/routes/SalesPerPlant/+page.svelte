<script>
  import Nav from "../../components/nav.svelte";
  export let data;

  console.log(data);

  let plot;

  const plotWidth = 1000;
  const plotHeight = 800;

  const xStart = 10;

  const minSale = 174;
  const maxSale = 23261;

  let xLin = 0;
  let selectedXi = null;
  let mouseX = null;
  let mouseY = null;
  const x = Object.values(data[Object.keys(data)[0]]).map((_, i) => i);
  const xDelta = (plotWidth - xStart) / x.length;

  const colorMap = {
    "4": "red",
    "5": "blue",
    "6": "orange",
    "7": "purple",
    "8": "green",
  };

  function xCord(i) {
    return xStart + i * xDelta;
  }

  function normalizeSaleValue(value) {
    return (plotHeight * value) / maxSale;
  }

  function range(start, end) {
    return Array.from(Array(end + 1).keys()).slice(start);
  }

  const coords = {};
  Object.keys(data).forEach((plantKey) => {
    coords[plantKey] = [];
    Object.values(data[plantKey]).forEach((v, i) => {
      coords[plantKey].push({
        x: i,
        y: normalizeSaleValue(v),
      });
    });
  });

  function log(v) {
    console.log(v);
    return v;
  }

  function moveMouse(e) {
    mouseX = e.clientX - plot.getBoundingClientRect().left;
    mouseY = e.clientY - plot.getBoundingClientRect().top;

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

<h1>Figure: Sales per plant</h1>
<Nav />
<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<svg
  id="plot"
  width={plotWidth}
  height={plotHeight}
  on:mousemove={moveMouse}
  bind:this={plot}
>
  {#each Object.keys(data) as plantKey}
    {#each range(1, x.length - 2) as i}
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
  <line
    x1={xLin}
    y1={0}
    x2={xLin}
    y2={plotHeight}
    style="stroke:lightgrey;stroke-width:2"
  />
  <rect
    width="80"
    height={100}
    fill="white"
    transform="translate({mouseX + 20}, {mouseY})"
  />
  {#each Object.keys(data) as plantKey, i}
    <text x={mouseX + 30} y={mouseY + 20 + 15 * i} class="small" style="fill:{colorMap[plantKey]}">
      {plantKey}:
    </text>
    <text x={mouseX + 50} y={mouseY + 20 + 15 * i} class="small" style="fill:{colorMap[plantKey]}">
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
