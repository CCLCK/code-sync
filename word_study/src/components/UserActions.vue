<template>
  <el-row class="user-actions">
    <el-col v-if="!user">
      <el-button @click="showLogin = true">登录</el-button>
      <el-button @click="showRegister = true">注册</el-button>
    </el-col>
    <el-col v-else>
      <p>欢迎，{{ this.email }}</p>
      <el-button @click="logout">退出</el-button>
    </el-col>

    <el-dialog title="登录" v-model="showLogin">
      <el-form @submit.prevent="login">
        <el-form-item label="邮箱" :error="emailError">
          <el-input v-model="email" placeholder="邮箱" @input="validateEmail" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password" placeholder="密码" />
        </el-form-item>
        <!-- <el-form-item>
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
        </el-form-item> -->
        <el-form-item>
          <el-button type="primary" native-type="submit">登录</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="注册" v-model="showRegister">
      <el-form @submit.prevent="register">
        <el-form-item label="邮箱&nbsp;&nbsp;&nbsp;&nbsp;" :error="emailError">
          <el-input v-model="email" placeholder="邮箱" @input="validateEmail" />
          
        </el-form-item>
        <el-form-item label="密码&nbsp;&nbsp;&nbsp;&nbsp;">
          <el-input v-model="password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item label="验证码">
          <el-input v-model="verificationCode" placeholder="验证码" />
          <el-button @click="sendVerificationCode">发送验证码</el-button>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="termsAccepted"
            >我已阅读并接受服务条款</el-checkbox
          >
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :disabled="
              !termsAccepted || !email || !password || !verificationCode
            "
            >注册</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </el-row>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      showLogin: false,
      showRegister: false,
      email: "",
      password: "",
      verificationCode: "",
      user: null,
      emailError: "",
      rememberMe: false,
      termsAccepted: false,
    };
  },
  methods: {
    async sendVerificationCode() {
      try {
        await axios.post("http://localhost:5400/register", {
          email: this.email,
          password: this.password,
        });
        this.$message.success("Verification code sent successfully");
      } catch (error) {
        console.error("Error sending verification code:", error);
        this.$message.error("Email already registered");
      }
    },
    validateEmail() {
      const re = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
      if (!re.test(this.email)) {
        this.emailError = "请输入有效的电子邮件地址";
      } else {
        this.emailError = "";
      }
    },
    login(event) {
      event.preventDefault();

      axios
        .post("http://localhost:5400/login", {
          email: this.email,
          password: this.password,
          rememberMe: this.rememberMe,
        })
        .then((response) => {
          if (response.data.message == "Logged in successfully") {
            this.user = this.email;
            this.showLogin = false;
            localStorage.setItem('user_id', response.data.user_id);
          } else {
            this.$message.error(response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error logging in:", error);
          if (error.response) {
    this.$message.error(error.response.data);
  } else {
    this.$message.error("An error occurred");
  }
        });
    },
    register(event) {
      event.preventDefault();

      axios
        .post("http://localhost:5400/verify", {
          email: this.email,
          password: this.password,
          verification_code: this.verificationCode,
        })
        .then((response) => {
          if (response.data.message == "User registered successfully") {
            this.user = this.email;
            this.showRegister = false;
            this.$message.success("User registered successfully");
            setTimeout(() => {
      location.reload();
    }, 1000);
          } else {
            this.$message.error(response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error verifying account:", error);
          this.$message.error("Error verifying account");
        });
    },
    logout() {
  this.user = null;
  location.reload();
},
  },
};
</script>

<style scoped>
</style>
