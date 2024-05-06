<!-- App.svelte -->
<script>
  import Nav from "../../components/nav.svelte";// Define the size of the matrix
  let rows = 5;
  let cols = 12;
</script>

<style>
  .grid {
    display: grid;
    gap: 5px;
  }

  .bubble {
    width: 50px;
    height: 50px;
    background-color: #007bff;
    border-radius: 50%;
  }
</style>

<div class="grid" style="grid-template-columns: repeat({cols}, 50px)">
  {#each Array(rows * cols) as _, i}
    <div class="bubble"></div>
  {/each}
</div>