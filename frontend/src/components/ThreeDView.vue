<template>
  <div ref="container" class="three-container"></div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default {
  name: "ThreeDView",
  mounted() {
    this.init3D();
    window.addEventListener("resize", this.onResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
    cancelAnimationFrame(this.animationId);
  },
  methods: {
    init3D() {
      const container = this.$refs.container;

      // scene
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xfafafa);

      // camera
      const width = container.clientWidth;
      const height = container.clientHeight;
      this.camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
      this.camera.position.set(0, 10, 20);

      // renderer
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(width, height);
      container.appendChild(this.renderer.domElement);

      // controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;

      // lights
      const light1 = new THREE.DirectionalLight(0xffffff, 0.8);
      light1.position.set(5, 10, 7);
      this.scene.add(light1);

      const ambient = new THREE.AmbientLight(0xffffff, 0.4);
      this.scene.add(ambient);

      this.drawSample();

      this.animate();
    },

    drawSample() {
      // ground
      const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(200, 200),
        new THREE.MeshStandardMaterial({ color: "#e0e0e0" })
      );
      plane.rotation.x = -Math.PI / 2;
      this.scene.add(plane);

      // sample box
      const box = new THREE.Mesh(
        new THREE.BoxGeometry(4, 4, 4),
        new THREE.MeshStandardMaterial({ color: "#3994ff" })
      );
      box.position.y = 2;
      this.scene.add(box);
    },

    animate() {
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
      this.animationId = requestAnimationFrame(this.animate);
    },

    onResize() {
      const container = this.$refs.container;
      this.camera.aspect = container.clientWidth / container.clientHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(container.clientWidth, container.clientHeight);
    }
  }
};
</script>

<style scoped>
.three-container {
  width: 100%;
  height: 550px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
