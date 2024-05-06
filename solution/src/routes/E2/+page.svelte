<script>
  import Nav from "../../components/nav.svelte";
  export let data;
</script>

<h1>Figure: E2</h1>
<Nav />
<!-- {#each data.result as datapoint}
  {datapoint.}
{/each}    -->
<svg id="plot" width="1000" height="800"> </svg>

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
