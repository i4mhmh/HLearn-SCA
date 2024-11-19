<template>
  <title>HLearn-侧信道攻击控制台</title>
  <div class="common-layout">
    <el-container>
      <el-header style="padding: 0%">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
        >
          <el-menu-item index="0">
            <img
              style="width: 80px"
              src="@/images/logo.svg"
              alt="HLearn logo"
            />
          </el-menu-item>
          <el-sub-menu index="1">
            <template #title> 个人中心 </template>
            <el-menu-item index="1-0">个人信息</el-menu-item>
            <el-menu-item index="1-1">执行任务</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="2">退出登录</el-menu-item>
        </el-menu>
      </el-header>
      <el-container style="display: flex">
        <el-aside style="width: 200px">
          <el-row class="tac">
            <el-col>
              <el-menu
                default-active="2"
                class="el-menu-vertical-demo"
                @open="handleOpen"
                @close="handleClose"
                style="height: 83vh"
              >
                <el-sub-menu index="1">
                  <template #title>
                    <el-icon><location /></el-icon>
                    <span>主控台</span>
                  </template>
                  <el-menu-item-group title="Group One">
                    <el-menu-item index="1-1">item one</el-menu-item>
                    <el-menu-item index="1-2">item two</el-menu-item>
                  </el-menu-item-group>
                  <el-menu-item-group title="Group Two">
                    <el-menu-item index="1-3">item three</el-menu-item>
                  </el-menu-item-group>
                  <el-sub-menu index="1-4">
                    <template #title>item four</template>
                    <el-menu-item index="1-4-1">item one</el-menu-item>
                  </el-sub-menu>
                </el-sub-menu>
                <el-menu-item index="2">
                  <el-icon><icon-menu /></el-icon>
                  <span>Navigator Two</span>
                </el-menu-item>
                <el-menu-item index="3" disabled>
                  <el-icon><document /></el-icon>
                  <span>Navigator Three</span>
                </el-menu-item>
                <el-menu-item index="4">
                  <el-icon><setting /></el-icon>
                  <span>Navigator Four</span>
                </el-menu-item>
              </el-menu>
            </el-col>
          </el-row>
        </el-aside>
        <el-main>Main</el-main>
      </el-container>
      <el-footer style="background-color: aliceblue; align-items: center">
        <center>
          侧信道攻击控制平台 &copy; 2024 <br />Made by Minghui Hou & Guilin
          University of Electronic Technology
        </center>
      </el-footer>
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
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>
