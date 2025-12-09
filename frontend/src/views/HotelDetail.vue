<template>
  <div class="hotel-detail">
    <div v-if="hotel">
      <h2>{{ hotel.name }}</h2>
      <p>{{ hotel.address }}, {{ hotel.city }}, {{ hotel.country }}</p>
      <p>Rating: {{ hotel.rating }}</p>
      <img v-if="hotel.image_url" :src="hotel.image_url" alt="Hotel Image" class="hotel-image" />
      <p>{{ hotel.description }}</p>

      <h3>Available Rooms</h3>
      <div v-if="rooms.length">
        <div v-for="room in rooms" :key="room.id" class="room-card">
          <h4>{{ room.type }} - Room {{ room.room_number }}</h4>
          <p>Price: ${{ room.price }} per night</p>
          <p>Capacity: {{ room.capacity }}</p>
          <p>Amenities: {{ room.amenities }}</p>
          <p :class="{ 'available': room.is_available, 'unavailable': !room.is_available }">
            Status: {{ room.is_available ? 'Available' : 'Unavailable' }}
          </p>
          <button v-if="room.is_available" @click="selectRoom(room)">Book Now</button>
        </div>
      </div>
      <p v-else>No rooms available for this hotel.</p>

      <div v-if="selectedRoom">
        <h3>Book Room {{ selectedRoom.room_number }}</h3>
        <form @submit.prevent="handleBooking">
          <div>
            <label for="checkInDate">Check-in Date:</label>
            <input type="date" id="checkInDate" v-model="checkInDate" required />
          </div>
          <div>
            <label for="checkOutDate">Check-out Date:</label>
            <input type="date" id="checkOutDate" v-model="checkOutDate" required />
          </div>
          <button type="submit">Confirm Booking</button>
        </form>
        <p v-if="bookingMessage">{{ bookingMessage }}</p>
      </div>

      <h3>Reviews</h3>
      <div v-if="reviews.length">
        <div v-for="review in reviews" :key="review.id" class="review-card">
          <p><strong>{{ review.username }}</strong> rated {{ review.rating }}/5</p>
          <p>{{ review.comment }}</p>
          <small>{{ review.created_at }}</small>
        </div>
      </div>
      <p v-else>No reviews yet. Be the first to review!</p>

      <div v-if="isLoggedIn">
        <h3>Submit a Review</h3>
        <form @submit.prevent="submitReview">
          <div>
            <label for="rating">Rating (1-5):</label>
            <input type="number" id="rating" v-model="newReview.rating" min="1" max="5" required />
          </div>
          <div>
            <label for="comment">Comment:</label>
            <textarea id="comment" v-model="newReview.comment"></textarea>
          </div>
          <button type="submit">Submit Review</button>
        </form>
        <p v-if="reviewMessage">{{ reviewMessage }}</p>
      </div>
    </div>
    <p v-else-if="message">{{ message }}</p>
    <p v-else>Loading hotel details...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HotelDetail',
  data() {
    return {
      hotel: null,
      rooms: [],
      reviews: [],
      message: '',
      selectedRoom: null,
      checkInDate: '',
      checkOutDate: '',
      bookingMessage: '',
      newReview: {
        rating: 5,
        comment: '',
      },
      reviewMessage: '',
    };
  },
  computed: {
    isLoggedIn() {
      return localStorage.getItem('access_token') !== null;
    },
  },
  created() {
    this.fetchHotelDetails();
    this.fetchHotelRooms();
    this.fetchHotelReviews();
  },
  methods: {
    async fetchHotelDetails() {
      try {
        const hotelId = this.$route.params.id;
        const response = await axios.get(`http://localhost:5000/hotels/${hotelId}`);
        this.hotel = response.data;
      } catch (error) {
        this.message = 'Error fetching hotel details.';
        console.error('Error fetching hotel details:', error);
      }
    },
    async fetchHotelRooms() {
      try {
        const hotelId = this.$route.params.id;
        const response = await axios.get(`http://localhost:5000/rooms/hotel/${hotelId}`);
        this.rooms = response.data.rooms;
      } catch (error) {
        this.message = 'Error fetching rooms.';
        console.error('Error fetching rooms:', error);
      }
    },
    async fetchHotelReviews() {
      try {
        const hotelId = this.$route.params.id;
        const response = await axios.get(`http://localhost:5000/reviews/hotel/${hotelId}`);
        this.reviews = response.data.reviews;
      } catch (error) {
        this.message = 'Error fetching reviews.';
        console.error('Error fetching reviews:', error);
      }
    },
    selectRoom(room) {
      this.selectedRoom = room;
      this.bookingMessage = '';
    },
    async handleBooking() {
      if (!this.selectedRoom) {
        this.bookingMessage = 'Please select a room first.';
        return;
      }
      if (!this.isLoggedIn) {
        this.bookingMessage = 'Please log in to book a room.';
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
          'http://localhost:5000/bookings',
          {
            room_id: this.selectedRoom.id,
            check_in_date: this.checkInDate,
            check_out_date: this.checkOutDate,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.bookingMessage = response.data.msg + ` Total Price: $${response.data.total_price}`;
        this.selectedRoom = null;
        this.checkInDate = '';
        this.checkOutDate = '';
        this.fetchHotelRooms(); // Refresh room availability
      } catch (error) {
        this.bookingMessage = error.response.data.msg || 'Booking failed';
        console.error('Booking error:', error);
      }
    },
    async submitReview() {
      if (!this.isLoggedIn) {
        this.reviewMessage = 'Please log in to submit a review.';
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        const hotelId = this.$route.params.id;
        const response = await axios.post(
          `http://localhost:5000/reviews/hotel/${hotelId}`,
          this.newReview,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.reviewMessage = response.data.msg;
        this.newReview.rating = 5;
        this.newReview.comment = '';
        this.fetchHotelReviews(); // Refresh reviews
      } catch (error) {
        this.reviewMessage = error.response.data.msg || 'Failed to submit review';
        console.error('Review submission error:', error);
      }
    },
  },
};
</script>

<style scoped>
.hotel-detail {
  padding: 20px;
  text-align: left;
}

.hotel-image {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 4px;
}

h3 {
  margin-top: 20px;
  margin-bottom: 10px;
}

.room-card, .review-card {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}

.available {
  color: green;
}

.unavailable {
  color: red;
}

form div {
  margin-bottom: 10px;
}

form label {
  display: inline-block;
  width: 120px;
}

form input, form textarea, form button {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

form button {
  background-color: #42b983;
  color: white;
  cursor: pointer;
  border: none;
  padding: 10px 15px;
}
</style>
