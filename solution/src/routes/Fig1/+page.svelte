<script>
  import Nav from "../../components/nav.svelte";
  
  const centerX = 600
  const centerY = 300
  const r = 200

  let start_x = 580;
  let start_y = 90;
  let start_alph = 90;

  let items = Array.from({ length: 12 }, (_, i) => i + 1);

  function cosValue(angleInDegrees) {
    let angleInRadians = (angleInDegrees * Math.PI) / 180;
    // Calculate cosine and sine
    return Math.cos(angleInRadians);
  }

  function sinValue(angleInDegrees) {
    let angleInRadians = (angleInDegrees * Math.PI) / 180;
    return Math.sin(angleInRadians);
  }

  function angle(i) {
    return start_alph + (30 * i);
  }

  function xPos(i) {
    // - 10 to position in the middle
    return centerX + (r * cosValue(angle(i))) - 10;
  }

  function yPos(i) {
    return centerY + (r * sinValue(angle(i)));
  }

  export let data;
</script>

<h1>Figure: 1</h1>
<Nav />

<svg id="plot" width="1200" height="600">
  <circle
    cx="{centerX}"
    cy="{centerY}"
    r="{r}"
    fill="none"
    stroke="green"
    stroke-width="3"
  />
  <circle
    cx="{centerX}"
    cy="{centerY}"
    r="2"
    fill="black"
    stroke="black"
    stroke-width="3"
  />
  {#each items as _, i}
    <rect
      width="20"
      height="100"
      fill="blue"
      transform="translate({xPos(i)}, {yPos(i)}) rotate({(30 * i) })"
    />
  {/each}
</svg>

<style>
  #plot {
    background-color: aliceblue;
    margin: auto;
    display: flex;
  }
  .red {
    color: red;
  }
  .blue {
    color: blue;
  }
</style>
