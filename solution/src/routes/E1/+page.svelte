<!-- App.svelte -->
<script>
  import Nav from "../../components/nav.svelte";// Define the size of the matrix
  let rows = 5;
  let cols = 12;
  let xMargin = 150;
  let yMargin = 150;
  let scale = 0.007;
  let spacing = 75;
  let height = 5*spacing+yMargin*2;
  let width = 12*spacing+xMargin+xMargin;
  let year = "2022";
  let selectedMaterial = "1";
  export let selected_datapoint = undefined;
  function log_console(input) {
                console.log(input);
            }
  function max(number1,number2){
    return number2
    // return Math.max(number1,number2)
  }
  function getMonthInNumber(numberMonth) {
    const map = {
      "1": 1,
      "2": 2,
      "3": 3,
      "4": 4,
      "5": 5,
      "6": 6,
      "7": 7,
      "8": 8,
      "9": 9,
      "10": 10,
      "11": 11,
      "12": 12,
    };
    return map[numberMonth]-1;
  }
  function getMonthInText(numberMonth) {
    const map = {
      "1": "Jan",
      "2": "Feb",
      "3": "Mar",
      "4": "Apr",
      "5": "May",
      "6": "Jun",
      "7": "Jul",
      "8": "Aug",
      "9": "Sep",
      "10": "Oct",
      "11": "Nov",
      "12": "Dec",
    };
    return map[numberMonth];
  }

  const annotationState = {
    Jan: false,
    Feb: false,
    Mar: false,
    Apr: false,
    May: false,
    Jun: false,
    Jul: false,
    Aug: false,
    Sep: false,
    Oct: false,
    Nov: false,
    Dec: false,
  };

  function getPlantInNumber(numberPlant) {
    const map = {
      "4": 1,
      "5": 2,
      "6": 3,
      "7": 4,
      "8": 5
    };
    return map[numberPlant]-1;
  }
  function getPlantName(numberPlant) {
    const map = {
      "4": "ANT2",
      "5": "WRO2",
      "6": "LYO2",
      "7": "BIR2",
      "8": "GOT2"
    };
    return map[numberPlant];
  }
  function sortByMonth(data) {
    let sortedDictByKey = {};
    let sortedByKey = Object.entries(data).sort(([keyA], [keyB]) =>
      keyA.localeCompare(keyB)
    );
    sortedByKey.forEach(([key, value]) => {
      sortedDictByKey[key] = value;
    });
    return sortedDictByKey;
  }

  // Define the function to be executed on change
  function handleChange(event) {
    year = event.target.value;
    console.log("Selected value:", year);
    // Add your logic here
  }
  // Define the function to be executed on change
  function handleChange2(event) {
    selectedMaterial = event.target.value;
    console.log("Selected value:", selectedMaterial);
    // Add your logic here
  }
  let mouse_x, mouse_y;
  const setMousePosition = function(event) {
    mouse_x = event.clientX;
    mouse_y = event.clientY;
  }

  export let data;

</script>
<Nav />
<style>
  .grid {
    display: grid;
    gap: 5px;
  }
  #plot {
    background-color: aliceblue;
  }

  .bubble {
    width: 50px;
    height: 50px;
    background-color: #007bff;
    border-radius: 50%;
  }
  #tooltip {
    position: fixed;
    background-color: white;
    padding: 3px;
    border: solid 1px;
  }
</style>
<svg id="plot" width={width} height={height} >
    {#each Object.entries(sortByMonth(data.result[year])) as [month,plants]}
      {#each Object.entries(plants) as [plant,materials]}
        {#each Object.entries(materials) as [material,obj],i}  
          {#if obj.difference>= 0 && material == selectedMaterial}
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <!-- svelte-ignore a11y-mouse-events-have-key-events -->
            <circle
              r={max(1000,obj.difference)*scale}
              cy = {yMargin+getPlantInNumber(plant)*spacing}
              cx = {xMargin+getMonthInNumber(month)*spacing}
              fill="red"  
              on:mouseover={function(event) {selected_datapoint = obj; setMousePosition(event)}}
              on:mouseout={function() {selected_datapoint = undefined}}
            />
            <!-- Rectangle to display JSON values -->
            
            <!-- <text x={xMargin+getMonthInNumber(month)*spacing} y={yMargin+getPlantInNumber(plant)*spacing} class="small">
              {obj.difference}
            </text> -->
            <!-- on:mouseover={annotateOn}
            on:mouseleave={annotateOff} -->
          {:else if obj.difference <= 0 && material == selectedMaterial}
            <circle
              r={max(1000,-obj.difference)*scale}
              cy = {yMargin+getPlantInNumber(plant)*spacing}
              cx = {xMargin+getMonthInNumber(month)*spacing}
              fill="green"  
              on:mouseover={function(event) {selected_datapoint = obj; setMousePosition(event)}}
              on:mouseout={function() {selected_datapoint = undefined}}
            />
              <!-- <text x={xMargin+getMonthInNumber(month)*spacing} y={yMargin+getPlantInNumber(plant)*spacing} class="small">
                {obj.difference}
              </text> -->
              <!-- on:mouseover={annotateOn}
              on:mouseleave={annotateOff} -->
          {/if}
        {/each}
      {/each}
    {/each}
    {#each Array(5) as _, i}
      <text x=50px y={yMargin+getPlantInNumber(i+4)*spacing} class="small">
        {getPlantName(i+4)}
      </text>
    {/each}  
    {#each Array(12) as _, i}
      <text x={xMargin+getMonthInNumber(i+1)*spacing-15} y={yMargin+5*spacing} class="small">
        {getMonthInText(i+1)}
      </text>
    {/each}          
</svg>
<div>
  <select name="year" id="year" on:change={handleChange}>
    <option value="2022">2022</option>
    <option value="2023">2023</option>
    <option value="2024">2024</option>
    <option value="2025">2025</option>
  </select>
</div>
<div>
  <select name="material" id="material" on:change={handleChange2}>
    <option value="1">EV Car Battery</option>
    <option value="2">Home Battery</option>
  </select>
</div>

{#if selected_datapoint != undefined}
<div id="tooltip" style="left: {mouse_x + 10}px; top: {mouse_y - 10}px">
<ul>
  <li>Forecasted: {selected_datapoint.forecast}</li>
  <li>Actual: {selected_datapoint.sales}</li>
  <li>Difference: {selected_datapoint.difference}</li>
</ul> 
</div>
{/if}


We kunnen zien dat er toch een stevig probleem is met de estimates van verschillende plants (kijk ook naar het feit dat de effectieve sales vrij constant zijn); in 2024 is er consistent veel meer besteld dan verwacht was.