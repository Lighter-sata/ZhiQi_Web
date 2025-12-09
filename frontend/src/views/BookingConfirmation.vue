<template>
  <div class="booking-confirmation">
    <h2>Booking Confirmation</h2>
    <div v-if="bookingDetails">
      <p><strong>Booking ID:</strong> {{ bookingDetails.booking_id }}</p>
      <p><strong>Room ID:</strong> {{ bookingDetails.room_id }}</p>
      <p><strong>Check-in Date:</strong> {{ bookingDetails.check_in_date }}</p>
      <p><strong>Check-out Date:</strong> {{ bookingDetails.check_out_date }}</p>
      <p><strong>Total Price:</strong> ${{ bookingDetails.total_price }}</p>
      <p><strong>Status:</strong> {{ bookingDetails.status }}</p>

      <button @click="proceedToPayment" :disabled="isPaid">Proceed to Payment</button>
      <p v-if="paymentMessage">{{ paymentMessage }}</p>
    </div>
    <p v-else>No booking details found.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookingConfirmation',
  props: {
    bookingId: { type: [String, Number], required: true },
    // 传递其他预订详情作为 props
    room_id: [String, Number],
    check_in_date: String,
    check_out_date: String,
    total_price: [String, Number],
    status: String,
  },
  data() {
    return {
      bookingDetails: null,
      paymentMessage: '',
      isPaid: false, // 假设支付状态
    };
  },
  created() {
    this.bookingDetails = {
      booking_id: this.bookingId,
      room_id: this.room_id,
      check_in_date: this.check_in_date,
      check_out_date: this.check_out_date,
      total_price: this.total_price,
      status: this.status,
    };
    // 在实际应用中，您可能会从后端 API 获取完整的预订详情
  },
  methods: {
    async proceedToPayment() {
      if (!this.bookingDetails) return;

      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
          'http://localhost:5000/payments/create-checkout-session',
          {
            booking_id: this.bookingDetails.booking_id,
            amount: this.bookingDetails.total_price,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.paymentMessage = response.data.msg + '. Redirecting to: ' + response.data.payment_url;
        this.isPaid = true; // 模拟支付成功
        // 实际中，这里会重定向到支付网关的URL
      } catch (error) {
        this.paymentMessage = error.response.data.msg || 'Payment initiation failed';
        console.error('Payment error:', error);
      }
    },
  },
};
</script>

<style scoped>
.booking-confirmation {
  padding: 20px;
  text-align: left;
}

button {
  background-color: #42b983;
  color: white;
  cursor: pointer;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  margin-top: 20px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
