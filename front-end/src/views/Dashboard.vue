<template>
  <title>HLearn-侧信道攻击控制台</title>
  <div class="common-layout">
    <el-container>
      <el-header style="padding: 0%">
        <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false">
          <el-menu-item index="0" @click="handleTopMenu(1)">
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
                default-active="1"
                class="el-menu-vertical-demo"
                style="height: 83.5vh"
              >
                <el-menu-item index="1" @click="handleMenuSelect(1)">
                  <template #title>
                    <el-icon><Odometer /></el-icon>
                    <span>服务端态势感知</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="2" @click="handleMenuSelect(2)">
                  <el-icon><Promotion /></el-icon>
                  <span>数据集上传</span>
                </el-menu-item>
                <el-sub-menu index="3" @click="handleMenuSelect(3)">
                  <template #title>
                    <el-icon><document /></el-icon>
                    <span>攻击</span>
                  </template>
                  <el-menu-item index="3-1" @click="handleMenuSelect(3.1)">
                    非建模类攻击
                  </el-menu-item>
                  <el-menu-item index="3-2" @click="handleMenuSelect(3.2)">
                    建模类攻击
                  </el-menu-item>
                </el-sub-menu>
                <el-menu-item index="4" @click="handleMenuSelect(4)">
                  <el-icon><Menu /></el-icon>
                  <span>任务中心</span>
                </el-menu-item>
                <el-menu-item index="5" @click="handleMenuSelect(5)">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>结果展示</span>
                </el-menu-item>
              </el-menu>
            </el-col>
          </el-row>
        </el-aside>
        <el-main><router-view /></el-main>
      </el-container>
      <el-footer style="background-color: aliceblue; align-items: center">
        <div style="text-align: center">
          侧信道攻击控制平台 &copy; 2024 <br />Made by Minghui Hou & Guilin
          University of Electronic Technology
        </div>
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
    const handleTopMenu = (index) => {
      if (index === 1) {
        window.location.reload("/");
      }
    };

    const handleMenuSelect = (index) => {
      if (index == 1) {
        router.push({ name: "SSA" });
      } else if (index == 2) {
        router.push({ name: "DataUpload" });
      }
    };

    onMounted(() => {
      checkAuthentication();
    });
    return {
      isAuthenticated,
      checkAuthentication,
      username,
      handleTopMenu,
      handleMenuSelect,
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
