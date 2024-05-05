<script>
  import MyComponent from '$lib/MyComponent.svelte';

  let slider_value = 5;
  const rescale = function (x, domain_min, domain_max, range_min, range_max) {
    return (
      ((range_max - range_min) * (x - domain_min)) / (domain_max - domain_min) +
      range_min
    );
  };
  export let data;
</script>

<body>
  <MyComponent></MyComponent>
  <svg id="plot" width="1000" height="800">
    {#each data.data as datapoint}
      {#if datapoint.Species == "Iris-versicolor"}
        <circle
          fill="red"
          cx={datapoint.SepalLengthCm * 100}
          cy={datapoint.SepalWidthCm * 100}
          r="{slider_value}"
        />
      {:else}
        <circle
          fill="blue"
          cx={datapoint.SepalLengthCm * 100}
          cy={datapoint.SepalWidthCm * 100}
          r="{slider_value}"
        />
      {/if}
    {/each}
  </svg>
  <input type="range" min="0" max="100" bind:value={slider_value} />
</body>

<style>
  #plot {
    background-color: aliceblue;
  }
  .red {
    color: red;
  }
  .blue {
    color: blue;
  }
</style>
