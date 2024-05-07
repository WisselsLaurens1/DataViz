<!-- App.svelte -->
<script>
// @ts-nocheck

  import Nav from "../../components/nav.svelte";// Define the size of the matrix
  let width = 1200
  let height = 600
  let material = 1;
  let box_width = 30;
  let spacing = 50;
  let bottomMargin = 100;
  let leftMargin = 100;

  const scaleX = function(x) {
    console.log(((width-leftMargin)*(x-1))/(4))
      return ((width-leftMargin)*(x-1))/(4)
  }
  const scaleY = function(y) {
      return ((0-height+bottomMargin)*(y))/(4000)
  }
  function getPlantInNumber(numberPlant) {
    console.log(1)
    const map = {
      "10004": 1,
      "10005": 2,
      "10006": 3,
      "10007": 4,
      "10008": 5,
      "20004": 1,
      "20005": 2,
      "20006": 3,
      "20007": 4,
      "20008": 5
    };
    return map[numberPlant];
  }
  function getMaterialInNumber(numberMaterial){
    const map = {
      "10004": 1,
      "10005": 1,
      "10006": 1,
      "10007": 1,
      "10008": 1,
      "20004": 2,
      "20005": 2,
      "20006": 2,
      "20007": 2,
      "20008": 2
    };
    console.log(map[numberMaterial])
    return map[numberMaterial];
  }
  
  function getPlantName(numberPlant) {

    console.log(3)
    const map = {
      "10004": "ANT2",
      "10005": "WRO2",
      "10006": "LYO2",
      "10007": "BIR2",
      "10008": "GOT2",
      "20004": "ANT2",
      "20005": "WRO2",
      "20006": "LYO2",
      "20007": "BIR2",
      "20008": "GOT2"
    };
    return map[numberPlant];
  }
  export let data;

</script>
<Nav />
<style>
  #plot {
    background-color: aliceblue;
    border-color: black;
    border-width: 2px;
  }
</style>
<svg id="plot" width={width} height={height}>
  {#each Object.entries(data.result) as [mpk,values]}
  
    {#if getMaterialInNumber(mpk) == material}
      
      <rect
        width={box_width}
        height={values[4]-values[2]}
        fill="red"
        transform="translate({scaleX(getPlantInNumber(mpk))+leftMargin}, {scaleY(values[2])})"
      />
    {/if}  
  {/each}      
</svg>
<!-- <div>
  <select name="year" id="year" on:change={handleChange}>
    <option value="2022">2022</option>
    <option value="2023">2023</option>
    <option value="2024">2024</option>
    <option value="2025">2025</option>
  </select>
</div> -->

<!-- {#if selected_datapoint != undefined}
<div id="tooltip" style="left: {mouse_x + 10}px; top: {mouse_y - 10}px">
<ul>
  <li>Forecasted: {selected_datapoint.forecast}</li>
  <li>Actual: {selected_datapoint.sales}</li>
  <li>Difference: {selected_datapoint.difference}</li>
</ul> 
</div>
{/if} -->