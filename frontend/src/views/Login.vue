<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      message: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('access_token', response.data.access_token);
        this.message = 'Login successful!';
        this.$router.push('/'); // 登录成功后跳转到首页
      } catch (error) {
        this.message = error.response.data.msg || 'Login failed';
      }
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
