<template>
  <div class="hotel-list">
    <h2>Available Hotels</h2>
    <div class="search-filter">
      <input type="text" v-model="searchQuery" placeholder="Search by city or hotel name" @input="fetchHotels" />
    </div>
    <div v-if="hotels.length">
      <div v-for="hotel in filteredHotels" :key="hotel.id" class="hotel-card">
        <h3>{{ hotel.name }}</h3>
        <p>{{ hotel.address }}, {{ hotel.city }}, {{ hotel.country }}</p>
        <p>Rating: {{ hotel.rating }}</p>
        <img v-if="hotel.image_url" :src="hotel.image_url" alt="Hotel Image" class="hotel-image" />
        <router-link :to="`/hotels/${hotel.id}`">View Details</router-link>
      </div>
    </div>
    <p v-else>No hotels found.</p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HotelList',
  data() {
    return {
      hotels: [],
      searchQuery: '',
      message: '',
    };
  },
  computed: {
    filteredHotels() {
      const query = this.searchQuery.toLowerCase();
      return this.hotels.filter(hotel => 
        hotel.city.toLowerCase().includes(query) || 
        hotel.name.toLowerCase().includes(query)
      );
    },
  },
  created() {
    this.fetchHotels();
  },
  methods: {
    async fetchHotels() {
      try {
        const response = await axios.get('http://localhost:5000/hotels');
        this.hotels = response.data.hotels;
      } catch (error) {
        this.message = 'Error fetching hotels.';
        console.error('Error fetching hotels:', error);
      }
    },
  },
};
</script>

<style scoped>
.hotel-list {
  padding: 20px;
}

.search-filter {
  margin-bottom: 20px;
}

.hotel-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  text-align: left;
}

.hotel-image {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 4px;
}
</style>
