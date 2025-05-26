<template>
    <div class="grid grid-cols-2 gap-4">
      <div
        v-for="(item, index) in cardItems"
        :key="index"
        class="p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100"
      >
        <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900">
          {{ item.title }}
        </h5>
  
        <div class="flex justify-center items-center gap-2 text-md text-gray-800">
          <span>{{ item.format(cryptoData?.[item.key]) }}</span>
  
          <!-- Panah dan persentase di sebelah kanan nilai -->
          <span
            v-if="item.changeKey"
            class="text-sm font-semibold flex items-center"
            :class="getChangeColor(cryptoData?.[item.changeKey])"
            :title="formatPercentageFull(cryptoData?.[item.changeKey])"
          >
            {{ getArrow(cryptoData?.[item.changeKey]) }}
            {{ formatPercentage(cryptoData?.[item.changeKey]) }}
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CardCryptoData",
    props: {
      cryptoData: Object,
    },
    methods: {
      formatShortNumber(value) {
        if (value === null || value === undefined) return "0";
        const num = Number(value);
        if (isNaN(num)) return value;
  
        const absNum = Math.abs(num);
        if (absNum >= 1.0e12) return (num / 1.0e12).toFixed(2) + "T";
        if (absNum >= 1.0e9) return (num / 1.0e9).toFixed(2) + "B";
        if (absNum >= 1.0e6) return (num / 1.0e6).toFixed(2) + "M";
        if (absNum >= 1.0e3) return (num / 1.0e3).toFixed(2) + "K";
        return num.toString();
      },
  
      formatCurrency(value) {
        if (!value && value !== 0) return "$0.00";
        return "$" + this.formatShortNumber(value);
      },
  
      formatNumber(value) {
        if (!value && value !== 0) return "0";
        return this.formatShortNumber(value);
      },
  
      // Format percentage dengan batas max agar UI tidak berantakan
      formatPercentage(value) {
        if (value === null || value === undefined) return "0.00%";
        const num = Number(value);
        if (num > 9999) return ">9999%";
        if (num < -9999) return "<-9999%";
        return num.toFixed(2) + "%";
      },
  
      // Format full percentage tanpa batas (untuk tooltip)
      formatPercentageFull(value) {
        if (value === null || value === undefined) return "0.00%";
        return Number(value).toFixed(2) + "%";
      },
  
      getArrow(value) {
        if (value > 0) return "▲";
        if (value < 0) return "▼";
        return "";
      },
  
      getChangeColor(value) {
        if (value > 0) return "text-green-600";
        if (value < 0) return "text-red-600";
        return "text-gray-500";
      },
    },
    computed: {
      cardItems() {
        return [
          {
            title: "Price",
            key: "Price",
            format: this.formatCurrency,
            changeKey: "PriceChangePercentage",
          },
          {
            title: "Market Cap (USD)",
            key: "MarketCap",
            format: this.formatCurrency,
            changeKey: "MarketCapChangePercentage",
          },
          {
            title: "24h Volume (USD)",
            key: "Volume24h",
            format: this.formatCurrency,
            // no changeKey agar tidak tampil persentase volume
          },
          {
            title: "FDV (USD)",
            key: "FDV",
            format: this.formatCurrency,
          },
          {
            title: "Total Supply",
            key: "TotalSupply",
            format: this.formatNumber,
          },
          {
            title: "Max Supply",
            key: "MaxSupply",
            format: (val) => (val ? this.formatNumber(val) : "Null"),
          },
          {
            title: "Circulating Supply",
            key: "CirculatingSupply",
            format: this.formatNumber,
          },
          {
            title: "ATH",
            key: "ATH",
            format: this.formatCurrency,
            changeKey: "ATHChangePercentage",
          },
          {
            title: "ATL",
            key: "ATL",
            format: this.formatCurrency,
            changeKey: "ATLChangePercentage",
          },
        ];
      },
    },
  };
  </script>
  