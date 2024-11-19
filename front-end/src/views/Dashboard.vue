<template>
  <title>HLearn-侧信道攻击控制台</title>
  <div class="common-layout">
    <el-container>
      <el-header
        ><el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
        >
          <el-menu-item index="0" @select="handleLogoSelect">
            <img
              style="width: 50px; height: 30px"
              src="@/images/logo.jpg"
              alt="HLearn logo"
            />
          </el-menu-item>
          <el-menu-item index="1">Processing Center</el-menu-item>
          <el-sub-menu index="2">
            <template #title>Workspace</template>
            <el-menu-item index="2-1">item one</el-menu-item>
            <el-menu-item index="2-2">item two</el-menu-item>
            <el-menu-item index="2-3">item three</el-menu-item>
            <el-sub-menu index="2-4">
              <template #title>item four</template>
              <el-menu-item index="2-4-1">item one</el-menu-item>
              <el-menu-item index="2-4-2">item two</el-menu-item>
              <el-menu-item index="2-4-3">item three</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-scrollba>
            <el-menu :default-openeds="['1', '3']">
              <el-sub-menu index="1">
                <template #title>
                  <el-icon>
                    <message />
                  </el-icon>
                </template>
              </el-sub-menu>
            </el-menu>
          </el-scrollba>
        </el-aside>
        <el-container>
          <el-main>Main</el-main>
          <el-footer>HLearn By M0nk3y</el-footer>
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
    // 处理logo点击事件
    const handleLogoSelect = (index) => {
      console.log(index);
      router.push({ name: "Dashboard" });
    };

    onMounted(() => {
      checkAuthentication();
    });
    return {
      isAuthenticated,
      checkAuthentication,
      username,
      handleLogoSelect,
    };
  },
};
</script>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
}
.common-layout {
  display: flex;
  flex: 1;
}
.el-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.el-main {
  flex: 1;
}
</style>
