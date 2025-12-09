<template>
  <div class="user-dashboard">
    <h2>User Dashboard</h2>
    <div v-if="bookings.length">
      <h3>My Bookings</h3>
      <div v-for="booking in bookings" :key="booking.id" class="booking-card">
        <p><strong>Booking ID:</strong> {{ booking.id }}</p>
        <p><strong>Room ID:</strong> {{ booking.room_id }}</p>
        <p><strong>Check-in Date:</strong> {{ booking.check_in_date }}</p>
        <p><strong>Check-out Date:</strong> {{ booking.check_out_date }}</p>
        <p><strong>Total Price:</strong> ${{ booking.total_price }}</p>
        <p><strong>Status:</strong> {{ booking.status }}</p>
        <button @click="cancelBooking(booking.id)" :disabled="booking.status === 'cancelled'">Cancel Booking</button>
      </div>
    </div>
    <p v-else>No bookings found.</p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // 导入 jwt-decode

export default {
  name: 'UserDashboard',
  data() {
    return {
      bookings: [],
      message: '',
    };
  },
  created() {
    this.fetchUserBookings();
  },
  methods: {
    async fetchUserBookings() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.message = 'Please log in to view your bookings.';
          return;
        }
        const decodedToken = jwtDecode(token); // 解码 token
        const userId = decodedToken.sub; // 获取用户ID

        const response = await axios.get(`http://localhost:5000/users/${userId}/bookings`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.bookings = response.data.bookings;
      } catch (error) {
        this.message = error.response.data.msg || 'Error fetching bookings.';
        console.error('Error fetching bookings:', error);
      }
    },
    async cancelBooking(bookingId) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.message = 'Please log in to cancel bookings.';
          return;
        }

        const response = await axios.delete(`http://localhost:5000/bookings/${bookingId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.message = response.data.msg;
        this.fetchUserBookings(); // Refresh bookings
      } catch (error) {
        this.message = error.response.data.msg || 'Failed to cancel booking';
        console.error('Cancel booking error:', error);
      }
    },
  },
};
</script>

<style scoped>
.user-dashboard {
  padding: 20px;
  text-align: left;
}

.booking-card {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}

button {
  background-color: #dc3545;
  color: white;
  cursor: pointer;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  margin-top: 5px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
