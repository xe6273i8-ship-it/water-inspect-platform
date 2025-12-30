<template>
  <div class="three-page">
    <h2>设施 3D 可视化展示</h2>
    <ThreeDView />
  </div>
</template>

<script>
import ThreeDView from "@/components/ThreeDView.vue";

export default {
  name: "ThreeDPage",
  components: { ThreeDView }
};
</script>

<style scoped>
.three-page {
  padding: 20px;
}
</style>
