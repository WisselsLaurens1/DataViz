<script>
  import Nav from "../../components/nav.svelte";

  const centerX = 600;
  const centerY = 300;
  const r = 200;

  const start_alph = 90;

  const l = 250;

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
    return start_alph + 30 * i;
  }

  const monthDeltaDegrees = 90;

  function xPos(i) {
    // - 10 to position in the middle
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

  function annotateOn(month) {
    annotationState[annotationState] = true
  }

  function annotateOff(month) {
    annotationState[annotationState] = false
  }

  export let data;
</script>

<h1>Figure: 1</h1>
<Nav />

<svg id="plot" width="1200" height="600">
  <circle
    cx={centerX}
    cy={centerY}
    {r}
    fill="none"
    stroke="black"
    stroke-width="3"
  />
  <circle
    cx={centerX}
    cy={centerY}
    r="2"
    fill="black"
    stroke="black"
    stroke-width="3"
  />
  {#each Object.entries(sortByMonth(data.result["2022"])) as [month, daysDelta], i}
    {#if daysDelta >= 0}
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <rect
        width="20"
        height={daysDelta * l}
        fill="red"
        transform="translate({xPos(i)}, {yPos(i)}) rotate({30 * i +
          monthDeltaDegrees})"
        on:mouseover={annotateOn}
        on:mouseleave={annotateOff}
      />
    {:else}
      <rect
        width="20"
        height={Math.abs(daysDelta * l)}
        fill="green"
        transform="translate({xPos(i)}, {yPos(i)}) rotate({30 * i +
          180 +
          monthDeltaDegrees})"
      />
    {/if}
    <text x={xPos(i)} y={yPos(i)} class="small">
      {getMonthInText(month)}
    </text>
    <!-- {#if annotationState[month] == true}
      <text x={mouse} y={yPos(i)} class="small">
        {getMonthInText(month)}
      </text>
    {/if} -->
  {/each}
</svg>

<style>
  #plot {
    background-color: aliceblue;
    margin: auto;
    display: flex;
  }
</style>
