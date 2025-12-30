<template>
  <div ref="container" class="three-container"></div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

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

      // === 场景
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0x87ceeb); // 天空蓝

      // === 相机
      const width = container.clientWidth;
      const height = container.clientHeight;
      this.camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
      this.camera.position.set(0, 15, 30);

      // === 渲染器
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(width, height);
      container.appendChild(this.renderer.domElement);

      // === 控制器
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;

      // === 光照
      const dirLight = new THREE.DirectionalLight(0xffffff, 1);
      dirLight.position.set(10, 20, 10);
      this.scene.add(dirLight);

      const ambient = new THREE.AmbientLight(0xffffff, 0.4);
      this.scene.add(ambient);

      // === 添加地面 + 水面
      this.addGroundAndRiver();

      // === 加载模型
      this.loadModels();

      // === 开始渲染
      this.animate();
    },

    addGroundAndRiver() {
      // 草地
      const groundGeo = new THREE.PlaneGeometry(200, 200);
      const groundMat = new THREE.MeshStandardMaterial({ color: 0x6bbf59 });
      const ground = new THREE.Mesh(groundGeo, groundMat);
      ground.rotation.x = -Math.PI / 2;
      this.scene.add(ground);

      // 河流水面
      const waterGeo = new THREE.PlaneGeometry(80, 15);
      const waterMat = new THREE.MeshStandardMaterial({
        color: 0x3ca0d3,
        transparent: true,
        opacity: 0.6,
      });
      const water = new THREE.Mesh(waterGeo, waterMat);
      water.rotation.x = -Math.PI / 2;
      water.position.set(0, 0.1, -20);
      this.scene.add(water);
    },

    loadModels() {
      const loader = new GLTFLoader();

      // ✔ 加载无人机模型
      loader.load(
        "/models/drone.glb",
        (gltf) => {
          const drone = gltf.scene;
          drone.scale.set(1.5, 1.5, 1.5);
          drone.position.set(0, 5, 0);
          this.scene.add(drone);
        },
        undefined,
        (error) => {
          console.error("加载无人机模型失败:", error);
        }
      );

      // ✔ 树木模型（如果有 tree.glb）
      loader.load(
        "/models/tree.glb",
        (gltf) => {
          const tree = gltf.scene;
          tree.scale.set(3, 3, 3);
          tree.position.set(-30, 0, -10);
          this.scene.add(tree);

          const tree2 = tree.clone();
          tree2.position.set(25, 0, -15);
          this.scene.add(tree2);
        },
        undefined,
        (err) => {
          // 如果没有 tree.glb 不报错
        }
      );
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
    },
  },
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
