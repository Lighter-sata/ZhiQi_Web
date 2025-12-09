<template>
  <div class="admin-dashboard">
    <h2>Admin Dashboard</h2>

    <h3>Manage Hotels</h3>
    <form @submit.prevent="addHotel">
      <input type="text" v-model="newHotel.name" placeholder="Name" required />
      <input type="text" v-model="newHotel.address" placeholder="Address" required />
      <input type="text" v-model="newHotel.city" placeholder="City" required />
      <input type="text" v-model="newHotel.country" placeholder="Country" required />
      <textarea v-model="newHotel.description" placeholder="Description"></textarea>
      <input type="text" v-model="newHotel.image_url" placeholder="Image URL" />
      <button type="submit">Add Hotel</button>
    </form>
    <p v-if="hotelMessage">{{ hotelMessage }}</p>
    <div v-if="hotels.length">
      <div v-for="hotel in hotels" :key="hotel.id" class="admin-card">
        <p><strong>{{ hotel.name }}</strong> ({{ hotel.city }})</p>
        <button @click="deleteHotel(hotel.id)">Delete</button>
      </div>
    </div>
    <p v-else>No hotels to manage.</p>

    <h3>Manage Users</h3>
    <p v-if="userMessage">{{ userMessage }}</p>
    <div v-if="users.length">
      <div v-for="user in users" :key="user.id" class="admin-card">
        <p><strong>{{ user.username }}</strong> ({{ user.email }})</p>
        <button @click="deleteUser(user.id)">Delete</button>
      </div>
    </div>
    <p v-else>No users to manage.</p>

    <h3>Manage Bookings</h3>
    <p v-if="bookingMessage">{{ bookingMessage }}</p>
    <div v-if="bookings.length">
      <div v-for="booking in bookings" :key="booking.id" class="admin-card">
        <p><strong>Booking ID:</strong> {{ booking.id }}</p>
        <p>User: {{ booking.user_id }}, Room: {{ booking.room_id }}</p>
        <p>Status: {{ booking.status }}</p>
        <select v-model="booking.status" @change="updateBookingStatus(booking.id, booking.status)">
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="cancelled">Cancelled</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>
    </div>
    <p v-else>No bookings to manage.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      hotels: [],
      users: [],
      bookings: [],
      newHotel: {
        name: '',
        address: '',
        city: '',
        country: '',
        description: '',
        image_url: '',
      },
      hotelMessage: '',
      userMessage: '',
      bookingMessage: '',
    };
  },
  created() {
    this.fetchHotels();
    this.fetchUsers();
    this.fetchAllBookings();
  },
  methods: {
    async fetchHotels() {
      try {
        const response = await axios.get('http://localhost:5000/hotels');
        this.hotels = response.data.hotels;
      } catch (error) {
        this.hotelMessage = 'Error fetching hotels.';
        console.error('Error fetching hotels:', error);
      }
    },
    async addHotel() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post('http://localhost:5000/hotels', this.newHotel, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.hotelMessage = response.data.msg;
        this.newHotel = { name: '', address: '', city: '', country: '', description: '', image_url: '' };
        this.fetchHotels();
      } catch (error) {
        this.hotelMessage = error.response.data.msg || 'Failed to add hotel';
        console.error('Add hotel error:', error);
      }
    },
    async deleteHotel(hotelId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.delete(`http://localhost:5000/hotels/${hotelId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.hotelMessage = response.data.msg;
        this.fetchHotels();
      } catch (error) {
        this.hotelMessage = error.response.data.msg || 'Failed to delete hotel';
        console.error('Delete hotel error:', error);
      }
    },
    async fetchUsers() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/admin/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.users = response.data.users;
      } catch (error) {
        this.userMessage = error.response.data.msg || 'Error fetching users.';
        console.error('Error fetching users:', error);
      }
    },
    async deleteUser(userId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.delete(`http://localhost:5000/admin/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.userMessage = response.data.msg;
        this.fetchUsers();
      } catch (error) {
        this.userMessage = error.response.data.msg || 'Failed to delete user';
        console.error('Delete user error:', error);
      }
    },
    async fetchAllBookings() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/admin/bookings', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.bookings = response.data.bookings;
      } catch (error) {
        this.bookingMessage = error.response.data.msg || 'Error fetching bookings.';
        console.error('Error fetching bookings:', error);
      }
    },
    async updateBookingStatus(bookingId, status) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`http://localhost:5000/admin/bookings/${bookingId}/status`, { status }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.bookingMessage = response.data.msg;
        this.fetchAllBookings();
      } catch (error) {
        this.bookingMessage = error.response.data.msg || 'Failed to update booking status';
        console.error('Update booking status error:', error);
      }
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  text-align: left;
}

h3 {
  margin-top: 20px;
  margin-bottom: 10px;
}

form input, form textarea, form button, .admin-card select {
  display: block;
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

form button {
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border: none;
  padding: 10px 15px;
}

.admin-card {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-card button {
  width: auto;
  margin-left: 10px;
  background-color: #dc3545;
}
</style>
