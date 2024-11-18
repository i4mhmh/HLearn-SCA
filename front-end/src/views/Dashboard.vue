<template>
  <title>HLearn-侧信道攻击控制台</title>
  <div class="common-layout">
    <el-container>
      <el-header><h1>HLearn</h1></el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
        <el-container>
          <el-main>Main</el-main>
          <el-footer>Footer</el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>
<script>
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import router from "@/router";
import axios from "axios";
import { ElNotification } from "element-plus";

export default {
  setup() {
    const username = ref(null);
    const isAuthenticated = ref(false);
    const checkAuthentication = async () => {
      const token = Cookies.get("token");
      console.log(token);
      if (!token) {
        this.$router.push({ name: "Login" });
        return;
      }
      try {
        const response = await axios.get(
          "http://localhost:8000/api/user/verify-token",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        username.value = response.data;
      } catch (error) {
        ElNotification({
          title: "请先登录",
          type: "warning",
        });
        router.push({ name: "Login" });
        return;
      }
    };
    onMounted(() => {
      checkAuthentication();
    });
    return {
      isAuthenticated,
      checkAuthentication,
      username,
    };
  },
};
</script>

<style ></style>
