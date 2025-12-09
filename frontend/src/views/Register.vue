<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: '',
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.message = response.data.msg;
        if (response.status === 201) {
          this.$router.push('/login');
        }
      } catch (error) {
        this.message = error.response.data.msg || 'Registration failed';
      }
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
