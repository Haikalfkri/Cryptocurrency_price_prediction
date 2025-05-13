<template>
  <div class="min-h-screen bg-white relative">
    <Navbar class="top-0 left-0 w-full bg-white shadow z-50" />

    <div class="max-w-3xl mx-auto mt-16 px-4 sm:px-6 lg:px-8">
      <!-- About Us -->
      <section class="mb-10">
        <h1 class="text-2xl font-bold text-gray-800 mb-4 text-left">
          About Us
        </h1>
        <p class="text-gray-600 leading-relaxed text-left text-sm sm:text-base">
          Cryptocurrency Price Prediction is a system built to assist both beginner and professional investors in
          analyzing and forecasting the future prices of various cryptocurrencies. In the volatile world of digital
          assets, having access to intelligent prediction tools is crucial to make informed investment decisions. Our
          platform leverages machine learning algorithms and real-time market sentiment to deliver predictive insights,
          helping users understand potential market movements.
          <br><br>
          With a user-friendly interface and comprehensive data analysis features, the system is designed to make
          complex financial forecasting more accessible. Whether you're just starting your crypto journey or looking to
          fine-tune your investment strategies, this tool provides valuable support and clarity. Our goal is to bridge
          the gap between data science and practical crypto investment, empowering users to make smarter choices and
          reduce risks. As the crypto market continues to grow, we’re committed to evolving with it and delivering
          consistent, accurate insights.
        </p>
      </section>

      <!-- Contact Us -->
      <section class="mb-10">
        <h2 class="text-xl font-semibold text-gray-800 mb-2 text-left">Contact Us</h2>
        <div class="text-gray-600 text-left text-sm">
          <p>Email: <a href="mailto:support@cryptopredictor.com"
              class="text-blue-500 hover:underline">support@cryptopredictor.com</a></p>
          <p>Instagram: <a href="https://instagram.com/cryptopredictor" target="_blank"
              class="text-blue-500 hover:underline">@cryptopredictor</a></p>
        </div>
      </section>

      <!-- Feedback -->
      <section class="mb-16">
        <h2 class="text-xl font-semibold text-gray-800 mb-2 text-left">Feedback</h2>
        <p class="text-gray-600 text-sm mb-4 text-left">
          If you have any suggestions, feature ideas, bug reports, or general feedback, feel free to submit them below.
        </p>

        <form @submit.prevent="submitFeedback" class="space-y-4 text-left relative">
          <textarea v-model="feedback" rows="4"
            class="w-full p-3 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
            placeholder="Write your feedback here..." required></textarea>

          <button type="submit"
            class="w-full sm:w-auto bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition disabled:opacity-50"
            :disabled="loading">
            {{ loading ? 'Sending...' : 'Submit Feedback' }}
          </button>
        </form>
      </section>
    </div>

    <!-- Modal -->
    <div v-if="successMessage || errorMessage"
      class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-sm w-full text-center">
        <h3 class="text-lg font-semibold mb-2 text-gray-800">
          {{ successMessage ? 'Success' : 'Error' }}
        </h3>
        <p class="text-sm text-gray-600 mb-4">
          {{ successMessage || errorMessage }}
        </p>
        <button @click="closeModal" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition">
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/NavbarCom.vue';
import axios from 'axios';

axios.defaults.headers.common["ngrok-skip-browser-warning"] = true;

export default {
  name: "UserFeedbackPage",
  components: {
    Navbar,
  },
  data() {
    return {
      feedback: '',
      successMessage: '',
      errorMessage: '',
      loading: false,
    };
  },
  methods: {
    async submitFeedback() {
      this.loading = true;
      try {
        const token = localStorage.getItem('accessToken');
        await axios.post(
          'http://127.0.0.1:8000/api/v1/userFeedback/',
          { feedback: this.feedback },
          {
            withCredentials: true,
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.successMessage = "Thank you! Your feedback has been submitted.";
        this.feedback = '';

        // Auto close after 1 second
        setTimeout(() => {
          this.closeModal();
        }, 2000);
      } catch (error) {
        this.errorMessage = "Failed to send feedback. Please try again.";
        console.error(error);

        setTimeout(() => {
          this.closeModal();
        }, 2000);
      } finally {
        this.loading = false;
      }
    },
    closeModal() {
      this.successMessage = '';
      this.errorMessage = '';
    },
  },
};
</script>

<style scoped></style>