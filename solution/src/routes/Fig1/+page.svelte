<script>
  import Nav from "../../components/nav.svelte";
  import Title from "../../components/title.svelte";

  const centerX = 600;
  const centerY = 300;
  const r = 200;

  const start_alph = 90;
  const l = 70;
  const notSelectedColor = "lightgrey";
  const positiveColor = "green"
  const negativeColor = "red"

  const monthDeltaDegrees = 90;

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

  let svg;
  let selectedYear = "2022";
  const axes = Array.from({ length: 10 }, (_, i) => i);

  function cosValue(angleInDegrees) {
    let angleInRadians = (angleInDegrees * Math.PI) / 180;
    return Math.cos(angleInRadians);
  }

  function sinValue(angleInDegrees) {
    let angleInRadians = (angleInDegrees * Math.PI) / 180;
    return Math.sin(angleInRadians);
  }

  function angle(i) {
    return start_alph + 30 * i;
  }

  function xPos(i) {
    return centerX + r * cosValue(angle(i) + monthDeltaDegrees);
  }

  function yPos(i) {
    return centerY + r * sinValue(angle(i) + monthDeltaDegrees);
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

  function getMonthInText(numberMonth) {
    const map = {
      "01": "Jan",
      "02": "Feb",
      "03": "Mar",
      "04": "Apr",
      "05": "May",
      "06": "Jun",
      "07": "Jul",
      "08": "Aug",
      "09": "Sep",
      "10": "Oct",
      "11": "Nov",
      "12": "Dec",
    };
    return map[numberMonth];
  }

  function annotateOn(month) {
    annotationState[month] = true;
    colorMap[selectedYear][month] 
    Object.keys(colorMap[selectedYear]).forEach(month_ => {
      if(month != month_){
        colorMap[selectedYear][month_].selected = notSelectedColor
      }
    }) 
  }
  
  function annotateOff(month) {
    annotationState[month] = false;
    colorMap[selectedYear][month] 
    Object.keys(colorMap[selectedYear]).forEach(month_ => {
      if(month != month_){
        colorMap[selectedYear][month_].selected = colorMap[selectedYear][month_].color
      }
    }) 
  }

  function setSelectedYear(newYear) {
    selectedYear = newYear;
  }




  function getColor(targetColor, month) {
    if (Object.values(annotationState).every((e) => e == false)) {
      return targetColor;
    }
    let activeMonth = null;
    console.log(annotationState)
    annotationState.forEach(([key, value]) => {
      console.log(key, value)
      if(key == month && value == true){
        return targetColor
      }
    });
    // return notSelectedColor

  }

  export let data;
  const colorMap = {}
  Object.entries(data.result).forEach(([year, months]) => {
    const monthsData = {}
    Object.entries(months).forEach(([month, v]) => {
      if(v >= 0){
        monthsData[month] = {
          "selected": negativeColor,
          "color": negativeColor
        }
      }else{
        monthsData[month] = {
          "selected": positiveColor,
          "color": positiveColor
        }
      }
    })
    colorMap[year] = monthsData
  });

</script>

<h1>Figure: 1</h1>
<Nav />

<svg id="plot" width="1200" height="600" bind:this={svg}>
  <circle
    cx={centerX}
    cy={centerY}
    {r}
    fill="none"
    stroke="black"
    stroke-width="3"
  />
  {#each axes as _, i}
    <circle
      cx={centerX}
      cy={centerY}
      r={r - 50 + 10 * i}
      fill="none"
      stroke="lightgrey"
      stroke-width="1"
    />
  {/each}
  {#each Object.entries(sortByMonth(data.result[selectedYear])) as [month, daysDelta], i}
    {#if daysDelta >= 0}
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <rect
        width="20"
        height={daysDelta * l}
        fill={colorMap[selectedYear][month].selected}
        transform="translate({xPos(i)}, {yPos(i)}) rotate({30 * i +
          monthDeltaDegrees})"
        on:mouseover={(e) => annotateOn(month)}
        on:mouseleave={(e) => annotateOff(month)}
      />
    {:else}
      <rect
        width="20"
        height={Math.abs(daysDelta * l)}
        fill={colorMap[selectedYear][month].selected}
        transform="translate({xPos(i)}, {yPos(i)}) rotate({30 * i +
          180 +
          monthDeltaDegrees})"
      />
    {/if}
    <text x={xPos(i)} y={yPos(i)} class="small">
      {getMonthInText(month)}
    </text>
    <text x={centerX - 75} y={centerY} class="small">
      Average difference in days:
    </text>
    {#if annotationState[month] == true}
      <text x={centerX - 75} y={centerY + 30} class="small">
        {daysDelta}
      </text>
    {/if}
  {/each}
</svg>
<div>
  {#each Object.keys(sortByMonth(data.result)) as year}
    <button on:click={() => setSelectedYear(year)}>{year}</button>
  {/each}
</div>

<style>
  #plot {
    background-color: aliceblue;
    margin: auto;
    display: flex;
  }
  /* svg rect:hover {
    filter: drop-shadow(0px -3px 4px rgba(34, 34, 34, 0.4));
    fill: rgb(149, 149, 149);
  } */
</style>
