<template>
  <title>HLearn-登录</title>
  <body style="margin: 0px">
    <div class="login-container">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>侧信道平台登录</span>
          </div>
        </template>
        <el-form
          ref="loginForm"
          :model="form"
          :rules="rules"
          label-width="120px"
        >
          <el-form-item label="账&ensp;号" prop="username">
            <el-input v-model="form.username"></el-input>
          </el-form-item>
          <el-form-item label="密&ensp;码" prop="password">
            <el-input type="password" v-model="form.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('loginForm')"
              >登录</el-button
            >
            <el-button type="success" @click="submitForm('loginForm')"
              >注册</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </body>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { ElNotification } from "element-plus";

export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入您的用户名", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入您的密码", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const requestBody = {
            username: this.form.username,
            password: this.form.password,
          };
          axios
            .post("http://localhost:8000/api/user/login", requestBody, {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
            })
            .then((response) => {
              const token = response.data.access_token;
              Cookies.set("token", token, { expires: 7 });
              ElNotification({
                title: "登录成功",
                type: "success",
              });
              this.$router.push({ name: "Dashboard" });
            })
            .catch((error) => {
              ElNotification({
                title: "用户名或密码错误",
                type: "error",
              });
            });
        } else {
          return false;
        }
      });
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #ffffff;
  margin: 0%;
}

.box-card {
  width: 400px;
  padding: 20px;
}

.card-header {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}
</style>
